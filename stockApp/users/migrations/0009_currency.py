# Generated by Django 4.0.5 on 2022-08-14 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_delete_currency'),
    ]

    operations = [
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
            ],
        ),
    ]
