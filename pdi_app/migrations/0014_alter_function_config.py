# Generated by Django 4.2.1 on 2023-06-01 20:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pdi_app', '0013_task_alias_task_funtion_input'),
    ]

    operations = [
        migrations.AlterField(
            model_name='function',
            name='config',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
