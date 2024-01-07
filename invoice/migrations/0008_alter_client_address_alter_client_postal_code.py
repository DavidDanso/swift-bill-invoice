# Generated by Django 5.0 on 2023-12-20 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0007_alter_client_address_alter_client_postal_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='address',
            field=models.CharField(default='456 Elm Avenue, Townsville, Province, 56789, Canada', max_length=255),
        ),
        migrations.AlterField(
            model_name='client',
            name='postal_code',
            field=models.CharField(default='G2J0B5', max_length=30),
        ),
    ]
