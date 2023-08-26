# Generated by Django 4.0.10 on 2023-05-09 19:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0002_device_qr_code_key'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='brand',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='device',
            name='desktop',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='device',
            name='mobile',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='device',
            name='tablet',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='device',
            name='total_disk_capacity',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='device',
            name='model',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
