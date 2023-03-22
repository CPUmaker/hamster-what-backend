from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from knox.models import AuthToken

from core.models.coupon import Coupon, CouponCategory


class CouponTests(APITestCase):

    """
    Test suite for Coupon
    """
    def add_test_person(self, username, email, password):
        user = User.objects.create_user(username=username, email=email, password=password)
        return AuthToken.objects.create(user)

    def add_test_coupon(self):
        coupon_category = CouponCategory.objects.create(category='sports', sub_category='sneakers')
        coupon = Coupon.objects.create(store='Apple', start_date='2022-12-31', expire_date='2023-12-31')
        coupon.categories.add(coupon_category)
        coupon.save()

    def test_register_default(self):
        username = "xjhmlcy"
        email = "xjhmlcy123@gmail.com"
        password = "abcdefg123"
        token, token_key = self.add_test_person(username, email, password)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token_key)

        self.add_test_coupon()

        url = "/api/coupon"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Coupon.objects.count(), 1)
        self.assertEqual(CouponCategory.objects.count(), 1)
        self.assertEqual(response.data[0].get('store', None), 'Apple')
