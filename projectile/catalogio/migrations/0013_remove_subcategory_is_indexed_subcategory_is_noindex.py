# Generated by Django 4.2.5 on 2024-01-23 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogio', '0012_tool_verified_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subcategory',
            name='is_indexed',
        ),
        migrations.AddField(
            model_name='subcategory',
            name='is_noindex',
            field=models.BooleanField(default=False),
        ),
    ]