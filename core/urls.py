from django.urls import path, include
from knox import views as knox_views
from rest_framework import routers

from core.api.auth import RegisterAPI, LoginAPI, AppleLogin, GoogleLogin, TwitterLogin, verify_user_and_activate
from core.api.password import ChangePasswordView
from core.api.profile import ProfileViewSet

router = routers.DefaultRouter()

urlpatterns = router.urls

urlpatterns += [
    # auth
    path('api/auth/register', RegisterAPI.as_view(), name='register'),
    path('api/auth/activate/<token>', verify_user_and_activate, name='activate'),
    path('api/auth/login', LoginAPI.as_view(), name='login'),
    path('api/auth/logout', knox_views.LogoutView.as_view(), name='logout'),
    path('api/auth/apple', AppleLogin.as_view(), name='apple_login'),
    path('api/auth/google', GoogleLogin.as_view(), name='google_login'),
    path('api/auth/twitter', TwitterLogin.as_view(), name='twitter_login'),
    # passwd
    path('api/change-password', ChangePasswordView.as_view(), name='change-password'),
    path('api/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    # profile
    path('api/profile', ProfileViewSet.as_view(), name='profile')
]
