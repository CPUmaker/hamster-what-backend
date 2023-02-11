from django.shortcuts import render
from rest_framework import generics, HTTP_HEADER_ENCODING
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response
from knox.auth import TokenAuthentication
from knox.models import AuthToken
from django.contrib.auth.backends import AllowAllUsersModelBackend

from core.serializers.login import LoginSerializer
from core.serializers.register import RegisterSerializer
from core.serializers.user import UserSerializer


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
