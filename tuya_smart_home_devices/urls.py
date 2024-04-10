from django.urls import path, include, re_path
from django.conf import settings
from rest_framework import routers
from .views import DeviceViewViewSet, RentalOwnerDeviceViewSet
router = routers.DefaultRouter()
router.register(r'device-vset', DeviceViewViewSet)
router.register(r'rental-own-device-vset', RentalOwnerDeviceViewSet)
api_version = settings.API_VERSION  
urlpatterns = [
    path(f'{api_version}/', include(router.urls)),
]