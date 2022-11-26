# Generated by Django 4.0.5 on 2022-07-23 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_userprofile_currency_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Premium',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plan', models.CharField(default='Free', max_length=255)),
                ('company_limit', models.IntegerField()),
                ('api_limit', models.IntegerField()),
            ],
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='api_limit',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='company_limit',
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='premium_plan',
            field=models.IntegerField(),
        ),
    ]
