from django.urls import path, include
from knox import views as knox_views

from core.api.auth import RegisterAPI, LoginAPI
from core.api.password import ChangePasswordView


urlpatterns = [
    path('api/auth/register', RegisterAPI.as_view(), name='register'),
    path('api/auth/login', LoginAPI.as_view(), name='login'),
    path('api/auth/logout', knox_views.LogoutView.as_view(), name='logout'),
    path('api/change-password', ChangePasswordView.as_view(), name='change-password'),
    path('api/password_reset', include('django_rest_passwordreset.urls', namespace='password_reset')),
]
