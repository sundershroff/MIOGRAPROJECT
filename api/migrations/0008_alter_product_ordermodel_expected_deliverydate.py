# Generated by Django 5.0 on 2024-06-15 07:42

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_alter_product_ordermodel_expected_deliverydate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product_ordermodel',
            name='expected_deliverydate',
            field=models.DateField(default=datetime.date(2024, 6, 22), null=True),
        ),
    ]
