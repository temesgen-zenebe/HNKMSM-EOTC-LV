# Generated by Django 4.2 on 2024-06-04 05:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ArchiveLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('url', models.URLField()),
                ('description', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('slug', models.SlugField(blank=True, max_length=200, null=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Gallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('media_type', models.CharField(choices=[('Photo', 'Photo'), ('Video', 'Video')], max_length=100)),
                ('file', models.FileField(upload_to='multimedia/gallery/')),
                ('description', models.TextField(blank=True, null=True)),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('slug', models.SlugField(blank=True, max_length=200, null=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserManual',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('version', models.CharField(max_length=20)),
                ('usage_description', models.TextField(blank=True, default=300, null=True)),
                ('file', models.FileField(upload_to='multimedia/userManuals/')),
                ('published_date', models.DateField(blank=True, null=True)),
                ('published_by', models.DateField(blank=True, null=True)),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('slug', models.SlugField(blank=True, max_length=200, null=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='TestimonyOfSalvation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('testimony', models.TextField(blank=True, max_length=1000, null=True)),
                ('link', models.URLField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('slug', models.SlugField(blank=True, max_length=200, null=True, unique=True)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PraiseGlory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('content', models.TextField(blank=True, default=1000, null=True)),
                ('link', models.URLField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('slug', models.SlugField(blank=True, max_length=200, null=True, unique=True)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BooksLibrary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('author', models.CharField(max_length=200)),
                ('published_date', models.DateField()),
                ('format_type', models.CharField(choices=[('audio', 'audio'), ('text', 'text')], max_length=50)),
                ('isbn', models.CharField(blank=True, max_length=13, null=True, unique=True)),
                ('web_link', models.URLField(blank=True, null=True)),
                ('summary', models.TextField(blank=True, max_length=300, null=True)),
                ('cover_image', models.ImageField(blank=True, null=True, upload_to='multimedia/book_covers/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('slug', models.SlugField(blank=True, max_length=200, null=True, unique=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
