# Generated by Django 4.2 on 2023-05-09 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projectVote', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectproposal',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='project/%Y/%m/%d'),
        ),
    ]
