# Generated by Django 4.2.9 on 2024-02-24 09:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0008_userprofile_iser_profile_pic'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='iser_profile_pic',
            new_name='user_profile_pic',
        ),
    ]