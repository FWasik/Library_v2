from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)



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
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    amount = models.IntegerField(default=5)

    def __str__(self):
        return self.title


class Order(models.Model):
    book = models.ManyToManyField(Book)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

