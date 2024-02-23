# Generated by Django 4.2.9 on 2024-02-19 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_userprofile_otp_used'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='expire_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='otp_used_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]