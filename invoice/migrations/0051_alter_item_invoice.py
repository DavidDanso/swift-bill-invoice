# Generated by Django 5.0 on 2024-03-06 03:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0050_alter_item_invoice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='invoice',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='items', to='invoice.invoice'),
        ),
    ]