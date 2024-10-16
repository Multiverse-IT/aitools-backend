# Generated by Django 4.2.5 on 2024-05-11 07:31

import autoslug.fields
import contentio.utils
import dirtyfields.dirtyfields
from django.db import migrations, models
import uuid
import versatileimagefield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CommonStorage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('storage', models.JSONField(default=list)),
                ('home_page', models.JSONField(default=list)),
                ('categories_page', models.JSONField(default=list)),
                ('blogs_page', models.JSONField(default=list)),
                ('about_page', models.JSONField(default=list)),
                ('redirects', models.JSONField(default=list)),
            ],
            options={
                'ordering': ('-created_at',),
                'abstract': False,
            },
            bases=(dirtyfields.dirtyfields.DirtyFieldsMixin, models.Model),
        ),
        migrations.CreateModel(
            name='FAQ',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=200)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from=contentio.utils.get_post_slug, unique=True)),
                ('summary', models.TextField(blank=True)),
                ('priority', models.IntegerField(default=0, help_text='Higher number is higher priority.')),
            ],
            options={
                'ordering': ('-created_at',),
                'abstract': False,
            },
            bases=(dirtyfields.dirtyfields.DirtyFieldsMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('short_description', models.TextField(blank=True)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from=contentio.utils.get_post_slug, unique=True)),
                ('avatar', versatileimagefield.fields.VersatileImageField(blank=True, upload_to=contentio.utils.get_post_media_path_prefix, verbose_name='Image')),
                ('alt', models.CharField(blank=True, max_length=255)),
                ('status', models.CharField(choices=[('DRAFT', 'Draft'), ('ACTIVE', 'Active'), ('HIDDEN', 'Hidden'), ('REMOVED', 'Removed')], db_index=True, default='ACTIVE', max_length=20)),
                ('meta_title', models.CharField(blank=True, max_length=255)),
                ('meta_description', models.TextField(blank=True)),
                ('is_noindex', models.BooleanField(default=False)),
                ('focus_keyword', models.CharField(blank=True, max_length=255)),
                ('canonical_url', models.URLField(blank=True)),
                ('view_count', models.PositiveBigIntegerField(default=0)),
            ],
            options={
                'ordering': ('-created_at',),
                'abstract': False,
            },
            bases=(dirtyfields.dirtyfields.DirtyFieldsMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Redirect',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('type', models.CharField(blank=True, max_length=255)),
                ('is_permanent', models.BooleanField(default=False)),
                ('old', models.CharField(blank=True, max_length=255)),
                ('new', models.CharField(blank=True, max_length=255)),
                ('extras', models.JSONField(default=list)),
            ],
            options={
                'ordering': ('-created_at',),
                'abstract': False,
            },
            bases=(dirtyfields.dirtyfields.DirtyFieldsMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Sponsor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('field', models.JSONField(default=list)),
                ('nofollow', models.BooleanField(default=False)),
                ('dofollow', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ('-created_at',),
                'abstract': False,
            },
            bases=(dirtyfields.dirtyfields.DirtyFieldsMixin, models.Model),
        ),
    ]
