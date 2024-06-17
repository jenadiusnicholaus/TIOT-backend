
from django.contrib import admin
from django.urls import path, include # new
from django.conf import settings # new
from . views import EjabberdSetPresenceView,EjabberdgetPresenceView
version = settings.API_VERSION


urlpatterns = [
    path(f'api/{version}/set-presence/', EjabberdSetPresenceView.as_view()),
    path(f'api/{version}/get-presence/', EjabberdgetPresenceView.as_view()),
]

