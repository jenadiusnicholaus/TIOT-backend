from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets

from tuya_smart_home_devices.api import  TuyaDeviceController
from tuya_smart_home_devices.models import Device, MyDevices
from tuya_smart_home_devices.serializers import DeviceSerializer, MyDeviceSerializers
from django.conf import settings
from rest_framework import status
from rest_framework import routers
from authentication.permissions import  IsRentalOwner, IsValidLogin
from rest_framework.permissions import (DjangoModelPermissionsOrAnonReadOnly, IsAuthenticated)
from rest_framework.views import APIView

# Create your views here.

class DeviceViewViewSet(viewsets.ModelViewSet):
    queryset =  Device.objects.all() 
    serializer_class = DeviceSerializer
    # permission_classes = []

    def list(self, request):
        device_id = request.query_params.get('device_id')
        tuyaDeviceController = TuyaDeviceController()

        if device_id is not None:
            # devide details use ?device_id=xxxx  at the end of the url     
            try:
                
                response = tuyaDeviceController.get_device_details(device_id=device_id)     

                if response.get('success') == False:
                    return Response(response, status=status.HTTP_400_BAD_REQUEST)
                else:   

                    return Response(response, status=status.HTTP_200_OK)

            except Exception as e:
                return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
            
        else:
            # get all devices 
            try:
                response = tuyaDeviceController.get_device_list()
                if not response.get('success'):
                    return Response(response, status=status.HTTP_400_BAD_REQUEST)
                
                try:
                
                    self.bulkSave(response)
                except Exception as e:  
                    return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    
                queryset = self.filter_queryset(self.get_queryset())
                if not queryset:
                    return Response({'message': 'No devices found'}, status=status.HTTP_404_NOT_FOUND)
                else:
                    serializer = self.get_serializer(queryset, many=True)
                    return Response(
                            {
                                'devices': serializer.data,
                                'success': True,
                                'message': 'Devices fetched successfully'
                            },
                            status=status.HTTP_200_OK
                    )
            except Exception as e:
                return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
            
    def bulkSave(self, response):
        try:
            for device_data in response['result']['list']:
                self.save_device(device_data)
         
        except Exception as e:
               raise Exception(str(e))    
                
    def save_device(self, device_data):
     
        if not Device.objects.filter(id=device_data['id']).exists():
            serializer = DeviceSerializer(data=device_data)
            if serializer.is_valid():
                serializer.save()
            else:
               
                raise Exception(serializer.errors)



class RentalOwnerDeviceViewSet(viewsets.ModelViewSet):
    queryset =  MyDevices.objects.all() 
    serializer_class = MyDeviceSerializers
    permission_classes= [IsValidLogin, IsRentalOwner, IsAuthenticated]
    def list(self, request):
        my_devices = self. filter_queryset(self.get_queryset().filter(user_id=request.user.id))
        if not my_devices:
            return Response({'message': 'No devices found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.get_serializer(my_devices, many=True)
        return Response({
            'devices': serializer.data, 
            'success': True,
            'message': 'Devices fetched successfully'
        }, status=status.HTTP_200_OK)
    
    def create(self, request):
        # add device my_devices
        device_id = request.query_params.get('device_id')
        if device_id is None:
            return Response({'message': 'device_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                #  user serializer to save device
                if self.filter_queryset(Device.objects.filter(id=device_id)).exists():
                    serializer = self.get_serializer(data={'device': device_id, 'user_id': request.user.id})
                    if serializer.is_valid():
                        serializer.save()
                        return Response({'success': True, 'message': 'Device added successfully'}, status=status.HTTP_201_CREATED)
                    else:
                        return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)   
               
                return Response({'success': True, 'message': 'Device does exists'}, status=status.HTTP_201_CREATED)
            except Device.DoesNotExist:
                return Response({'message': 'Device not found'}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
            




        
        
        

            
        
  