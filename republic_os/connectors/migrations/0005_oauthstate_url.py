# Generated by Django 4.0.10 on 2023-04-14 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('connectors', '0004_oauthstate_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='oauthstate',
            name='url',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
