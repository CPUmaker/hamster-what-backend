from django.shortcuts import render
from django.urls import reverse
from rest_framework import generics
from rest_framework.response import Response
from dj_rest_auth.registration.views import SocialConnectView, SocialLoginView
from dj_rest_auth.social_serializers import TwitterLoginSerializer
from knox.models import AuthToken
from allauth.socialaccount.providers.apple.client import AppleOAuth2Client
from allauth.socialaccount.providers.apple.views import AppleOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.twitter.views import TwitterOAuthAdapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client

from core.serializers.login import LoginSerializer
from core.serializers.appleSocialLoginSerializer import AppleSocialLoginSerializer
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


class AppleLogin(SocialLoginView):
    adapter_class = AppleOAuth2Adapter
    client_class = AppleOAuth2Client

    @property
    def callback_url(self):
        return self.request.build_absolute_uri(reverse('apple_callback'))


class GoogleLogin(SocialLoginView): # if you want to use Authorization Code Grant, use this
    adapter_class = GoogleOAuth2Adapter
    client_class = OAuth2Client

    @property
    def callback_url(self):
        return self.request.build_absolute_uri(reverse('google_callback'))


class TwitterLogin(SocialLoginView):
    serializer_class = TwitterLoginSerializer
    adapter_class = TwitterOAuthAdapter


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
