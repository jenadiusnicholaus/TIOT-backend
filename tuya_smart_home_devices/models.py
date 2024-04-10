from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Device(models.Model):
    active_time = models.BigIntegerField( null=True, blank=True)
    asset_id = models.CharField(max_length=50, null=True, blank=True)
    category = models.CharField(max_length=50)
    category_name = models.CharField(max_length=100,null=True, blank=True)
    create_time = models.BigIntegerField(null=True, blank=True)
    gateway_id = models.CharField(max_length=50, null=True, blank=True)
    icon = models.CharField(null=True, blank=True)
    id = models.CharField(max_length=50, primary_key=True)
    ip = models.GenericIPAddressField(null=True, blank=True)
    lat = models.CharField(max_length=50, null=True, blank=True)
    local_key = models.CharField(max_length=50, null=True, blank=True)
    lon = models.CharField(max_length=50, null=True, blank=True)
    model = models.CharField(max_length=50, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    online = models.BooleanField(null=True, blank=True)
    product_id = models.CharField(max_length=50, null=True, blank=True)
    product_name = models.CharField(max_length=100, null=True, blank=True)
    sub = models.BooleanField(null=True, blank=True)
    time_zone = models.CharField(max_length=10, null=True, blank=True)
    update_time = models.BigIntegerField(null=True, blank=True)
    uuid = models.CharField(max_length=50, null=True, blank=True)
    is_active = models.BooleanField(default=False)

   
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Devices"
        verbose_name = "Device"

class MyDevices(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE, null=True, blank=True, unique=True, related_name='my_device')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.device.name
    class Meta:
        verbose_name_plural = "My Devices"
        verbose_name = "My Device"


        