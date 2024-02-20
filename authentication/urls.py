from django.urls import path, include
from rest_framework import routers
from authentication.views import TinantRegisterUserModelView, ActivateAccount, ResendOtp, RentalOwnRegisterUserModelView, DeleteAccount, ChangePasswordView,ResetPasswordInitView ,ResetPasswordConfirmView,UpdateUserProfile
router = routers.DefaultRouter()
router.register(r'user-registration', TinantRegisterUserModelView)
router.register(r'rental-owner-registration', RentalOwnRegisterUserModelView)
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
    path('v1/delete-account/', DeleteAccount.as_view(), name='delete_account'), 
    path('v1/change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('v1/initiate-reset-password/', ResetPasswordInitView.as_view(), name='reset_password'),
    path('v1/confirm-reset-password/', ResetPasswordConfirmView.as_view(), name='confirm_reset_password'),
    path('v1/update-user-profile/', UpdateUserProfile.as_view(), name='update_user_profile'),

]