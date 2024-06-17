from pyejabberd import EjabberdAPIClient # type: ignore

from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import json 

from ejabberd_integration.ejabberd_api_lib import EjabberdApi


api = EjabberdApi(settings.EJABBERD_API_ACCESS_TOKEN)


class EjabberdSetPresenceView(APIView):
    def post(self, request):
        # Get the key from the QueryDict
        json_string = list(request.data.keys())[0]

        # Convert the JSON string to a dictionary
        data = json.loads(json_string)

        # Now you can access the values in the dictionary
        user = data.get("user")
        host = data.get("host")
        resource = data.get("resource")
        type = data.get("type")
        show = data.get("show")
        _status = data.get("status")
        priority = data.get("priority")
        priority = int(priority)


        try:

            response = api.setPresence(user, host, resource, type, show, _status, priority)
            if response.status_code == 200  :
                return Response(response.json(), status=status.HTTP_200_OK)
        
            return Response(response.json(), status=status.HTTP_400_BAD_REQUEST)
        except ValueError as e: 
            print(e) 

            return Response({"error": f"{e}"}, status=status.HTTP_400_BAD_REQUEST)
       
       
    
    
class EjabberdgetPresenceView(APIView):
    def post(self, request):
        # Get the key from the QueryDict
        json_string = list(request.data.keys())[0]

        # Convert the JSON string to a dictionary
        data = json.loads(json_string)

        # Now you can access the values in the dictionary
        user = data.get("user")
        host = data.get("host")

        response = api.getPresence(user, host)

        if response.status_code == 200:
            return Response(response.json(), status=status.HTTP_200_OK)
        
        return Response(response.json(), status=status.HTTP_400_BAD_REQUEST)

      

       


