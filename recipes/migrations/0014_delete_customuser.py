# Generated by Django 5.0.2 on 2024-02-14 20:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0013_customuser'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CustomUser',
        ),
    ]