from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    PESEL = models.CharField(max_length=11)
    phone_number = models.CharField(max_length=9)


