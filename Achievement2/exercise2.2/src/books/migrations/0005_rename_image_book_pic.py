# Generated by Django 4.2.6 on 2023-11-01 15:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0004_alter_book_book_type_alter_book_genre'),
    ]

    operations = [
        migrations.RenameField(
            model_name='book',
            old_name='image',
            new_name='pic',
        ),
    ]
