# Generated by Django 4.2 on 2024-04-14 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schools', '0009_quationsandanswer'),
    ]

    operations = [
        migrations.AddField(
            model_name='quationsandanswer',
            name='is_answered',
            field=models.BooleanField(default=False),
        ),
    ]