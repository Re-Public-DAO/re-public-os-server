# Generated by Django 4.0.10 on 2023-04-17 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('connectors', '0008_connectorsync'),
    ]

    operations = [
        migrations.AlterField(
            model_name='oauthstate',
            name='scope',
            field=models.CharField(max_length=500, null=True),
        ),
    ]
