# Generated by Django 4.0.5 on 2022-07-14 18:35

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0002_stock_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock',
            name='price_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
