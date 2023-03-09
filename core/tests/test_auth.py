from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from knox.models import AuthToken

from core.models.profile import Profile


class AuthTests(APITestCase):

    """
    Test suite for Auth
    """
    def add_test_person(self, username, email, password):
        user = User.objects.create_user(username=username, email=email, password=password)
        return AuthToken.objects.create(user)

    def test_register_default(self):
        url = "/api/auth/register"
        data = {
            "username": "xjhmlcy",
            "email": "xjhmlcy@gmail.com",
            "password": "abcdefg123"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(Profile.objects.count(), 1)
        self.assertEqual(User.objects.get().username, data["username"])
        self.assertEqual(Profile.objects.get().user.email, data["email"])
        self.assertFalse(User.objects.get().is_active)
    
    def test_register_exist_email(self):
        url = "/api/auth/register"
        data1 = {
            "username": "xjhmlcy",
            "email": "xjhmlcy@gmail.com",
            "password": "abcdefg123"
        }
        data2 = {
            "username": "xjhmlcy_1",
            "email": "xjhmlcy@gmail.com",
            "password": "abcdefg123"
        }
        response = self.client.post(url, data1, format='json')
        response = self.client.post(url, data2, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(Profile.objects.count(), 1)
        self.assertEqual(User.objects.get().username, data1["username"])
        self.assertEqual(Profile.objects.get().user.email, data1["email"])
    
    def test_register_exist_username(self):
        url = "/api/auth/register"
        data1 = {
            "username": "xjhmlcy",
            "email": "xjhmlcy@gmail.com",
            "password": "abcdefg123"
        }
        data2 = {
            "username": "xjhmlcy",
            "email": "xjhmlcy123@gmail.com",
            "password": "abcdefg123"
        }
        response = self.client.post(url, data1, format='json')
        response = self.client.post(url, data2, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(Profile.objects.count(), 1)
        self.assertEqual(User.objects.get().username, data1["username"])
        self.assertEqual(Profile.objects.get().user.email, data1["email"])
    
    def test_login_default_by_username(self):
        username = "xjhmlcy"
        email = "xjhmlcy123@gmail.com"
        password = "abcdefg123"
        token, token_key = self.add_test_person(username, email, password)

        url = "/api/auth/login"
        data = {
            "username": username,
            "password": password
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data.get('user', None))
        self.assertEqual(response.data['user'].get('id', None), token.user.id)
        self.assertEqual(response.data['user'].get('username', None), token.user.username)
        self.assertEqual(response.data['user'].get('email', None), token.user.email)
    
    def test_login_default_by_email(self):
        username = "xjhmlcy"
        email = "xjhmlcy123@gmail.com"
        password = "abcdefg123"
        token, token_key = self.add_test_person(username, email, password)

        url = "/api/auth/login"
        data = {
            "username": email,
            "password": password
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data.get('user', None))
        self.assertEqual(response.data['user'].get('id', None), token.user.id)
        self.assertEqual(response.data['user'].get('username', None), token.user.username)
        self.assertEqual(response.data['user'].get('email', None), token.user.email)
    
    def test_login_wrong_password(self):
        username = "xjhmlcy"
        email = "xjhmlcy123@gmail.com"
        password = "abcdefg123"
        token, token_key = self.add_test_person(username, email, password)

        url = "/api/auth/login"
        data = {
            "username": email,
            "password": password + "456"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_login_no_username(self):
        url = "/api/auth/login"
        data = {
            "username": '123456',
            "password": "12345678"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
