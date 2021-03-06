# Generated by Django 3.2.9 on 2021-11-23 11:22

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0013_auto_20211116_1715'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='image',
            field=models.ImageField(default='', upload_to='books/'),
        ),
        migrations.AlterField(
            model_name='order',
            name='date_delivery',
            field=models.DateField(blank=True, default=datetime.date(2021, 11, 25)),
        ),
        migrations.AlterField(
            model_name='order',
            name='rental_end',
            field=models.DateField(blank=True, default=datetime.date(2021, 12, 23)),
        ),
    ]
