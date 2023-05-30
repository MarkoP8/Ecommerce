from django.db import models
from django.utils import timezone
from django.conf import settings
from store.models.user import User
from store.models.order import Order


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, null=True)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=100, null=False, default=False)
    street_address = models.CharField(max_length=100)
    card_name = models.CharField(max_length=100, null=True)
    credit_card = models.IntegerField(null=True)
    exp_month = models.IntegerField(null=True)
    exp_year = models.IntegerField(null=True)
    cvv = models.IntegerField(null=True)
    
    def __str__(self):
        return f"{self.user} - {self.country} ({self.city})"