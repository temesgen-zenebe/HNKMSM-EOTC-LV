# Generated by Django 4.2 on 2024-05-30 21:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_eventgallery_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='status_tag',
            field=models.CharField(default='active', max_length=200),
        ),
    ]
