# Generated by Django 4.0.10 on 2023-05-09 20:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0003_device_brand_device_desktop_device_mobile_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='os',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='device',
            name='os_version',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
