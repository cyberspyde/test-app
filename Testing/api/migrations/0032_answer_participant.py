# Generated by Django 5.1.3 on 2024-12-13 15:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0031_question_order_testroom_testparticipant'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='participant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.testparticipant'),
        ),
    ]