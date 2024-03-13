# Generated by Django 5.0 on 2024-03-06 03:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0049_invoice_paid_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='invoice',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='items', to='invoice.invoice'),
        ),
    ]