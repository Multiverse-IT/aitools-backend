# Generated by Django 4.2.5 on 2023-10-08 07:25

import autoslug.fields
import catalogio.utils
import dirtyfields.dirtyfields
from django.db import migrations, models
import django.db.models.deletion
import uuid
import versatileimagefield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=255)),
            ],
            options={
                'ordering': ('-created_at',),
                'abstract': False,
            },
            bases=(dirtyfields.dirtyfields.DirtyFieldsMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Feature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=255)),
            ],
            options={
                'ordering': ('created_at',),
            },
            bases=(dirtyfields.dirtyfields.DirtyFieldsMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('pros', models.CharField(blank=True, max_length=255)),
                ('cons', models.CharField(blank=True, max_length=255)),
                ('review', models.CharField(blank=True, max_length=255)),
                ('rating', models.DecimalField(decimal_places=1, default=None, max_digits=2)),
            ],
            options={
                'ordering': ('created_at',),
            },
            bases=(dirtyfields.dirtyfields.DirtyFieldsMixin, models.Model),
        ),
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=255)),
            ],
            options={
                'ordering': ('-created_at',),
                'abstract': False,
            },
            bases=(dirtyfields.dirtyfields.DirtyFieldsMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Tool',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
                ('is_verified', models.BooleanField(default=False)),
                ('pricing', models.DecimalField(blank=True, decimal_places=3, max_digits=19, null=True)),
                ('categories', models.JSONField(blank=True, default=list)),
                ('description', models.TextField()),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from=catalogio.utils.get_tool_slug, unique=True)),
                ('is_editor', models.BooleanField(default=False)),
                ('is_trending', models.BooleanField(default=False)),
                ('is_new', models.BooleanField(default=True)),
                ('save', models.PositiveBigIntegerField()),
                ('image', versatileimagefield.fields.VersatileImageField(blank=True, upload_to=catalogio.utils.get_tools_media_path_prefix, verbose_name='Avatar')),
                ('short_description', models.CharField(max_length=255)),
                ('website_url', models.URLField(blank=True)),
                ('blog_url', models.URLField(blank=True)),
                ('linkedin_url', models.URLField(blank=True)),
                ('instagram_url', models.URLField(blank=True)),
                ('facebook_url', models.URLField(blank=True)),
                ('twitter_url', models.URLField(blank=True)),
            ],
            options={
                'ordering': ('-created_at',),
            },
            bases=(dirtyfields.dirtyfields.DirtyFieldsMixin, models.Model),
        ),
        migrations.CreateModel(
            name='ToolsConnector',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('feature', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='catalogio.feature')),
                ('rating', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='catalogio.rating')),
                ('tool', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalogio.tool')),
            ],
            options={
                'ordering': ('-created_at',),
                'abstract': False,
            },
            bases=(dirtyfields.dirtyfields.DirtyFieldsMixin, models.Model),
        ),
        migrations.AddField(
            model_name='rating',
            name='tool',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalogio.tool'),
        ),
        migrations.CreateModel(
            name='CategoryConnector',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalogio.category')),
                ('sub_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalogio.subcategory')),
                ('tool', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='catalogio.tool')),
            ],
            options={
                'ordering': ('-created_at',),
                'abstract': False,
            },
            bases=(dirtyfields.dirtyfields.DirtyFieldsMixin, models.Model),
        ),
    ]
