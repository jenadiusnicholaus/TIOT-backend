
from django.contrib import admin
from django.urls import path, include # new
from django.conf import settings # new
from django.conf.urls.static import static # new


urlpatterns = [
    path('admin/', admin.site.urls),
     path('api-auth/', include('rest_framework.urls')),
     path('api/user-auth/', include('authentication.urls')),
     path('api/device/', include('tuya_smart_home_devices.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

