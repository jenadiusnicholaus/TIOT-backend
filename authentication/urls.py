from django.urls import path, include
from rest_framework import routers
from authentication.views import UserViewSet




# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'user-vset', UserViewSet)

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/token/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]