# Generated by Django 4.2.9 on 2024-04-10 09:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tuya_smart_home_devices', '0006_remove_device_user_id_mydevices'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mydevices',
            old_name='Device_id',
            new_name='device_id',
        ),
    ]