# Generated by Django 4.0.5 on 2022-07-19 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0005_transaction_stock_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='stock_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=9),
        ),
    ]
