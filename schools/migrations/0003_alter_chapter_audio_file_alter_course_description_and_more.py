# Generated by Django 4.2 on 2024-04-04 19:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('schools', '0002_chapter_audio_file_chapter_video_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chapter',
            name='audio_file',
            field=models.FileField(blank=True, null=True, upload_to='audio'),
        ),
        migrations.AlterField(
            model_name='course',
            name='description',
            field=models.TextField(blank=True, max_length=500, null=True),
        ),
        migrations.CreateModel(
            name='Resources',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Resources_title', models.CharField(max_length=100)),
                ('links', models.TextField()),
                ('chapter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schools.chapter')),
            ],
        ),
    ]