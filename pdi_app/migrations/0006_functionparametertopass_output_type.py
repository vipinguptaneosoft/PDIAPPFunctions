# Generated by Django 4.2.1 on 2023-05-14 21:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pdi_app', '0005_taskoutput_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='functionparametertopass',
            name='output_type',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
