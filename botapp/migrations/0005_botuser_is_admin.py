# Generated by Django 5.0.1 on 2024-10-30 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('botapp', '0004_userrequest_file_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='botuser',
            name='is_admin',
            field=models.BooleanField(default=False),
        ),
    ]