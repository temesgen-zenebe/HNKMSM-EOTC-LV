# Generated by Django 4.2 on 2024-04-09 05:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('schools', '0004_report_is_chapter_completed_report_is_quiz_completed'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='report',
            name='is_chapter_completed',
        ),
        migrations.RemoveField(
            model_name='report',
            name='is_quiz_completed',
        ),
        migrations.CreateModel(
            name='Progress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_chapter_completed', models.BooleanField(default=False)),
                ('is_quiz_completed', models.BooleanField(default=False)),
                ('slug', models.SlugField(unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schools.course')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
