# Generated by Django 4.0.10 on 2023-04-17 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('connectors', '0012_alter_oauthstate_code'),
    ]

    operations = [
        migrations.CreateModel(
            name='RawFileIngest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(max_length=255, null=True)),
                ('error', models.CharField(max_length=255, null=True)),
                ('completed_at', models.DateTimeField(null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
