# Generated by Django 4.2 on 2024-06-10 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('multimedia', '0012_spiritualpoemsong_pdf_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='spiritualpoemsong',
            name='language',
            field=models.CharField(choices=[('English', 'English'), ('Amharic', 'Amharic'), ('Other', 'Other')], default='en', max_length=20),
        ),
    ]