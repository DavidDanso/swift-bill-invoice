# Generated by Django 5.0 on 2024-02-04 16:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0039_alter_item_invoice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='invoice',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='invoice.invoice'),
        ),
    ]
