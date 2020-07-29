from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.datetime_safe import datetime

# Create your models here.
class Visitor(models.Model):
    email = models.EmailField(max_length=40, unique=True)

    def __str__(self):
        return self.email

class Item(models.Model):
    name = models.CharField(max_length=20, null=False, blank=True)
    price = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
    icon = models.ImageField(default='user-profile.png')
    feature_01 = models.CharField(max_length=200)
    feature_02 = models.CharField(max_length=200)
    feature_03 = models.CharField(max_length=200)
    feature_04 = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Entry(models.Model):
    user = models.ForeignKey(Visitor, on_delete=models.CASCADE, null=False, blank=True)
    subscription_plan = models.ForeignKey(Item, on_delete=models.CASCADE, null=False, blank=True, default=None)
    start_date = models.DateTimeField(auto_now_add=True, null=True, blank=False)
    ordered_date = models.DateTimeField()
    total = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.user.email}'
