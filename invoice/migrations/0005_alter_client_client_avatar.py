# Generated by Django 5.0 on 2023-12-19 03:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0004_alter_client_client_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='client_avatar',
            field=models.ImageField(default='emil-kowalski.png', upload_to='client_avatar/'),
        ),
    ]
