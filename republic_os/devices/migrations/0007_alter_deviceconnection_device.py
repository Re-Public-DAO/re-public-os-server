# Generated by Django 4.0.10 on 2023-05-23 21:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0006_deviceconnection'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deviceconnection',
            name='device',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='connection', to='devices.device'),
        ),
    ]