# Generated by Django 4.2.5 on 2024-01-14 02:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogio', '0011_remove_tool_is_indexed_subcategory_focus_keyword_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='tool',
            name='verified_status',
            field=models.CharField(blank=True, choices=[('PENDING', 'Pending'), ('APPROVED', 'Approved'), ('REJECTED', 'Rejected')], max_length=30),
        ),
    ]
