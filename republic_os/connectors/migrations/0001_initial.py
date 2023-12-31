# Generated by Django 4.0.10 on 2023-04-06 20:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='OAuthState',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('state', models.CharField(max_length=255)),
                ('scope', models.CharField(max_length=255)),
                ('code', models.CharField(max_length=255)),
                ('access_token', models.CharField(max_length=255)),
                ('refresh_token', models.CharField(max_length=255)),
                ('expires_in', models.IntegerField()),
                ('wallet_address', models.CharField(max_length=255)),
                ('re_public_user_id', models.CharField(max_length=255)),
                ('code_verifier', models.CharField(max_length=255)),
                ('connector_id', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
