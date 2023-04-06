import json
import jwt
from jwt.algorithms import RSAAlgorithm
import requests

from django.contrib.auth.models import User
from django.shortcuts import render
from django.urls import reverse
from rest_framework import generics, status, serializers, HTTP_HEADER_ENCODING, permissions
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response
from knox.auth import TokenAuthentication
from knox.models import AuthToken

from core.models.social_account import SocialAccount
from core.serializers.login import LoginSerializer
from core.serializers.register import RegisterSerializer
from core.serializers.user import UserSerializer
from core.serializers.socialAuthSerializer import AppleUserInputSerializer, FacebookUserInputSerializer, GoogleUserInputSerializer


class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user.is_active = False
        user.save()
        token = AuthToken.objects.create(user)
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": token[1]
        })


class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        token = AuthToken.objects.create(user)
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": token[1],
        })


class AppleLogin(generics.GenericAPIView):
    serializer_class = AppleUserInputSerializer
    APPLE_PUBLIC_KEY_URL = "https://appleid.apple.com/auth/keys"
    APPLE_APP_ID = "com.hamsterwhat.ios"
    
    def _decode_apple_user_token(self, apple_user_token):
        key_payload = requests.get(self.APPLE_PUBLIC_KEY_URL).json()

        for public_key in key_payload["keys"]:
            public_key = RSAAlgorithm.from_jwk(json.dumps(public_key))
            try:
                token = jwt.decode(apple_user_token, public_key, audience=[self.APPLE_APP_ID, 'host.exp.Exponent'], algorithms=['RS256'])
            except jwt.exceptions.ExpiredSignatureError as e:
                serializers.ValidationError({"id_token": "That token has expired."})
            except jwt.exceptions.InvalidAudienceError as e:
                serializers.ValidationError({"id_token": "That token's audience did not match."})
            except Exception as e:
                continue
        
        if token is None:
            serializers.ValidationError({"id_token": "That token is invalid."})
        return token

    def post(self, request):
        print(request.data)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        id_token = serializer.validated_data.get('id_token')
        data_from_id_token = self._decode_apple_user_token(id_token)
        print(data_from_id_token)
        
        identity = 'apple_' + data_from_id_token.get('sub')
        if SocialAccount.objects.filter(identity=identity).exists():
            user = SocialAccount.objects.filter(identity=identity).first().user
        else:
            user, created = User.objects.get_or_create(
                username=identity,
                password=User.objects.make_random_password(),
                email=data_from_id_token.get('email', None),
            )
            social_account = SocialAccount(identity=identity, user=user)
            social_account.save()
        token = AuthToken.objects.create(user)
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": token[1],
        })


class GoogleLogin(generics.GenericAPIView):
    serializer_class = GoogleUserInputSerializer
    GOOGLE_API = "https://www.googleapis.com/userinfo/v2/me"

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        access_token = serializer.validated_data.get('access_token')
        req = requests.get(self.GOOGLE_API, params={'access_token': access_token})
        data_from_api = req.json()
        
        identity = 'google_' + data_from_api.get('id')
        if SocialAccount.objects.filter(identity=identity).exists():
            user = SocialAccount.objects.filter(identity=identity).first().user
        else:
            user, created = User.objects.get_or_create(
                username=identity,
                password=User.objects.make_random_password(),
                email=data_from_api.get('email', None),
            )
            if created:
                user.first_name = data_from_api.get('given_name', user.first_name)
                user.last_name = data_from_api.get('family_name', user.last_name)
                user.save()
                user.profile.photo = data_from_api.get('picture', user.profile.photo)
                user.profile.save()
            social_account = SocialAccount(identity=identity, user=user)
            social_account.save()
        token = AuthToken.objects.create(user)
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": token[1],
        })


class FacebookLogin(generics.GenericAPIView):
    serializer_class = FacebookUserInputSerializer
    FACEBOOK_API = "https://graph.facebook.com/me"

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        access_token = serializer.validated_data.get('access_token')
        req = requests.get(self.FACEBOOK_API, params={'fields': 'id,name,email,first_name,last_name,picture', 'access_token': access_token})
        data_from_api = req.json()
        
        identity = 'fb_' + data_from_api.get('id')
        if SocialAccount.objects.filter(identity=identity).exists():
            user = SocialAccount.objects.filter(identity=identity).first().user
        else:
            user, created = User.objects.get_or_create(
                username=identity,
                password=User.objects.make_random_password(),
                email=data_from_api.get('email', None),
            )
            if created:
                user.first_name = data_from_api.get('first_name', user.first_name)
                user.last_name = data_from_api.get('last_name', user.last_name)
                user.save()
                user.profile.photo = data_from_api.get('picture', {}).get('data', {}).get('url', user.profile.photo)
                user.profile.save()
            social_account = SocialAccount(identity=identity, user=user)
            social_account.save()
        token = AuthToken.objects.create(user)
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": token[1],
        })


@api_view(['GET'])
@authentication_classes([])
def validate_token(request):
    try:
        authenticator = TokenAuthentication()
        user, auth_token = authenticator.authenticate(request)
        if user and auth_token:
            return Response({'valid': 'true'})
    except:
        return Response({'valid': 'false'})


class DeleteAccountAPI(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def delete(self, request):
        user = self.request.user
        if user:
            user.delete()
            return Response({'msg': 'Delete successfully.'})
        return Response({'msg': 'Failed to delete this account.'}, status=status.HTTP_401_UNAUTHORIZED)


def verify_user_and_activate(request, token):
    try:
        auth = AuthToken.objects.filter(digest=token).first()
        auth.user.is_active = True
        auth.user.save()
        return render(
            request,
            template_name='email/verification_success.html',
            context={
                'msg': 'Your Email is verified successfully and account has been activated.',
                'status': 'Verification Successful!',
            }
        )
    except:
        return render(
            request,
            template_name='email/verification_fail.html',
            context={
                'msg': 'There is something wrong with this link, unable to verify the user...',
                'minor_msg': 'There is something wrong with this link...',
                'status': 'Verification Failed!',
            }
        )
