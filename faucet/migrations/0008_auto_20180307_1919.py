# Generated by Django 2.0.2 on 2018-03-07 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('faucet', '0007_auto_20180307_1839'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lecture',
            name='account',
            field=models.CharField(max_length=255, unique=True, verbose_name='Имя аккаунта'),
        ),
    ]