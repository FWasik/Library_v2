# Generated by Django 3.2.9 on 2021-11-23 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Authentication', '0009_alter_customuser_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='image',
            field=models.ImageField(default='default.jpg', upload_to='profile_pics/'),
        ),
    ]