# Generated by Django 4.0.5 on 2022-08-14 17:00

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_premium_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=255)),
                ('rate', models.DecimalField(decimal_places=2, default=0, max_digits=9)),
                ('date', models.DateField(default=django.utils.timezone.now)),
            ],
        ),
    ]