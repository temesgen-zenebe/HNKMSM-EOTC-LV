# Generated by Django 4.2 on 2024-05-15 07:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0006_rename_school_type_baptizedcertification_baptize_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='baptizedcertification',
            name='christian_fathers_name',
        ),
    ]
