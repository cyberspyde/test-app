# Generated by Django 5.1.3 on 2024-12-02 08:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_performance_number_of_tests_done_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Performance',
        ),
    ]