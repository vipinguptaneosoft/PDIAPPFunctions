# Generated by Django 4.2.1 on 2023-05-17 07:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pdi_app', '0008_functionparametertopass_input_key'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='alias',
            field=models.TextField(default='Alias'),
        ),
    ]