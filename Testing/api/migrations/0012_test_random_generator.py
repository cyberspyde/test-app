# Generated by Django 5.1.3 on 2024-12-03 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_remove_user_number_of_tests_done'),
    ]

    operations = [
        migrations.AddField(
            model_name='test',
            name='random_generator',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
