# Generated by Django 4.0.5 on 2022-08-01 11:08

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_userprofile_api_requests_userprofile_companies'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='api_renewal',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
