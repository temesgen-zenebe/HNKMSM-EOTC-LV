# Generated by Django 4.2 on 2024-12-12 09:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0010_alter_paymentcaselists_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentcasecartlist',
            name='payment_case',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='payments.paymentcaselists'),
        ),
    ]
