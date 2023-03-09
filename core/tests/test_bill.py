from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from knox.models import AuthToken

from core.models.bill import Bill

endpoint = "/api/bill/"

data_1 = {
    "title": "water",
    "price": "0.85",
    "comment": "discount",
    "categories": 8
}

data_2 = {
    "title": "mattress",
    "price": "99.65",
    "comment": "None",
    "categories": 2
}


class BillTests(APITestCase):
    def setUp(self):
        username = "xjhmlcy"
        email = "xjhmlcy123@gmail.com"
        password = "abcdefg123"
        user = User.objects.create_user(username=username, email=email, password=password)
        token, token_key = AuthToken.objects.create(user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token_key)

    def test_create(self):
        get_response_create_1 = self.client.post(endpoint, data_1, format='json')
        get_response_create_2 = self.client.post(endpoint, data_2, format='json')

        self.assertEqual(get_response_create_1.status_code, 201)
        self.assertEqual(get_response_create_2.status_code, 201)
        # print(get_response_create_1.data)

    def test_get(self):
        endpoint = "/api/bill/"
        self.client.post(endpoint, data_1, format='json')
        self.client.post(endpoint, data_2, format='json')

        get_response_list_1 = self.client.get(endpoint)
        self.assertEqual(get_response_list_1.status_code, 200)
        # print(get_response_list_1.json())

    def test_detailed_get(self):
        endpoint = "/api/bill/"
        self.client.post(endpoint, data_1, format='json')
        self.client.post(endpoint, data_2, format='json')

        endpoint = f"/api/bill/{Bill.objects.all()[0].id}/"
        get_response = self.client.get(endpoint)
        # print(get_response.json())
        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(get_response.json()["title"],data_1["title"])
        self.assertEqual(get_response.json()["price"],data_1["price"])
        self.assertEqual(get_response.json()["categories"],data_1["categories"])
        self.assertEqual(get_response.json()["comment"],data_1["comment"])

    def test_detailed_update(self):
        endpoint = "/api/bill/"
        self.client.post(endpoint, data_1, format='json')
        self.client.post(endpoint, data_2, format='json')

        endpoint = f"/api/bill/{Bill.objects.all()[0].id}/"
        data_updated = {
            "title": "buttersquash",
            "price": "0.01",
            "comment": "juicy",
            "categories": 4
        }
        get_response = self.client.put(endpoint, data_updated, format='json')
        # print(get_response.json())
        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(get_response.json()["title"],data_updated["title"])
        self.assertEqual(get_response.json()["price"],data_updated["price"])
        self.assertEqual(get_response.json()["categories"],data_updated["categories"])
        self.assertEqual(get_response.json()["comment"],data_updated["comment"])

        ## partial update
        data_updated_2 = {
            "title": "buttersquash",
            "price": "56.60",
            "comment": "juicy",
            "categories": 4
        }
        get_response = self.client.put(endpoint, data_updated_2, format='json')
        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(get_response.json()["title"],data_updated_2["title"])
        self.assertEqual(get_response.json()["price"],data_updated_2["price"])
        self.assertEqual(get_response.json()["categories"],data_updated_2["categories"])
        self.assertEqual(get_response.json()["comment"],data_updated_2["comment"])
