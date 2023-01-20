from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from rest_framework import status

from .models.profile import Profile


class ProfileTestCase(APITestCase):

    """
    Test suite for Contact
    """
    def setUp(self):
        self.client = APIClient()
        self.data = {
            "username": "xjhmlcy",
            "email": "xjhmlcy@gmail.com",
            "password": "abcdefg123"
        }
        self.url = "/api/auth/register"

    def test_create_contact(self):
        '''
        test ContactViewSet create method
        '''
        data = self.data
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(Profile.objects.count(), 1)
        self.assertEqual(User.objects.get().username, "xjhmlcy")
        self.assertEqual(Profile.objects.get().user.email, "xjhmlcy@gmail.com")
