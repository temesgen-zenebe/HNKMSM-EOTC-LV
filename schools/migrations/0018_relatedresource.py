# Generated by Django 4.2 on 2024-04-21 07:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('schools', '0017_remove_faqreader_is_satisfied_faq_is_satisfied'),
    ]

    operations = [
        migrations.CreateModel(
            name='RelatedResource',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('relatedResource_title', models.CharField(max_length=100)),
                ('links', models.TextField()),
                ('faq_relatedResource', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schools.faq')),
            ],
        ),
    ]