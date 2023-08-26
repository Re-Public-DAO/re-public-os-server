# Generated by Django 4.0.10 on 2023-05-26 18:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0011_remove_appinstall_app'),
    ]

    operations = [
        migrations.AddField(
            model_name='app',
            name='interface_url_desktop',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='app',
            name='interface_url_mobile',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='app',
            name='interface_url_web',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
