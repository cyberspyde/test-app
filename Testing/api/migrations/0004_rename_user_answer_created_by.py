# Generated by Django 5.1.3 on 2024-11-30 04:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_user_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='answer',
            old_name='user',
            new_name='created_by',
        ),
    ]
