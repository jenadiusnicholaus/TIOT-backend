# Generated by Django 4.2.9 on 2024-04-20 14:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tuya_smart_home', '0022_rentalownerpropertyroom_create_time_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rentalownerpropertydevices',
            name='create_time',
        ),
    ]
