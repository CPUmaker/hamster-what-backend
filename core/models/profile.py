from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django_countries.fields import CountryField
from django_extensions.db.models import TimeStampedModel

from .utils import UUIDModel


class Profile(TimeStampedModel, UUIDModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    birthday = models.DateField(verbose_name="Birthday", null=True)
    country = CountryField(null=True, verbose_name="Country")
    city = models.CharField(max_length=100, verbose_name="City in English")
    affiliation = models.CharField(
        max_length=100, verbose_name="Name of your organization in English",
    )
    photo = models.ImageField(upload_to='media/', max_length=100000, null=True, blank=True, default="https://static.productionready.io/images/smiley-cyrus.jpg")

    def __str__(self):
        return self.user.username
