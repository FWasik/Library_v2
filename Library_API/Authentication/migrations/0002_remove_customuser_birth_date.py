# Generated by Django 3.2.8 on 2021-10-12 14:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Authentication', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='birth_date',
        ),
    ]
