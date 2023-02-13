from django.db import models

from .utils import UUIDModel


class CouponCategory(UUIDModel):
    category = models.CharField(max_length=50)
    sub_category = models.CharField(max_length=50)

    def __str__(self) -> str:
        return f'<CouponCategory: {self.category}-{self.sub_category}>'
