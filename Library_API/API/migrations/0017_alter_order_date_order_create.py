# Generated by Django 3.2.9 on 2021-11-29 15:28

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0016_alter_order_date_order_create'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='date_order_create',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now),
        ),
    ]
