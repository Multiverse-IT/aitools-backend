# Generated by Django 4.2.5 on 2023-12-11 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contentio', '0003_post_short_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='view_count',
            field=models.PositiveBigIntegerField(default=0),
        ),
    ]
