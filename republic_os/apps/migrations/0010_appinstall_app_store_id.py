# Generated by Django 4.0.10 on 2023-04-04 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0009_rename_app_id_app_app_store_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='appinstall',
            name='app_store_id',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
