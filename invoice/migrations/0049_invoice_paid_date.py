# Generated by Django 5.0 on 2024-02-19 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0048_alter_item_invoice'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='paid_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
