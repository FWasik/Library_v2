# Generated by Django 3.2.6 on 2021-08-21 14:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0003_book_number_of_books'),
    ]

    operations = [
        migrations.RenameField(
            model_name='book',
            old_name='number_of_books',
            new_name='amount',
        ),
    ]
