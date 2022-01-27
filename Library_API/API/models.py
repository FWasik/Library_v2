from django.db import models
from django.conf import settings
from datetime import timedelta, date
from django.utils import timezone

from django.core.validators import RegexValidator


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
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, default='')
    last_name = models.CharField(max_length=100)

    def __str__(self):
        if self.middle_name:
            return self.first_name + ' ' + self.middle_name + ' ' + self.last_name

        else:
            return self.first_name + ' ' + self.last_name


class Book(models.Model):
    title = models.CharField(max_length=100)
    summary = models.TextField(max_length=1500, blank=True, default='')
    author = models.ManyToManyField(Author)
    amount = models.IntegerField(default=5)
    publisher = models.ForeignKey(Publisher, on_delete=models.SET_NULL, null=True)
    genre = models.ManyToManyField(Genre)
    number_of_pages = models.PositiveSmallIntegerField(default=0)
    year_of_release = models.PositiveSmallIntegerField(default=0)
    image = models.ImageField(upload_to='books/', default='')

    def __str__(self):
        return self.title


class Address(models.Model):
    street = models.CharField(max_length=100,
                              validators=[RegexValidator(
                                  regex='^[a-zA-ZŻŹĆĄŚĘŃŁÓżźćąśęńłó -]{1,100}$',
                                  message='Zły format ulicy: Tylko litery')])

    number_of_building = models.CharField(max_length=5,
                                          validators=[RegexValidator(
                                              regex='^[0-9]{1,5}$',
                                              message='Zły format nr. budynku: tylko cyfry XXXXX')])

    number_of_apartment = models.CharField(max_length=5, blank=True,
                                           validators=[RegexValidator(
                                               regex='^[0-9]{1,5}$',
                                               message='Zły format nr. lokalu: tylko cyfry XXXXX')])

    city = models.CharField(max_length=100,
                            validators=[RegexValidator(
                                regex='^[a-zA-ZŻŹĆĄŚĘŃŁÓżźćąśęńłó -]{1,100}$',
                                message='Zły format miasta: Tylko litery')])

    state = models.CharField(max_length=100,
                             validators=[RegexValidator(
                                 regex='^[a-zA-ZŻŹĆĄŚĘŃŁÓżźćąśęńłó -]{1,100}$',
                                 message='Zły format powiaty: Tylko litery')])
    zip_code = models.CharField(max_length=6,
                                validators=[RegexValidator(
                                    regex="^\d{2}-\d{3}$",
                                    message="Zły format kodu pocztowego: XX-XXX (cyfry)")])


class Order(models.Model):
    book = models.ManyToManyField(Book)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_order_create = models.DateTimeField(default=timezone.now, blank=True)
    date_delivery = models.DateField(default=date.today() + timedelta(days=2), blank=True)
    rental_end = models.DateField(default=date.today() + timedelta(days=30), blank=True)
    deliverer = models.ForeignKey(Deliverer, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f'Order number.' + str(self.id)
