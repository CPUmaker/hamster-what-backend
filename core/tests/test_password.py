from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from knox.models import AuthToken

from core.models.profile import Profile


class PasswordTests(APITestCase):

    """
    Test suite for Password
    """
    def add_test_person(self, username, email, password):
        user = User.objects.create_user(username=username, email=email, password=password)
        return AuthToken.objects.create(user)

    def test_password_change_default(self):
        username = "xjhmlcy"
        email = "xjhmlcy123@gmail.com"
        old_password = "abcdefg123"
        new_password = "abcdefg123456"
        token, token_key = self.add_test_person(username, email, old_password)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token_key)

        url = "/api/change-password"
        data = {
            "old_password": old_password,
            "new_password": new_password
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = "/api/auth/login"
        data = {
            "username": email,
            "password": new_password
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_password_change_wrong_old_password(self):
        username = "xjhmlcy"
        email = "xjhmlcy123@gmail.com"
        old_password = "abcdefg123"
        new_password = "abcdefg123456"
        token, token_key = self.add_test_person(username, email, old_password)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token_key)

        url = "/api/change-password"
        data = {
            "old_password": old_password + "123",
            "new_password": new_password
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

