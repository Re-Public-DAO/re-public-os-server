# Generated by Django 4.0.10 on 2023-05-26 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0008_device_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='device',
            old_name='name',
            new_name='name_on_device',
        ),
        migrations.AddField(
            model_name='device',
            name='name_in_os',
            field=models.CharField(max_length=255, null=True),
        ),
    ]