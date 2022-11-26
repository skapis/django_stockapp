# Generated by Django 4.0.5 on 2022-07-11 18:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0001_initial'),
        ('transactions', '0004_transaction_shares'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='stock_id',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='stocks.stock'),
        ),
    ]
