# Generated by Django 4.0.5 on 2022-08-14 17:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_currency'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Currency',
        ),
    ]