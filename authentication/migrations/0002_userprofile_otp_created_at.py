# Generated by Django 4.2.9 on 2024-02-19 10:27

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='otp_created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
