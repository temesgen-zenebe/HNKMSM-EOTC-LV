# Generated by Django 4.2 on 2024-06-30 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0006_paymenthistory_payment_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymenthistory',
            name='slug',
            field=models.SlugField(blank=True, max_length=255, unique=True),
        ),
    ]
