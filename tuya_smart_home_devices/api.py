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
    
    def send_command(self, device_id, command):
        return self.openapi.post(f'/v1.0/iot-03/devices/{device_id}/commands', command)