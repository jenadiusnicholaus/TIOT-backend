
from django.contrib import admin
from django.urls import path, include # new
from django.conf import settings # new
from . views import ( EjabberdSetPresenceView,
                      EjabberdgetPresenceView,
                      EjabberdgetRosterView,
                      EjabberdAddRosterItemView,
                      EjabberdSendStanzaMessage,
                      EjabberdRetrieveMessages
                      
                      )
version = settings.API_VERSION


urlpatterns = [
    path(f'api/{version}/set-presence/', EjabberdSetPresenceView.as_view()),
    path(f'api/{version}/get-presence/', EjabberdgetPresenceView.as_view()),
    path(f'api/{version}/get-roster/', EjabberdgetRosterView.as_view()),
    path(f'api/{version}/add-roster-item/', EjabberdAddRosterItemView.as_view()),
    path(f'api/{version}/send-message/', EjabberdSendStanzaMessage.as_view()),
    path(f'api/{version}/retrieve-messages/', EjabberdRetrieveMessages.as_view())
]

