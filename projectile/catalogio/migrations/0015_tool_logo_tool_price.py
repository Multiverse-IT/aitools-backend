# Generated by Django 4.2.5 on 2024-03-29 14:33

import catalogio.utils
from django.db import migrations, models
import versatileimagefield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('catalogio', '0014_tool_is_suggession'),
    ]

    operations = [
        migrations.AddField(
            model_name='tool',
            name='logo',
            field=versatileimagefield.fields.VersatileImageField(blank=True, null=True, upload_to=catalogio.utils.get_tools_media_path_prefix, verbose_name='Logo'),
        ),
        migrations.AddField(
            model_name='tool',
            name='price',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
