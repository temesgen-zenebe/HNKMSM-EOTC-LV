# Generated by Django 4.2 on 2025-01-09 20:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0026_paymentcases_shipping_cost'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordercase',
            name='shipping_information',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='order_cases', to='payments.shippinginformation'),
        ),
    ]
