# Generated by Django 4.2 on 2024-06-06 18:28

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('multimedia', '0007_bookslibrary_votecount'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookslibrary',
            name='voters',
            field=models.ManyToManyField(blank=True, related_name='voted_books', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='bookslibrary',
            name='voteCount',
            field=models.PositiveIntegerField(default=0),
        ),
    ]