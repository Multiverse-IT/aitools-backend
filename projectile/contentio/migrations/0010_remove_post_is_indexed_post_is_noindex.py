# Generated by Django 4.2.5 on 2024-01-23 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contentio', '0009_redirect'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='is_indexed',
        ),
        migrations.AddField(
            model_name='post',
            name='is_noindex',
            field=models.BooleanField(default=False),
        ),
    ]