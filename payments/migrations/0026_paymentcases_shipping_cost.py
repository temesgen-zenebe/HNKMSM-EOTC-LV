# Generated by Django 4.2 on 2025-01-06 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0025_order_shippinginformation_ordercase'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymentcases',
            name='shipping_cost',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
