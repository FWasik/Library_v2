# Generated by Django 3.2.8 on 2021-11-09 21:17

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0004_auto_20211103_0957'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='middle_name',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='order',
            name='date_delivery',
            field=models.DateField(blank=True, default=datetime.date(2021, 11, 11)),
        ),
        migrations.AlterField(
            model_name='order',
            name='rental_end',
            field=models.DateField(blank=True, default=datetime.date(2021, 12, 9)),
        ),
    ]
