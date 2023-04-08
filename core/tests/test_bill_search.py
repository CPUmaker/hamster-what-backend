from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from knox.models import AuthToken

from core.models.bill import Bill

from datetime import date

endpoint = "/api/bill/"

data_1 = {
    "wallet": 3,
    "price": "0.85",
    "comment": "discount",
    "categories": 8
}

data_2 = {
    "wallet": 1,
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

    def test_categories_search(self):

        endpoint = "/api/bill/"

        get_response_create_1 = self.client.post(endpoint, data_1, format='json')
        get_response_create_2 = self.client.post(endpoint, data_2, format='json')

        self.assertEqual(get_response_create_1.status_code, 201)
        self.assertEqual(get_response_create_2.status_code, 201)

        endpoint = "/api/bill/search/?item=categories&keyword=8"

        get_response = self.client.get(endpoint)
        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(get_response.json()[0]["wallet"],data_1["wallet"])
        self.assertEqual(get_response.json()[0]["price"],data_1["price"])
        self.assertEqual(get_response.json()[0]["categories"],data_1["categories"])
        self.assertEqual(get_response.json()[0]["comment"],data_1["comment"])



        endpoint = "/api/bill/search/?item=categories&keyword=2"

        get_response = self.client.get(endpoint)
        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(get_response.json()[0]["wallet"],data_2["wallet"])
        self.assertEqual(get_response.json()[0]["price"],data_2["price"])
        self.assertEqual(get_response.json()[0]["categories"],data_2["categories"])
        self.assertEqual(get_response.json()[0]["comment"],data_2["comment"])


    def test_price_search(self):

        endpoint = "/api/bill/"

        get_response_create_1 = self.client.post(endpoint, data_1, format='json')
        get_response_create_2 = self.client.post(endpoint, data_2, format='json')

        self.assertEqual(get_response_create_1.status_code, 201)
        self.assertEqual(get_response_create_2.status_code, 201)

        endpoint = "/api/bill/search/?item=price&keyword=0.85"

        get_response = self.client.get(endpoint)
        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(get_response.json()[0]["wallet"],data_1["wallet"])
        self.assertEqual(get_response.json()[0]["price"],data_1["price"])
        self.assertEqual(get_response.json()[0]["categories"],data_1["categories"])
        self.assertEqual(get_response.json()[0]["comment"],data_1["comment"])



        endpoint = "/api/bill/search/?item=price&keyword=99.65"

        get_response = self.client.get(endpoint)
        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(get_response.json()[0]["wallet"],data_2["wallet"])
        self.assertEqual(get_response.json()[0]["price"],data_2["price"])
        self.assertEqual(get_response.json()[0]["categories"],data_2["categories"])
        self.assertEqual(get_response.json()[0]["comment"],data_2["comment"])


    def test_date_search(self):

        # date: today
        data_1 = {
            "wallet": 3,
            "price": "0.85",
            "comment": "discount",
            "categories": 8,
        }

        # date: this month
        data_2 = {
            "wallet": 1,
            "price": "99.65",
            "comment": "None",
            "categories": 2,
            "date": date( date.today().year, date.today().month, 2)
        }

        # date: this year
        data_3 = {
            "wallet": 2,
            "price": "8.88",
            "comment": "",
            "categories": 1,
            "date": date( date.today().year, 2, date.today().day)
        }

        endpoint = "/api/bill/"

        get_response_create_1 = self.client.post(endpoint, data_3, format='json')

        self.assertEqual(get_response_create_1.status_code, 201)

        endpoint = "/api/bill/search/?item=date&keyword=year"

        get_response = self.client.get(endpoint)
        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(get_response.json()[0]["wallet"],data_3["wallet"])
        self.assertEqual(get_response.json()[0]["price"],data_3["price"])
        self.assertEqual(get_response.json()[0]["categories"],data_3["categories"])
        self.assertEqual(get_response.json()[0]["comment"],data_3["comment"])


        endpoint = "/api/bill/"

        get_response_create_2 = self.client.post(endpoint, data_2, format='json')

        self.assertEqual(get_response_create_2.status_code, 201)

        endpoint = "/api/bill/search/?item=date&keyword=month"

        get_response = self.client.get(endpoint)
        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(get_response.json()[0]["wallet"],data_2["wallet"])
        self.assertEqual(get_response.json()[0]["price"],data_2["price"])
        self.assertEqual(get_response.json()[0]["categories"],data_2["categories"])
        self.assertEqual(get_response.json()[0]["comment"],data_2["comment"])


        endpoint = "/api/bill/"

        get_response_create_3 = self.client.post(endpoint, data_1, format='json')

        self.assertEqual(get_response_create_3.status_code, 201)

        endpoint = "/api/bill/search/?item=date&keyword=day"

        get_response = self.client.get(endpoint)
        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(get_response.json()[0]["wallet"],data_1["wallet"])
        self.assertEqual(get_response.json()[0]["price"],data_1["price"])
        self.assertEqual(get_response.json()[0]["categories"],data_1["categories"])
        self.assertEqual(get_response.json()[0]["comment"],data_1["comment"])
