from rest_framework import serializers

from authentication.serializers import UserProfileSerializer
from tuya_smart_home.models import Device, RentalOwnerProperty, RentalOwnerPropertyDevices, RentalOwnerPropertyRoom, TenantRoomDevices, RentalOwnerProPertyRoomtype
from django.contrib.auth.models import User

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

class DashboordStatusSerializer(serializers.ModelSerializer):
    total_properties = serializers.SerializerMethodField()
    total_rooms = serializers.SerializerMethodField()  
    total_tenants = serializers.SerializerMethodField() 
    class Meta:
        model = User
        fields = [
            "total_properties",
            "total_rooms",
            "total_tenants",

        ]

    def get_total_properties(self, obj):
        return RentalOwnerProperty.objects.filter(user_id=obj.id).count()
    
    def get_total_rooms(self, obj): 
        return RentalOwnerPropertyRoom.objects.filter(property_id__user_id=obj.id).count()
    
    def get_total_tenants(self, obj):
        #  count the tenant
        return User.objects.filter(userprofile__is_tenant=True).count()
        
        





class PropertyDeviceSerializers(serializers.ModelSerializer):
    class Meta:
        model = RentalOwnerPropertyDevices
        fields = '__all__'