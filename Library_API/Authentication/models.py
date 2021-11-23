from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator


class CustomUser(AbstractUser):
    middle_name = models.CharField(max_length=100, blank=True, default='')
    PESEL = models.CharField(max_length=11, default='', unique=True,
                             validators=[RegexValidator(regex="^[0-9]{11}$", message="Zły format PESELU: 11 cyfr!")])
    phone_number = models.CharField(max_length=9, unique=True,
                                    validators=[RegexValidator(regex="^[0-9]{9}$",
                                                               message="Zły format numeru telefonu: 9 cyfr!")])
    email = models.EmailField(max_length=50, unique=True,
                              validators=[RegexValidator(regex="^([-!#-\'*+\/-9=?A-Z^-~]{1,64}(\.[-!#-\'*+\/-9=?A-Z^-~]"
                                                               "{1,64})*|\"([]!#-[^-~ \t]|(\\[\t -~]))+\")"
                                                               "@[0-9A-Za-z]([0-9A-Za-z-]{0,61}[0-9A-Za-z])?"
                                                               "(\.[0-9A-Za-z]([0-9A-Za-z-]{0,61}[0-9A-Za-z])?)+$",
                                                         message="Zły format emailu: email@email")])
    image = models.ImageField(upload_to='profile_pics/', blank=True, default='default.jpg')


