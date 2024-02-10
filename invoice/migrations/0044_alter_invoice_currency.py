# Generated by Django 5.0 on 2024-02-08 21:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0043_delete_pagerequest'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='currency',
            field=models.CharField(choices=[('USD', 'USD 🇺🇸'), ('GHS', 'GHS 🇬🇭'), ('GBP', 'GBP 🇬🇧'), ('EUR', 'EUR 🇪🇺'), ('NGN', 'NGN 🇳🇬')], max_length=200),
        ),
    ]
