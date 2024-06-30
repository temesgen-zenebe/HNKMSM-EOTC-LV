# Generated by Django 4.2 on 2024-06-24 09:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('payments', '0003_payment_payment_case'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentCaseLists',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('stripsPayment_link', models.URLField()),
                ('QRCodeImage', models.ImageField(blank=True, null=True, upload_to='payments/qrcodes/')),
                ('case_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('status', models.CharField(choices=[('active', 'Active'), ('inactive', 'Inactive')], max_length=50)),
                ('category', models.CharField(max_length=100)),
                ('type', models.CharField(choices=[('onetime', 'One-Time'), ('recurring', 'Recurring')], max_length=50)),
                ('image', models.ImageField(blank=True, null=True, upload_to='payments/case_images/')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('slug', models.SlugField(unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PaymentHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('paymentConfirmation', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payment_date', models.DateTimeField(auto_now_add=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('slug', models.SlugField(unique=True)),
                ('payment_case', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='payments.paymentcaselists')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
