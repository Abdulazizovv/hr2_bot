# Generated by Django 5.0.1 on 2024-10-29 22:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('botapp', '0003_userrequest_sixth_answer'),
    ]

    operations = [
        migrations.AddField(
            model_name='userrequest',
            name='file_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]