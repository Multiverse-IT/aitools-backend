# Generated by Django 4.2.5 on 2024-03-28 13:47

import dirtyfields.dirtyfields
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('contentio', '0010_remove_post_is_indexed_post_is_noindex'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sponsor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('field', models.JSONField(default=list)),
            ],
            options={
                'ordering': ('-created_at',),
                'abstract': False,
            },
            bases=(dirtyfields.dirtyfields.DirtyFieldsMixin, models.Model),
        ),
    ]
