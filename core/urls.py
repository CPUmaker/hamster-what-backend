from django.urls import path, include
from knox import views as knox_views
from rest_framework import routers

from core.api.auth import RegisterAPI, LoginAPI, AppleLogin, GoogleLogin, FacebookLogin, validate_token, DeleteAccountAPI, verify_user_and_activate
from core.api.password import ChangePasswordView
from core.api.profile import ProfileViewSet
from core.api.coupon import CouponViewSet
from core.api.bill import *
from core.api.billSearch import SearchBillListView
from core.api.billPriceSum import BillSumPriceListViewAPI

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
    path('api/auth/delete-account', DeleteAccountAPI.as_view(), name='delete-account'),
    # passwd
    path('api/change-password', ChangePasswordView.as_view(), name='change-password'),
    path('api/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    # profile
    path('api/profile', ProfileViewSet.as_view(), name='profile'),
    # coupon
    path('api/coupon', CouponViewSet.as_view(), name='coupon'),

    # bill
    path('api/bill/', bill_list_create_api, name="bill-list"),
    path('api/bill/<uuid:pk>/', bill_detail_api, name="bill-detail"),

    # bill search
    path('api/bill/search/', SearchBillListView.as_view(), name="bill-search"),

    # bill price list searched by categories
    path('api/bill/price-sum/', BillSumPriceListViewAPI, name="bill-price-sum")
]


from rest_framework.authtoken.views import obtain_auth_token
urlpatterns += [
    path('api/auth/', obtain_auth_token)
]
