
from django.utils import timezone
import datetime
import time
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets

from tuya_smart_home.decice_api import  TuyaDeviceController
from tuya_smart_home.models import Device, RentalOwnerProPertyRoomtype, RentalOwnerProperty, RentalOwnerPropertyDevices, RentalOwnerPropertyRoom, TenantRoomDevices
from tuya_smart_home.serializers import  DeviceSerializer, PropertyDeviceSerializers, RentalOwnerPropertySerializers, RentalOwnerRoomSerializers, RentalOwnerRoomTypeSerializers
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
                    # save_response to database
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
            
class RentalOwnerProperties(viewsets.ModelViewSet):
    queryset =  RentalOwnerPropertyRoom.objects.all() 
    serializer_class = RentalOwnerPropertySerializers
    permission_classes = [IsValidLogin, IsRentalOwner, IsAuthenticated]
    def list(self, request):
        # get all devices for rental owner
        my_property = self. filter_queryset(self.get_queryset().filter(user_id=request.user.id))
        if not my_property.exists():    
            return Response({'message': 'No Property found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.get_serializer(my_property, many=True)
        return Response({
            'properties': serializer.data, 
            'success': True,
            'message': 'Devices fetched successfully'
        }, status=status.HTTP_200_OK)
    
    def create(self, request):
        # create property for rental owner
        request_data = {
            'user_id': request.user.id,
            'name': request.data.get('name'),
            'lon': request.data.get('lon'),
            'lat': request.data.get('lat'),
            'geo_name': request.data.get('geo_name'),
            'city': request.data.get('city'),
            'province': request.data.get('province')

         }

        serializer = self.get_serializer(data=request_data)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': True, 'message': 'Property added successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST) 
        
    def put(self, request ): 
        # update property for rental owner
        request_data = {
            'user_id': request.user.id,
            'name': request.data.get('name'),
            'lon': request.data.get('lon'),
            'lat': request.data.get('lat'),
            'geo_name': request.data.get('geo_name'),
            'city': request.data.get('city'),
            'province': request.data.get('province')

         }
        try:
            property = RentalOwnerProperty.objects.get(id=request.query_params.get('property_id'))  
            serializer = self.get_serializer(property, data=request_data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'success': True, 'message': 'Property updated successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST) 
        except RentalOwnerProperty.DoesNotExist:
            return Response({'message': 'Property not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        # delete property for rental owner
        try:
            property = RentalOwnerProperty.objects.get(id=request.query_params.get('property_id'))  
            property.delete()
            return Response({'success': True, 'message': 'Property deleted successfully'}, status=status.HTTP_200_OK)
        except RentalOwnerProperty.DoesNotExist:
            return Response({'message': 'Property not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        



class RentalOwnerPropertyRoomTypeViewSet(viewsets.ModelViewSet): 
    queryset =  RentalOwnerProPertyRoomtype.objects.all() 
    serializer_class = RentalOwnerRoomTypeSerializers
    permission_classes = [IsValidLogin, IsRentalOwner, IsAuthenticated]
    def list(self, request):
        # get all room types for rental owner
        room_types = self. filter_queryset(self.get_queryset())
        if not room_types.exists():    
            return Response({'message': 'No room types found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.get_serializer(room_types, many=True)
        return Response({
            'room_types': serializer.data, 
            'success': True,
            'message': 'Room types fetched successfully'
        }, status=status.HTTP_200_OK)
    
    def create(self, request):
        # create room type for rental owner
        request_data = {
            'name': request.data.get('name'),
            "is_active": request.data.get('is_active')
         }

        serializer = self.get_serializer(data=request_data)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': True, 'message': 'Room type added successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
    def put(self, request ):
        # update room type for rental owner
        request_data = {
            'name': request.data.get('name'),
            "is_active": request.data.get('is_active')
         }
        try:
            room_type = RentalOwnerProPertyRoomtype.objects.get(id=request.query_params.get('room_type_id'))  
            serializer = self.get_serializer(room_type, data=request_data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'success': True, 'message': 'Room type updated successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST) 
        except RentalOwnerProPertyRoomtype.DoesNotExist:
            return Response({'message': 'Room type not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request):
        # delete room type for rental owner
        try:
            room_type = RentalOwnerProPertyRoomtype.objects.get(id=request.query_params.get('room_type_id'))  
            room_type.delete()
            return Response({'success': True, 'message': 'Room type deleted successfully'}, status=status.HTTP_200_OK)
        except RentalOwnerProPertyRoomtype.DoesNotExist:
            return Response({'message': 'Room type not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        

class RentalOwnerPropertyRoomViewSet(viewsets.ModelViewSet):
    queryset =  RentalOwnerPropertyRoom.objects.all() 
    serializer_class = RentalOwnerRoomSerializers
    permission_classes = [IsValidLogin, IsRentalOwner, IsAuthenticated]
    def list(self, request):
        # get all rooms for rental owner
        my_rooms = self. filter_queryset(self.get_queryset().filter(user_id=request.user.id))
        if not my_rooms.exists():    
            return Response({'message': 'No rooms found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.get_serializer(my_rooms, many=True)
        return Response({
            'rooms': serializer.data, 
            'success': True,
            'message': 'Rooms fetched successfully'
        }, status=status.HTTP_200_OK)
    
    def create(self, request):
        # create room for rental owner
     
        request_data = {
            'user_id': request.user.id,
            'name': request.data.get('name'),
            'property_id': request.data.get('property_id'),
            'room_type': request.data.get('room_type')
         }

        serializer = self.get_serializer(data=request_data)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': True, 'message': 'Room added successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST) 
        
    def put(self, request ): 
        # update room for rental owner
        request_data = {
            'user_id': request.user.id,
            'name': request.data.get('name'),
            'property_id': request.data.get('property_id'),
            'room_type': request.data.get('room_type')
         }
        try:
            room = self.get_queryset().get(id=request.query_params.get('room_id'))
            serializer = self.get_serializer(room, data=request_data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'success': True, 'message': 'Room updated successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST) 
        except RentalOwnerProperty.DoesNotExist:
            return Response({'message': 'Room not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        # delete room for rental owner
        try:
            room = self.get_queryset().get(id=request.query_params.get('room_id')) 
            room.delete()
            return Response({'success': True, 'message': 'Room deleted successfully'}, status=status.HTTP_200_OK)
        except RentalOwnerProperty.DoesNotExist:
            return Response({'message': 'Room not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
          
         

class RentalOwnerPropertyDeviceViewSet(viewsets.ModelViewSet):
    queryset =  RentalOwnerPropertyDevices.objects.all() 
    serializer_class = PropertyDeviceSerializers
    permission_classes= [IsValidLogin, IsRentalOwner, IsAuthenticated]
    def list(self, request):
        my_devices = self. filter_queryset(self.get_queryset().filter(property_id=request.query_params.get('property_id')))
        if not my_devices:
            return Response({'message': 'No devices found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.get_serializer(my_devices, many=True)
        return Response({
            'devices': serializer.data, 
            'success': True,
            'message': 'Devices fetched successfully'
        }, status=status.HTTP_200_OK)
    
    def create(self, request):
        # add device to property
        if request.data.get('device_id') is None or request.data.get('property_id') is None:
            return Response({'message': 'device_id and property_id are required'}, status=status.HTTP_400_BAD_REQUEST)
        
        current_time = timezone.now()
        request_data = {
            'device_id': request.data.get('device_id'),
            'property_id': request.data.get('property_id'),
            'create_time': current_time
            }
        
        serializer = self.get_serializer(data=request_data)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': True, 'message': 'Device added successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        
        
       

class DeviceFunctionsViewSet(viewsets.ModelViewSet):
    queryset =  TenantRoomDevices.objects.all() 
    serializer_class = DeviceSerializer
    permission_classes = [IsValidLogin, IsAuthenticated]
    def list(self, request):
        # get device  statistics
        device_id = request.query_params.get('device_id')
        tuyaDeviceController = TuyaDeviceController()
      

        try:
            #  get_status_reporting_log(self, device_id, codes, start_time, end_time, last_row_key, size)
            response = tuyaDeviceController.get_device_functions( device_id=device_id)
            if response.get('success') == False:
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class  ControllDeviceVset(viewsets.ModelViewSet):
    queryset =  TenantRoomDevices.objects.all() 
    serializer_class = DeviceSerializer
    permission_classes = [IsValidLogin, IsAuthenticated]


    def create(self, request):  
        # send command to device
        device_id = request.query_params.get('device_id')
        command = request.data
        tuyaDeviceController = TuyaDeviceController()

        try:
            response = tuyaDeviceController.send_command(device_id=device_id, command=command)
            if response.get('success') == False:
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST) 
           

class DevicePropertiesViewSet(viewsets.ModelViewSet):
    queryset =  TenantRoomDevices.objects.all() 
    serializer_class = DeviceSerializer
    permission_classes = [IsValidLogin, IsAuthenticated]
    def list(self, request):
        # get device  statistics
        device_id = request.query_params.get('device_id')
        tuyaDeviceController = TuyaDeviceController()
        try:
            response = tuyaDeviceController.get_device_properties( device_id=device_id)
            if response.get('success') == False:
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class DeviceStatusViewSet(viewsets.ModelViewSet):
    queryset =  TenantRoomDevices.objects.all() 
    serializer_class = DeviceSerializer
    permission_classes = [IsValidLogin, IsAuthenticated]
    def list(self, request):
        # get device  statistics
        device_id = request.query_params.get('device_id')
        tuyaDeviceController = TuyaDeviceController()
        try:
            response = tuyaDeviceController.get_device_status(device_id=device_id)
            if response.get('success') == False:
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class DeviceLogsViewSet(viewsets.ModelViewSet):
    queryset =  TenantRoomDevices.objects.all() 
    serializer_class = DeviceSerializer
    permission_classes = [IsValidLogin, IsAuthenticated]
    def list(self, request):
        # get device  statistics
        device_id = request.query_params.get('device_id')
        tuyaDeviceController = TuyaDeviceController()
        try:
            # Get today's date
            today = datetime.date.today()

            # Get yesterday's date
            yesterday = today - datetime.timedelta(days=1)

            # Convert dates to timestamps
            start_time = int(time.mktime(yesterday.timetuple()))
            end_time = int(time.mktime(today.timetuple()))
            codes = request.query_params.get('codes')
            # start_time = request.query_params.get('start_time')
            # end_time = request.query_params.get('end_time')
            last_row_key = request.query_params.get('last_row_key')
            size = request.query_params.get('size')
            event_types = request.query_params.get('event_types')   
            response = tuyaDeviceController.get_device_logs(device_id=device_id, event_types=event_types, codes=codes, start_time=start_time, end_time=end_time, last_row_key=last_row_key, size=size)

            # response = tuyaDeviceController.get_device_logs( device_id=device_id)
            if response.get('success') == False:
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)   


class DeviceStatusLogsViewSet(viewsets.ModelViewSet):
    queryset =  Device.objects.all() 
    serializer_class = DeviceSerializer
    permission_classes = [IsValidLogin, IsAuthenticated]
    def list(self, request):
        # get device  statistics
        device_id = request.query_params.get('device_id')
        tuyaDeviceController = TuyaDeviceController()
        try:
            # Get today's date
            today = datetime.date.today()

            # Get yesterday's date
            yesterday = today - datetime.timedelta(days=1)

            # Convert dates to timestamps
            start_time = int(time.mktime(yesterday.timetuple()))
            end_time = int(time.mktime(today.timetuple()))
            codes = request.query_params.get('codes')
            # start_time = request.query_params.get('start_time')
            # end_time = request.query_params.get('end_time')
            last_row_key = request.query_params.get('last_row_key')
            size = request.query_params.get('size')
            response = tuyaDeviceController.get_status_reporting_log(device_id=device_id, codes=codes, start_time=start_time, end_time=end_time, last_row_key=last_row_key, size=size)

            # response = tuyaDeviceController.get_device_logs( device_id=device_id)
            if response.get('success') == False:
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)        
        
  