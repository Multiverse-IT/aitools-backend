# Generated by Django 4.2.5 on 2024-04-07 06:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalogio', '0018_bestalternativetool'),
    ]

    operations = [
        migrations.AddField(
            model_name='bestalternativetool',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='catalogio.category'),
        ),
    ]
