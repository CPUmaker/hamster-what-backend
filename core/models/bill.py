from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from core.models.utils import UUIDModel
import datetime


class Bill(UUIDModel):

    user = models.ForeignKey(User, default=1, null=True, on_delete=models.SET_NULL)
    
    title = models.CharField(max_length = 120)
    
    date = models.DateField(verbose_name="payment time", default = datetime.date.today)

    datetime = models.DateTimeField(verbose_name="payment date & time", default = timezone.now)

    price = models.DecimalField(verbose_name='payment amount', max_digits=15, decimal_places=2, default=0.00)

    comment = models.TextField(verbose_name= "comment", blank = True, null = True, default=None)


    # need confirmation
    categories = (
        (1, "Food"),
        (2, "Groceries"),
        (3, "Transportation"),
        (4, "clothing"),
        (5, "Entertainment"),
        (6, "Bill"),
        (7, "Sports"),
        (8, "Electronics"),
        (9, "Travel"),
        (10, "House & Car"),
        (11, "Others")
    )


    categories = models.SmallIntegerField(verbose_name="bill categories", choices = categories, default=11)