# Generated by Django 4.0.10 on 2023-10-21 21:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('connectors', '0023_auto_20231001_0039'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='oauthstate',
            name='connector',
        ),
    ]