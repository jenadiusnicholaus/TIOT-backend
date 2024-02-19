from django.urls import path, include
from rest_framework import routers
from authentication.views import RegisterUserModelView, ActivateAccount, ResendOtp
router = routers.DefaultRouter()
router.register(r'user-registration', RegisterUserModelView)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/token/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('v1/activate-account/', ActivateAccount.as_view(), name='activate_account'),
    path('v1/resend-otp/', ResendOtp.as_view(), name='resend_otp'),
]