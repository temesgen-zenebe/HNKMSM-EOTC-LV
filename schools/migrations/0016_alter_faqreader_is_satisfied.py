# Generated by Django 4.2 on 2024-04-19 19:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schools', '0015_remove_faq_satisfaction_rating_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='faqreader',
            name='is_satisfied',
            field=models.BooleanField(default=False),
        ),
    ]