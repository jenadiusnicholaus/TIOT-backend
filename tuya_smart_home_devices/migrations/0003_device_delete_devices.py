# Generated by Django 4.2.9 on 2024-04-10 06:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tuya_smart_home_devices', '0002_remove_devices_device_category_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('active_time', models.BigIntegerField(blank=True, null=True)),
                ('asset_id', models.CharField(blank=True, max_length=50, null=True)),
                ('category', models.CharField(max_length=50)),
                ('category_name', models.CharField(blank=True, max_length=100, null=True)),
                ('create_time', models.BigIntegerField(blank=True, null=True)),
                ('gateway_id', models.CharField(blank=True, max_length=50, null=True)),
                ('icon', models.URLField(blank=True, null=True)),
                ('id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('ip', models.GenericIPAddressField(blank=True, null=True)),
                ('lat', models.CharField(blank=True, max_length=50, null=True)),
                ('local_key', models.CharField(blank=True, max_length=50, null=True)),
                ('lon', models.CharField(blank=True, max_length=50, null=True)),
                ('model', models.CharField(blank=True, max_length=50, null=True)),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('online', models.BooleanField(blank=True, null=True)),
                ('product_id', models.CharField(blank=True, max_length=50, null=True)),
                ('product_name', models.CharField(blank=True, max_length=100, null=True)),
                ('sub', models.BooleanField(blank=True, null=True)),
                ('time_zone', models.CharField(blank=True, max_length=10, null=True)),
                ('update_time', models.BigIntegerField(blank=True, null=True)),
                ('uuid', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'verbose_name': 'Device',
                'verbose_name_plural': 'Devices',
            },
        ),
        migrations.DeleteModel(
            name='Devices',
        ),
    ]
