# Generated by Django 4.2.1 on 2023-05-16 08:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pdi_app', '0006_functionparametertopass_output_type'),
    ]

    operations = [
        migrations.RenameField(
            model_name='functionparametertopass',
            old_name='key',
            new_name='output_key',
        ),
    ]