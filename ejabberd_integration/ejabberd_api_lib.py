import requests
from django.conf import settings 
import json   

class EjabberdApi:
    def __init__(self, access_token):
        self.access_token = access_token
        self.headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json',
        }       

    def setPresence(self, user, host, resource, type, show, status, priority):
        url = settings.EJABBERD_API_BU + "/api/set_presence"
        payload = json.dumps({
        "user": user,
        "host": host,  
        "resource": resource,
        "type": type,
        "show": show,
        "status": status,
        "priority": priority
        })
        headers = self.headers

        response = requests.request("POST", url, headers=headers, data=payload)
        return response

    def getPresence(self, user, host):
        url = settings.EJABBERD_API_BU + "/api/get_presence"
        payload = json.dumps({
        "user": user,
        "host": host
        })
        headers = self.headers

        response = requests.request("POST", url, headers=headers, data=payload)
        return response 

        
