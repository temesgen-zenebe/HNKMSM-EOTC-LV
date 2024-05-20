# Generated by Django 4.2 on 2024-05-15 05:28

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0004_sermoncategory_sermon_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='BaptizedCertification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('school_type', models.CharField(choices=[('youth', 'youth'), ('children', 'children')], max_length=100)),
                ('baptism_date', models.DateField()),
                ('christina_name', models.CharField(blank=True, max_length=100, null=True)),
                ('given_full_name', models.CharField(max_length=200)),
                ('fathers_full_name', models.CharField(max_length=200)),
                ('mothers_full_name', models.CharField(max_length=200)),
                ('phone_number', models.CharField(max_length=20)),
                ('child_country_of_birth', models.CharField(max_length=100)),
                ('christian_fathers_name', models.CharField(blank=True, max_length=100, null=True)),
                ('christian_fathers_or_mothers_name', models.CharField(blank=True, max_length=100, null=True)),
                ('priest_who_baptized', models.CharField(blank=True, max_length=100, null=True)),
                ('qualified', models.BooleanField(default=False)),
                ('service_request_confirmation_number', models.CharField(blank=True, max_length=100, null=True)),
                ('citification_request_confirmation_number', models.CharField(blank=True, max_length=100, null=True)),
                ('approved_by', models.CharField(blank=True, max_length=100, null=True)),
                ('slug', models.SlugField(blank=True, max_length=200, null=True, unique=True)),
                ('applied_data', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]