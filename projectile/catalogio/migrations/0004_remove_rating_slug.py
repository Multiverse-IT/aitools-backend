# Generated by Django 4.2.5 on 2023-11-22 05:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalogio', '0003_subcategory_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rating',
            name='slug',
        ),
    ]
