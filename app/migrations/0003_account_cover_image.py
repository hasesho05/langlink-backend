# Generated by Django 4.1.1 on 2023-02-18 09:10

import app.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_account_encrypted_password'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='cover_image',
            field=models.ImageField(blank=True, null=True, upload_to=app.models.Account.user_directory_path, verbose_name='カバー画像'),
        ),
    ]
