# Generated by Django 3.2.6 on 2021-08-24 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0007_auto_20210823_1750'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='author',
        ),
        migrations.AddField(
            model_name='book',
            name='author',
            field=models.ManyToManyField(to='API.Author'),
        ),
    ]