# Generated by Django 4.0.5 on 2022-07-15 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0004_stock_logo'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock',
            name='sector',
            field=models.CharField(default='none', max_length=255),
        ),
    ]
