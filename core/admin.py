from django.contrib import admin

# Register your models here.
from core.models.bill import Bill

admin.site.register(Bill)
