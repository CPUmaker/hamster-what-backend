from django.contrib.auth.models import User
from django.db import models

from .utils import UUIDModel


class SocialAccount(UUIDModel):
    identity = models.CharField(max_length=100, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.identity
