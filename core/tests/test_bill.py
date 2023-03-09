import requests
import unittest

# """ login user """

user = {
    "username": "superuser",
    "email": "",
    "password": "1"
}

auth_endpoint = "http://localhost:8001/api/auth/"

auth_response = requests.post(auth_endpoint, json = user)

if auth_response.status_code == 200:
    token = auth_response.json()["token"]

    headers = {'Authorization': f"Token {token}"}

    endpoint = "http://localhost:8001/api/bill/"

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


class BillTests(unittest.TestCase):

    def test_create(self):
        get_response_create_1 = requests.post(endpoint, json = data_1, headers=headers)
        get_response_create_2 = requests.post(endpoint, json = data_2, headers=headers)

        self.assertEqual(get_response_create_1.status_code, 201)
        self.assertEqual(get_response_create_2.status_code, 201)

    def test_get(self):
        get_response_list_1 = requests.get(endpoint, headers=headers)
        self.assertEqual(get_response_list_1.status_code, 200)
        # print(get_response_list_1.json())

    def test_detailed_get(self):
        endpoint = "http://localhost:8001/api/bill/d5b1886c-abff-44e3-b0a8-b26981d5cfe9/"
        get_response = requests.get(endpoint, headers=headers)
        print(get_response.json())
        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(get_response.json()["title"],data_1["title"])
        self.assertEqual(get_response.json()["price"],data_1["price"])
        self.assertEqual(get_response.json()["categories"],data_1["categories"])
        self.assertEqual(get_response.json()["comment"],data_1["comment"])

    def test_detailed_update(self):
        endpoint = "http://localhost:8001/api/bill/8bbf80af-12a0-4603-8270-79ad9feffda5/"
        data_updated = {
            "title": "buttersquash",
            "price": "0.01",
            "comment": "juicy",
            "categories": 4
        }
        get_response = requests.put(endpoint, data = data_updated, headers=headers)
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
        get_response = requests.put(endpoint, data = data_updated_2, headers=headers)
        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(get_response.json()["title"],data_updated_2["title"])
        self.assertEqual(get_response.json()["price"],data_updated_2["price"])
        self.assertEqual(get_response.json()["categories"],data_updated_2["categories"])
        self.assertEqual(get_response.json()["comment"],data_updated_2["comment"])


    # def test_delete(self):
    #     endpoint = "http://localhost:8001/api/bill/cb0e20c4-5344-4130-8a29-cbd50656fb48/"
    #     get_response = requests.delete(endpoint, headers=headers)
    #     print(get_response.json())
    #     self.assertEqual(get_response.status_code, 204)
    #     get_response = requests.get(endpoint, headers=headers)
    #     # data not exist
    #     self.assertEqual(get_response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
