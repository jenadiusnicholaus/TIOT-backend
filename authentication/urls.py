from django.urls import path, include, re_path
from django.conf import settings
from rest_framework import routers
from authentication.views import TinantRegisterUserModelView, ActivateAccount, ResendOtp, RentalOwnRegisterUserModelView, DeleteAccount, ChangePasswordView,ResetPasswordInitView ,ResetPasswordConfirmView, UserProfileViewSet, GoogleSignInView
router = routers.DefaultRouter()
router.register(r'user-registration', TinantRegisterUserModelView)
router.register(r'rental-owner-registration', RentalOwnRegisterUserModelView)
router.register(r'user-profile_vset', UserProfileViewSet)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
api_version = settings.API_VERSION  
urlpatterns = [
    path(f'{api_version}/', include(router.urls)),
    path(f'{api_version}/token/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path(f'{api_version}/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path(f'{api_version}/activate-account/', ActivateAccount.as_view(), name='activate_account'),
    path(f'{api_version}/resend-otp/', ResendOtp.as_view(), name='resend_otp'),
    path(f'{api_version}/delete-account/', DeleteAccount.as_view(), name='delete_account'), 
    path(f'{api_version}/change-password/', ChangePasswordView.as_view(), name='change_password'),
    path(f'{api_version}/initiate-reset-password/', ResetPasswordInitView.as_view(), name='reset_password'),
    path(f'{api_version}/confirm-reset-password/', ResetPasswordConfirmView.as_view(), name='confirm_reset_password'),
    path(f'{api_version}/social_auth/google/', GoogleSignInView.as_view(), name='google_login'),



]