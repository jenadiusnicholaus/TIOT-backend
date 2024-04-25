from rest_framework import serializers

from tuya_smart_home.models import Device, RentalOwnerProperty, RentalOwnerPropertyDevices, RentalOwnerPropertyRoom, TenantRoomDevices, RentalOwnerProPertyRoomtype


class RentalOwnerPropertySerializers(serializers.ModelSerializer): 
    class Meta:
        model = RentalOwnerProperty
        fields = '__all__'  

class RentalOwnerRoomSerializers(serializers.ModelSerializer):
    class Meta:
        model = RentalOwnerPropertyRoom
        fields = '__all__'

class RentalOwnerRoomTypeSerializers(serializers.ModelSerializer):
    class Meta:
        model = RentalOwnerProPertyRoomtype
        fields = '__all__'    

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = '__all__'





class PropertyDeviceSerializers(serializers.ModelSerializer):
    class Meta:
        model = RentalOwnerPropertyDevices
        fields = '__all__'