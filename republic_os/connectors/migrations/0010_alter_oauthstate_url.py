# Generated by Django 4.0.10 on 2023-04-17 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('connectors', '0009_alter_oauthstate_scope'),
    ]

    operations = [
        migrations.AlterField(
            model_name='oauthstate',
            name='url',
            field=models.CharField(max_length=500, null=True),
        ),
    ]