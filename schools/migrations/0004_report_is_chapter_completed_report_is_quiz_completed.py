# Generated by Django 4.2 on 2024-04-08 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schools', '0003_alter_chapter_audio_file_alter_course_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='is_chapter_completed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='report',
            name='is_quiz_completed',
            field=models.BooleanField(default=False),
        ),
    ]
