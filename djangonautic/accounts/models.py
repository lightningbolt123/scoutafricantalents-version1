from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.
class CustomUser(AbstractUser):
    bio = models.CharField(max_length=200, blank=True)
    picture = models.ImageField(default='user-profile.png', upload_to='profile-picture/')
    phone_number = PhoneNumberField(null=False, blank=True)
    gender = models.CharField(max_length=1, blank=False)
    date_of_birth = models.DateField(null=True, blank=False)
    country_of_birth = models.CharField(max_length=20)

    def __str__(self):
        return self.username