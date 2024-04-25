from django.contrib import admin
from .models import Device, TenantRoomDevices, SmartLockCard, RentalOwnerPropertyDevices, RentalOwnerRoomDevices, TenantPropertyDevices, RentalOwnerProperty, RentalOwnerPropertyRoom, RentalOwnerPropertyDevices, TenantPropertyDevices, RentalOwnerProPertyRoomtype

class RentalOwnerPropertyAdmin(admin.ModelAdmin):
   
    list_display = ['id', 'name', 'lon', 'lat', 'geo_name', 'image', 'city',  'province', 'create_time', 'update_time', 'is_active']

class RentalOwnerPropertyDevicesAdmin(admin.ModelAdmin):
    list_display = ['device_id', 'property_id', ]  

class RentalOwnerRoomDevicesAdmin(admin.ModelAdmin):
    list_display = ['device_id', 'room_id', 'create_time']


class TenantPropertyDevicesAdmin(admin.ModelAdmin):
    list_display = ['device', 'user_id', 'property_id', 'create_time']

class TenantRoomDevicesAdmin(admin.ModelAdmin):
    list_display = ['device', 'user_id', 'room_id', 'create_time']

class RentalOwnerPropertyRoomAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'property_id']

class RentalOwnerProPertyRoomtypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


class DeviceAdmin(admin.ModelAdmin):
    list_display = ['active_time', 'asset_id', 'category', 'category_name', 'create_time', 'gateway_id', 'icon', 'id', 'ip', 'lat', 'local_key', 'lon', 'model', 'name', 'online', 'product_id', 'product_name', 'sub', 'time_zone', 'update_time', 'uuid', 'is_active']

class TenantRoomAdmin(admin.ModelAdmin):
    list_display = ['device', 'user_id', 'room_id', 'create_time']

class SmartLockCardAdmin(admin.ModelAdmin):
    list_display = ['tenant_id', 'card_id', 'card_number', 'card_type', 'create_time', 'device_id', 'end_time', 'start_time']



admin.site.register(RentalOwnerProperty, RentalOwnerPropertyAdmin)
admin.site.register(Device, DeviceAdmin)
admin.site.register(TenantRoomDevices, TenantRoomAdmin)
admin.site.register(SmartLockCard, SmartLockCardAdmin)
admin.site.register(RentalOwnerPropertyDevices, RentalOwnerPropertyDevicesAdmin)
admin.site.register(RentalOwnerRoomDevices, RentalOwnerRoomDevicesAdmin)
admin.site.register(TenantPropertyDevices, TenantPropertyDevicesAdmin)
admin.site.register(RentalOwnerPropertyRoom, RentalOwnerPropertyRoomAdmin)
admin.site.register(RentalOwnerProPertyRoomtype, RentalOwnerProPertyRoomtypeAdmin)

# admin.site.register(Device)

