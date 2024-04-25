from django.conf import settings
from tuya_iot import TuyaOpenAPI
import logging
from tuya_connector import (
    TuyaOpenAPI,
    TuyaOpenPulsar,
    TuyaCloudPulsarTopic,
    TUYA_LOGGER,
)
class TuyaDeviceController:
    def __init__(self, ):
        self.openapi = TuyaOpenAPI(settings.ENDPOINT, settings.ACCESS_ID, settings.ACCESS_KEY) 
        try:
            self.openapi.connect()
            TUYA_LOGGER.setLevel(logging.DEBUG)
        except Exception as e:
            print(e)
            raise Exception(e)

    
    def get_statistics(self):
        return self.openapi.get("/v1.0/statistics-datas-survey", dict())

    def start_message_queue(self, message_listener):
        self.open_pulsar.add_message_listener(message_listener)
        self.open_pulsar.start()

    def stop_message_queue(self):
        self.open_pulsar.stop()


    def get_device_details(self, device_id):
        return self.openapi.get(f"/v1.0/iot-03/devices/{device_id}")
    
    def get_device_functions(self, device_id):
        return self.openapi.get(f"/v1.0/iot-03/devices/{device_id}/functions")
    

    def get_device_status(self, device_id):
        return self.openapi.get(f"/v1.0/iot-03/devices/{device_id}/status")
    
    def get_device_commands(self, device_id):
        return self.openapi.get(f"/v1.0/iot-03/devices/{device_id}/commands")
    
    def get_device_properties(self, device_id):
        return self.openapi.get(f"/v1.0/iot-03/devices/{device_id}/properties")
    
    def get_device_property(self, device_id, property_id):
        return self.openapi.get(f"/v1.0/iot-03/devices/{device_id}/properties/{property_id}")
    
    def get_device_list(self):
        return self.openapi.get(f"/v1.1/iot-03/devices?page_size=10")
    
    def get_device_list_by_category(self, category):
        return self.openapi.get(f"/v1.1/iot-03/devices?category={category}")    
    
    def get_device_list_by_room(self, room_id):

        return self.openapi.get(f"/v1.1/iot-03/devices?room_id={room_id}")
    
    def get_device_list_by_group(self, group_id):
        return self.openapi.get(f"/v1.1/iot-03/devices?group_id={group_id}")
    
    def get_device_list_by_room_and_group(self, room_id, group_id): 
        return self.openapi.get(f"/v1.1/iot-03/devices?room_id={room_id}&group_id={group_id}")
  
    def update_device(self, device_id, device_data):
        return self.openapi.put(f"/v1.0/iot-03/devices/{device_id}", device_data)

    def delete_device(self, device_id):
        return self.openapi.delete(f"/v1.0/iot-03/devices/{device_id}")
    
    def delete_devices(self, device_ids):
        return self.openapi.delete(f"/v1.0/iot-03/devices?device_ids={device_ids}")

    def get_status_reporting_log(self, device_id, codes, start_time, end_time, size, last_row_key=None,):
        return self.openapi.get(f"/v1.0/iot-03/devices/{device_id}/report-logs?codes={codes}&end_time={end_time}&size={size}&start_time={start_time}") 
       
    def get_device_logs(self, device_id, codes, event_types, start_time, end_time, size=None, last_row_key=None ):
        return self.openapi.get(f"/v1.0/iot-03/devices/{device_id}/logs?codes={codes}&end_time={end_time}&event_types={event_types}&start_time={start_time}")
    
    def send_command(self, device_id, command):
        return self.openapi.post(f'/v1.0/iot-03/devices/{device_id}/commands', command)
    
   

