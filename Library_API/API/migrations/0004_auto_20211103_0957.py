# Generated by Django 3.2.8 on 2021-11-03 08:57

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0003_alter_order_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='date_delivery',
            field=models.DateField(blank=True, default=datetime.date(2021, 11, 5)),
        ),
        migrations.AlterField(
            model_name='order',
            name='rental_end',
            field=models.DateField(blank=True, default=datetime.date(2021, 12, 3)),
        ),
    ]
