# Generated by Django 4.2 on 2024-06-11 01:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('multimedia', '0013_alter_spiritualpoemsong_language'),
    ]

    operations = [
        migrations.AddField(
            model_name='praiseglory',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='multimedia/praiseGlory/'),
        ),
    ]