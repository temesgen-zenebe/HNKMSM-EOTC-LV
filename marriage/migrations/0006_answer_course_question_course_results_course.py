# Generated by Django 4.2 on 2024-08-19 09:11

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('marriage', '0005_course_is_completed'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='course',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='marriage.course'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='question',
            name='course',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='marriage.course'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='results',
            name='course',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='marriage.course'),
            preserve_default=False,
        ),
    ]