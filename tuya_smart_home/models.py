import uuid
from django.db import models
from django.contrib.auth.models import User

class RentalOwnerProperty(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    lon = models.CharField(max_length=50, null=True, blank=True)
    lat = models.CharField(max_length=50, null=True, blank=True)
    geo_name = models.CharField(max_length=50, null=True, blank=True)
    image = models.ImageField(upload_to='property_images/', null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    province = models.CharField(max_length=50, null=True, blank=True)
    create_time = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    update_time = models.DateTimeField(auto_now=True, null=True, blank=True)
   
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.name if self.name else 'No name'
    class Meta:
        verbose_name_plural = "Properties"
        verbose_name = "Property"

class RentalOwnerProPertyRoomtype(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    create_time = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    update_time = models.DateTimeField(auto_now=True, null=True, blank=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = "Room Types"
        verbose_name = "Room Type"

class RentalOwnerPropertyRoom(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    room_type = models.ForeignKey(RentalOwnerProPertyRoomtype, on_delete=models.CASCADE, null=True, blank=True)   
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    property_id = models.ForeignKey(RentalOwnerProperty, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    create_time = models.DateTimeField(auto_now_add=True, null=True, blank=True)    
    update_time = models.DateTimeField(auto_now=True, null=True, blank=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = "Rooms"
        verbose_name = "Room"



# Create your models here.
class Device(models.Model):
    active_time = models.BigIntegerField( null=True, blank=True)
    asset_id = models.CharField(max_length=50, null=True, blank=True)
    category = models.CharField(max_length=50)
    category_name = models.CharField(max_length=100,null=True, blank=True)
    create_time = models.BigIntegerField(null=True, blank=True)
    gateway_id = models.CharField(max_length=50, null=True, blank=True, )
    icon = models.CharField(null=True, blank=True)
    id = models.CharField(max_length=50, primary_key=True, unique=True)
    ip = models.CharField(null=True, blank=True)
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
        return self.name if self.name else 'No name'    
    
    class Meta:
        verbose_name_plural = "Devices"
        verbose_name = "Device"

class RentalOwnerRoomDevices(models.Model):
    device_id = models.ForeignKey(Device, on_delete=models.CASCADE, null=True, blank=True)
    room_id = models.ForeignKey(RentalOwnerPropertyRoom, on_delete=models.CASCADE, null=True, blank=True)
    create_time = models.BigIntegerField(null=True, blank=True)


    def __str__(self):
        return self.device_id.name
    class Meta:
        verbose_name_plural = "Room Devices"
        verbose_name = "Room Device"

class RentalOwnerPropertyDevices(models.Model):
    device_id = models.ForeignKey(Device, on_delete=models.CASCADE, null=True, blank=True)
    property_id = models.ForeignKey(RentalOwnerProperty, on_delete=models.CASCADE, null=True, blank=True)
    create_time = models.DateTimeField( null=True, blank=True)


    class Meta:
        verbose_name_plural = "Property Devices"
        verbose_name = "Property Device"
        unique_together = ('device_id', 'property_id')  
    
    def __str__(self):
        return self.device_id.name if self.device_id and self.device_id.name else 'No name'
        

class TenantRoomDevices(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE, null=True, blank=True, unique=True, related_name='tenant_room_device')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    room_id = models.ForeignKey(RentalOwnerPropertyRoom, on_delete=models.CASCADE, null=True, blank=True)
    create_time = models.BigIntegerField(null=True, blank=True)

    def __str__(self):
        return self.device.name
    class Meta:
        verbose_name_plural = "Tenant Devices"
        verbose_name = "Tenant Device"


class TenantPropertyDevices(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE, null=True, blank=True, unique=True, related_name='tenant_property_device')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    property_id = models.ForeignKey(RentalOwnerProperty, on_delete=models.CASCADE, null=True, blank=True)
    create_time = models.BigIntegerField(null=True, blank=True)

    def __str__(self):
        return self.device.name
    class Meta:
        verbose_name_plural = "Tenant Property Devices"
        verbose_name = "Tenant Property Device"


class SmartLockCard(models.Model):
    tenant_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    card_id = models.CharField(max_length=50, null=True, blank=True)
    card_number = models.CharField(max_length=50, null=True, blank=True)
    card_type = models.CharField(max_length=50, null=True, blank=True)
    create_time = models.BigIntegerField(null=True, blank=True)
    device_id = models.ForeignKey(Device, on_delete=models.CASCADE, null=True, blank=True)
    end_time = models.BigIntegerField(null=True, blank=True)
    start_time = models.BigIntegerField(null=True, blank=True)

    def __str__(self):
        return self.card_number
    class Meta:
        verbose_name_plural = "Smart Lock Cards"
        verbose_name = "Smart Lock Card"


        