from django.urls import path, include, re_path
from django.conf import settings
from rest_framework import routers
from .views import DeviceViewViewSet, RentalOwnerPropertyDeviceViewSet, DeviceFunctionsViewSet, ControllDeviceVset, DeviceStatusViewSet, DeviceLogsViewSet, DeviceStatusLogsViewSet,RentalOwnerProperties, RentalOwnerPropertyRoomViewSet, RentalOwnerPropertyRoomTypeViewSet, DashBoardStatsViewSet
router = routers.DefaultRouter()
router.register(r'device-vset', DeviceViewViewSet)
router.register(r'device-functions-vset', DeviceFunctionsViewSet)
router.register(r'controll-device-vset', ControllDeviceVset)
router.register(r'device-status-vset', DeviceStatusViewSet)
router.register(r'device-logs-vset', DeviceLogsViewSet)
router.register(r'device-status-logs-vset', DeviceStatusLogsViewSet)
# rental owner properties   
router.register(r'rental-owner-properties_vset', RentalOwnerProperties)  
router.register(r'rental-owner-property-device-vset', RentalOwnerPropertyDeviceViewSet)
router.register(r'rental-owner-property-room_vset', RentalOwnerPropertyRoomViewSet)
router.register(r'rental-owner-property-room-type_vset', RentalOwnerPropertyRoomTypeViewSet)
# rental-owner-property-room-type_vset

router.register(r'dashboard-stats_vset', DashBoardStatsViewSet) 



api_version = settings.API_VERSION  
urlpatterns = [
    path(f'{api_version}/', include(router.urls)),
]