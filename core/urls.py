from django.urls import path, include
from knox import views as knox_views
from rest_framework import routers

from core.api.auth import RegisterAPI, LoginAPI, AppleLogin, GoogleLogin, FacebookLogin, validate_token, verify_user_and_activate
from core.api.password import ChangePasswordView
from core.api.profile import ProfileViewSet
from core.api.coupon import CouponViewSet
from core.api.bill import *

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
    path('api/auth/facebook', FacebookLogin.as_view(), name='facebook_login'),
    path('api/auth/validate-token', validate_token, name='validate-token'),
    # passwd
    path('api/change-password', ChangePasswordView.as_view(), name='change-password'),
    path('api/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    # profile
    path('api/profile', ProfileViewSet.as_view(), name='profile'),
    # coupon
    path('api/coupon', CouponViewSet.as_view(), name='coupon'),

    # bill
    path('api/bill/', bill_list_create_api, name="bill-list"),
    path('api/bill/<uuid:pk>/', bill_detail_api, name="bill-detail")
]
