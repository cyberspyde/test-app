# Generated by Django 5.1.3 on 2024-12-11 15:08

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0021_favorite_my_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='favorites',
        ),
        migrations.DeleteModel(
            name='Favorite',
        ),
        migrations.AddField(
            model_name='user',
            name='favorites',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=20), blank=True, null=True, size=5),
        ),
    ]
