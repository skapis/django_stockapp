# Generated by Django 4.0.5 on 2022-07-09 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0003_alter_transaction_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='shares',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=9),
        ),
    ]
