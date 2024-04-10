from rest_framework import serializers

from tuya_smart_home_devices.models import Device, MyDevices

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = '__all__'


class MyDeviceSerializers(serializers.ModelSerializer):
    device = DeviceSerializer() # nested serializer
    class Meta:
        model = MyDevices
        fields = ['device' ]