# Generated by Django 4.2.1 on 2023-06-12 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pdi_app', '0021_rename_config_functionparametertopass_dict_config_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskoutput',
            name='output',
            field=models.TextField(blank=True, null=True),
        ),
    ]
