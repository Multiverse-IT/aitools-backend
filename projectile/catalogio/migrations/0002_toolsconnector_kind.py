# Generated by Django 4.2.5 on 2023-10-21 04:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogio', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='toolsconnector',
            name='kind',
            field=models.CharField(choices=[('FEATUER', 'Feature'), ('RATING', 'Rating')], default=1, max_length=30),
            preserve_default=False,
        ),
    ]
