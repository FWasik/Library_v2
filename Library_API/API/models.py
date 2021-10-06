from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from datetime import timedelta, date
from django.utils import timezone


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Deliverer(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Publisher(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Author(models.Model):
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=50)

    def __str__(self):
        if self.middle_name:
            return self.first_name + ' ' + self.middle_name + ' ' + self.last_name

        else:
            return self.first_name + ' ' + self.last_name


class Book(models.Model):
    title = models.CharField(max_length=100)
    summary = models.TextField(max_length=1500, null=True, blank=True)
    author = models.ManyToManyField(Author)
    amount = models.IntegerField(default=5)
    publisher = models.ForeignKey(Publisher, on_delete=models.SET_NULL, blank=True, null=True)
    genre = models.ManyToManyField(Genre)
    number_of_pages = models.PositiveSmallIntegerField(default=0)
    year_of_release = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.title


class Address(models.Model):
    street = models.CharField(max_length=200)
    number_of_building = models.CharField(max_length=5)
    number_of_apartment = models.CharField(max_length=5, blank=True, null=True)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=6)


class Order(models.Model):
    book = models.ManyToManyField(Book)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_order_create = models.DateTimeField(default=timezone.now, blank=True)
    date_delivery = models.DateField(default=date.today() + timedelta(days=2), blank=True)
    rental_end = models.DateField(default=date.today() + timedelta(days=30), blank=True)
    deliverer = models.ForeignKey(Deliverer, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f'Order number.' + str(self.id)
