# Generated by Django 4.2 on 2024-09-06 01:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0008_alter_paymenthistory_payment_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymentcaselists',
            name='Instraction',
            field=models.TextField(default='If you need guidance on how to make a payment, please contact the office for assistance.'),
        ),
        migrations.AlterField(
            model_name='paymentcaselists',
            name='category',
            field=models.CharField(choices=[('service', 'service'), ('donation', 'donation'), ('marriageSchoolRegFee', 'marriageSchoolRegFee'), ('abentChildrenRegFee', 'abentChildrenRegFee'), ('abentYouthRegFee', 'abentYouthRegFee'), ('churchProjectSupportFree', 'churchProjectSupportFree')], default='service', max_length=100),
        ),
    ]
