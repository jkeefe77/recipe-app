# Generated by Django 4.2.6 on 2023-10-31 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='image',
            field=models.ImageField(default='no_picture.jpg', upload_to='customers'),
        ),
    ]
