from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models import Q
from core.models.utils import UUIDModel
import datetime
from datetime import date
from dateutil.relativedelta import relativedelta
# pip install python-dateutil


class BillSearchQuerySet(models.QuerySet):
    def searchCategories(self, query, user=None):
        lookup = Q(categories = query)
        qs = self.filter(lookup)
        if user is not None:
            qs = self.filter(user=user).filter(lookup)
        return qs
    
    def searchPrice(self, query, user=None):
        lookup = Q(price=query)
        qs = self.filter(lookup)
        if user is not None:
            qs = self.filter(user=user).filter(lookup)
        return qs
    
    def searchThisMonth(self, user=None):
        end_date = date.today()
        start_date = end_date + relativedelta(months=-1)
        lookup = Q(date__range = [start_date, end_date])
        qs = self.filter(lookup)
        if user is not None:
            qs = self.filter(user=user).filter(lookup)
        return qs

    def searchToday(self, user=None):
        end_date = date.today()
        start_date = end_date + relativedelta(days=-1)
        lookup = Q(date__range = [start_date, end_date])
        qs = self.filter(lookup)
        if user is not None:
            qs = self.filter(user=user).filter(lookup)
        return qs
    
    # def searchTitle(self, keyword, user=None):
    #     lookup = Q(title__contains = keyword)
    #     qs = self.filter(lookup)
    #     if user is not None:
    #         qs = self.filter(user=user).filter(lookup)
    #     return qs
    

    # def categorieAmount(self, date, categories, user=None):
    #     if date == "day":
    #         qs = self.searchCategories(categories, user=user).searchToday(user=user)
    #     elif date == "month":
    #         qs = self.searchCategories(categories, user=user).searchThisMonth(user=user)

class BillManager(models.Manager):

    def get_queryset(self, *args, **kwargs):
        return BillSearchQuerySet(self.model, using = self._db)

class Bill(UUIDModel):

    user = models.ForeignKey(User, default=1, null=True, on_delete=models.SET_NULL)
    
    # title = models.CharField(max_length = 120)
    
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

    wallet = (
        (1, "checking account"),
        (2, "credit account"),
        (3, "cash"),
        (4, "savings account"),
        (5, "other")
    )

    wallet = models.SmallIntegerField(verbose_name="wallet", choices=wallet, default=3)