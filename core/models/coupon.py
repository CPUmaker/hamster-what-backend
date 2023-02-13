from django.db import models

from .coupon_category import CouponCategory
from .utils import UUIDModel


class Coupon (UUIDModel):
    store = models.CharField(max_length=100)
    merchant_homepage = models.URLField(max_length=200)
    offer_text = models.CharField(max_length=100)
    offer_value = models.CharField(max_length=100)
    title = models.CharField(max_length=200, default='')
    description = models.TextField(default='')
    code = models.CharField(max_length=50)
    smart_link = models.URLField(max_length=200)
    image_url = models.URLField(max_length=200)
    type = models.CharField(max_length=50)
    status = models.CharField(max_length=50)
    start_date = models.DateField('coupon valid date')
    expire_date = models.DateField('coupon expired date')
    categories = models.ManyToManyField(to=CouponCategory)

    def __str__(self) -> str:
        return self.coupon_text[:12] + '...'

