from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from knox.models import AuthToken

from core.models.profile import Profile


class ProfileTests(APITestCase):

    """
    Test suite for Profile
    """
    def add_test_person(self):
        user = User(username='xjhmlcy', email='xjhmlcy@gmail.com', password='abcdefg123')
        user.save()
        return AuthToken.objects.create(user)

    def test_retrive_profile(self):
        token, token_key = self.add_test_person()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token_key)

        url = "http://localhost:8000/api/profile"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data.get('user', None))
        self.assertEqual(response.data['user'].get('username'), token.user.username)
        self.assertEqual(response.data['user'].get('email'), token.user.email)
        self.assertEqual(response.data.get('bio'), '')
        self.assertEqual(response.data.get('birthday'), None)
        self.assertEqual(response.data.get('country'), '')
        self.assertEqual(response.data.get('city'), '')
        self.assertEqual(response.data.get('affiliation'), '')
        self.assertEqual(response.data.get('photo'), 'http://testserver/media/https%3A/static.productionready.io/images/smiley-cyrus.jpg')
    
    def test_update_profile(self):
        token, token_key = self.add_test_person()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token_key)

        url = "http://localhost:8000/api/profile"
        data = {
            'bio': 'Hello, world!',
            'birthday': '2000-03-09',
            'country': 'CA',
            'city': 'Waterloo',
            'affiliation': 'University of Waterloo'
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data.get('user', None))
        self.assertEqual(response.data['user'].get('username'), token.user.username)
        self.assertEqual(response.data['user'].get('email'), token.user.email)
        self.assertEqual(response.data.get('bio'), data['bio'])
        self.assertEqual(response.data.get('birthday'), str(data['birthday']))
        self.assertEqual(response.data.get('country'), data['country'])
        self.assertEqual(response.data.get('city'), data['city'])
        self.assertEqual(response.data.get('affiliation'), data['affiliation'])
        self.assertEqual(response.data.get('photo'), 'http://testserver/media/https%3A/static.productionready.io/images/smiley-cyrus.jpg')

    def test_update_username(self):
        token, token_key = self.add_test_person()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token_key)

        url = "http://localhost:8000/api/profile"
        data = {
            'user': {
                'username': 'apple'
            }
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(User.objects.get(username=data['user']['username']))
        self.assertIsNotNone(response.data.get('user', None))
        self.assertEqual(response.data['user'].get('username', None), data['user']['username'])

    def test_update_email(self):
        token, token_key = self.add_test_person()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token_key)

        url = "http://localhost:8000/api/profile"
        data = {
            'user': {
                'email': 'apple@gmail.com'
            }
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(User.objects.get(email=data['user']['email']))
        self.assertFalse(User.objects.get(email=data['user']['email']).is_active)
        self.assertIsNotNone(response.data.get('user', None))
        self.assertEqual(response.data['user'].get('email', None), data['user']['email'])
