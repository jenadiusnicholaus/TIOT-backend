# Generated by Django 4.2.9 on 2024-02-19 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_userprofile_otp_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='otp_used',
            field=models.BooleanField(default=False),
        ),
    ]