# Generated by Django 4.2.1 on 2023-06-13 05:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pdi_app', '0027_alter_taskoutput_output'),
    ]

    operations = [
        migrations.AddField(
            model_name='functionparametertopass',
            name='single_config',
            field=models.TextField(blank=True, null=True),
        ),
    ]
