# Generated by Django 4.0.5 on 2022-08-03 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0007_stock_currency_stock_exchange_stock_industry_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock',
            name='avg_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=9),
        ),
        migrations.AddField(
            model_name='stock',
            name='cur_value',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=9),
        ),
        migrations.AddField(
            model_name='stock',
            name='total_value',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=9),
        ),
    ]
