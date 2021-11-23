# Generated by Django 3.2.8 on 2021-11-16 16:02

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0011_auto_20211116_1659'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='city',
            field=models.CharField(max_length=50, validators=[django.core.validators.RegexValidator(message='Zły format miasta: Tylko litery', regex='^[a-zA-ZŻŹĆĄŚĘŃŁÓżźćąśęńłó ]{1,50}$')]),
        ),
        migrations.AlterField(
            model_name='address',
            name='state',
            field=models.CharField(max_length=50, validators=[django.core.validators.RegexValidator(message='Zły format powiaty: Tylko litery', regex='^[a-zA-ZŻŹĆĄŚĘŃŁÓżźćąśęńłó ]{1,50}$')]),
        ),
        migrations.AlterField(
            model_name='address',
            name='street',
            field=models.CharField(max_length=200, validators=[django.core.validators.RegexValidator(message='Zły format ulicy: Tylko litery', regex='^[a-zA-ZŻŹĆĄŚĘŃŁÓżźćąśęńłó ]{1,200}$')]),
        ),
    ]