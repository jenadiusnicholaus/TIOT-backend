from datetime import timedelta
from django.contrib.auth.tokens import default_token_generator
from django.http import BadHeaderError
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from rest_framework import  viewsets
from rest_framework.response import Response

from authentication.serializers import UserSerializer, RentalOwnerRegisterSerializer, TenantRegisterSerializer
from .models import User, UserProfile
import random
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User
from django.utils import timezone
from rest_framework.permissions import AllowAny
from django.core.validators import validate_email
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import update_session_auth_hash
from .serializers import ChangePasswordSerializer, ResetPasswordConfirmSerializer, UserProfileSerializer

from google.oauth2 import id_token
from google.auth.transport import requests
from django.contrib.auth import get_user_model
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly
from rest_framework import viewsets
from django.conf import settings
from django.contrib.auth.models import Group

class GoogleSignInView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        try:
            idinfo = id_token.verify_oauth2_token(request.data['access_token'], requests.Request(), settings.GOOGLE_CLIENT_ID)

            if 'accounts.google.com' in idinfo['iss']:
                User = get_user_model()
                user, created = User.objects.get_or_create(email=idinfo['email'])
                if created:
                    user.username = idinfo['name']
                    user.is_active = True 
                     
                    user.save()
                    # Create the user profile
                    UserProfile.objects.create(user=user, is_tenant=True,
                                               phone=request.data.get('phone_number', None),
                                               )
                
                    # Add user to Tenant's Group
                    user_group, group_created = Group.objects.get_or_create(name='Tenant')
                    if not user.groups.filter(name='Tenant').exists():
                        user.groups.add(user_group)

                    
                    message = "User created successfully."
                else:
                    message = "Welcome back!"


                refresh = RefreshToken.for_user(user)
                response_data = {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    "message": message,
                    "username": user.username,
                    "email": user.email,
                }
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Invalid token issuer'}, status=status.HTTP_400_BAD_REQUEST)

        except ValueError as e:
            return Response({'message': 'Invalid or malformed token'}, status=status.HTTP_400_BAD_REQUEST)

class UserRegistration(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = RentalOwnerRegisterSerializer
    permission_classes = [AllowAny]
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():

            user = serializer.save()
            otp = random.randint(100000, 999999)
            UserProfile.objects.create( 
                user=user, 
                otp=otp,
                is_client=True,
                otp_created_at=timezone.localtime(timezone.now()))
            

            # add to Rental owner's Group
            user_group, created = Group.objects.get_or_create(name='Rental Owner')
            if not user.groups.filter(name='Rental Owner').exists():
                user.groups.add(user_group)
            # Send email with OTP

            mail_subject = 'Activate your account.'
            message = render_to_string('activate_account.html', {
                'user': user,
                'otp': otp,
            })

          
            try:
                email = request.data['email']
                email = EmailMessage(mail_subject, message, to=[email])
                res = email.send()
            except:
                user.delete()  # Delete the user if sending the email fails
                return Response({"message": "Failed to send email."}, status=status.HTTP_400_BAD_REQUEST)

            response_data = {
                "message": "User created successfully. A verification code has been sent to your email. Please verify your account immediately before the session expires in 5 minutes.",
                "user_id": user.id,
                "username": user.username,
                "email": user.email,
                "is_active": user.is_active 
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(
            {"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )




class TinantRegisterUserModelView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = TenantRegisterSerializer
    permission_classes = [AllowAny]
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        User_profile = UserProfile.objects.filter(phone=request.data.get('phone_number'))

        if User_profile.exists():
            return Response({"message": {
                "phone_number": ["Phone number already exists."]
            }}, status=status.HTTP_400_BAD_REQUEST)
        

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            otp = random.randint(100000, 999999)
            UserProfile.objects.create( 
                user=user, 
                otp=otp,
                is_tenant=True,
                phone=request.data.get('phone_number'),
                otp_created_at=timezone.localtime(timezone.now()))
            # Add user to Tenant's Group
            user_group, group_created = Group.objects.get_or_create(name='Tenant')
            if not user.groups.filter(name='Tenant').exists():
                user.groups.add(user_group)

            
            # Send email with OTP
            mail_subject = 'Activate your account.'
            message = render_to_string('activate_account.html', {
                'user': user,
                'otp': otp,
            })

          
            try:
                email = request.data['email']
                email = EmailMessage(mail_subject, message, to=[email])
                res = email.send()
            except:
                user.delete()  # Delete the user if sending the email fails
                return Response({"message": "Failed to send email."}, status=status.HTTP_400_BAD_REQUEST)

            response_data = {
                "message": "User created successfully. A verification code has been sent to your email. Please verify your account immediately before the session expires in 5 minutes.",
                "user_id": user.id,
                "username": user.username,
                "email": user.email,
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(
            {"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )
    

class ResendOtp(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        try:
            user = User.objects.get(email=request.data.get('email'))
        except User.DoesNotExist:
            return Response({'error': 'User does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        user_profile = UserProfile.objects.get(user=user)
        # if user_profile.otp_used:
        #     return Response({'error': 'OTP already used'}, status=status.HTTP_400_BAD_REQUEST)

            # Calculate the time remaining until the user can request another OTP
        time_remaining = user_profile.otp_created_at + timedelta(minutes=5) - timezone.localtime(timezone.now())
        if time_remaining > timedelta(minutes=0):

            # If the time remaining is more than 0, return an error with the time remaining
            return Response({'error': f'Please wait for {time_remaining.seconds // 60} minutes and {time_remaining.seconds % 60} seconds before sending another OTP'}, status=status.HTTP_400_BAD_REQUEST)
        otp = random.randint(100000, 999999)
        user_profile.otp = otp
        user_profile.otp_created_at = timezone.localtime(timezone.now())
        user_profile.save()
        mail_subject = 'Activate your account.'
        message = render_to_string('activate_account.html', {
            'user': user,
            'otp': otp,
        })
        email = EmailMessage(mail_subject, message, to=[request.data.get('email')])
        email.send()
        return Response({'message': 'OTP sent successfully'}, status=status.HTTP_200_OK)
        

class ActivateAccount(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
 
        try:
            user = User.objects.get(email=request.data.get('email'))
        except User.DoesNotExist:
            return Response({'error': 'User does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        otp =  request.data.get("otp", None)
        # user = User.objects.get(email=request.data.get('email'))
        user_profile = UserProfile.objects.get(user=user)
        if user_profile.otp == otp and timezone.localtime(timezone.now()) < user_profile.otp_created_at + timedelta(minutes=5):
            user.is_active = True
            user_profile.otp_used = True
            user_profile.save() 
            user.save()
            return Response({'message': 'Account activated successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid or expired OTP'}, status=status.HTTP_400_BAD_REQUEST)
        


class DeleteAccount(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        try:
            user = User.objects.get(email=request.data.get('email'))
        except User.DoesNotExist:
            return Response({'error': 'User does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        user.delete()
        return Response({'message': 'Account deleted successfully'}, status=status.HTTP_200_OK)
    



class ChangePasswordView(APIView):
    """
    An endpoint for changing password.
    """
    permission_classes = [IsAuthenticated]

    def put(self, request):
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not request.user.check_password(serializer.data.get("old_password")):
                return Response({"message": "Wrong password."}, status=status.HTTP_400_BAD_REQUEST)
            
            # set_password also hashes the password
            request.user.set_password(serializer.data.get("new_password"))
            request.user.save()
            update_session_auth_hash(request, request.user)  # Important!
            return Response({"message": "Password changed successfully"}, status=status.HTTP_200_OK)

        return Response({ "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    


class ResetPasswordInitView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        try:
            user = User.objects.get(email=request.data.get('email'))
            token = default_token_generator.make_token(user)
            mail_subject = 'Reset your password.'
            message = render_to_string('reset_password.html', {
                'user': user,
                'token': token,
            })
        except User.DoesNotExist:
            return Response({'error': 'User does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': 'An error occurred: {}'.format(str(e))}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            email = EmailMessage(mail_subject, message, to=[request.data.get('email')])
            email.send()
        except BadHeaderError:
            return Response({'error': 'Invalid header found.'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': 'An error occurred while sending the email: {}'.format(str(e))}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'message': "Password reset OTP code has been sent to your email address. Please visit your email and use that code to confirm your password reset request."}, status=status.HTTP_200_OK)
    

class ResetPasswordConfirmView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ResetPasswordConfirmSerializer(data=request.data)
        if serializer.is_valid():
           
            token = serializer.data.get('token')
            new_password = serializer.data.get('new_password')
            confirm_password = serializer.data.get('confirm_password')

            # Get the user
            try:
                user = User.objects.get(email=serializer.data.get('email'))
            except User.DoesNotExist:
                return Response({'message': 'User does not exist'}, status=status.HTTP_400_BAD_REQUEST)

            # Check if the new password and confirm password match
            if new_password != confirm_password:
                return Response({'message': 'Passwords do not match.'}, status=status.HTTP_400_BAD_REQUEST)

            # Check token
            if not default_token_generator.check_token(user, token):
                return Response({'message': 'Invalid token.'}, status=status.HTTP_400_BAD_REQUEST)

            # Set new password
            user.set_password(new_password)
            user.save()

            return Response({'message': 'Password reset successfully'}, status=status.HTTP_200_OK)
        else:

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    




class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    permission_classes = [IsAuthenticated,]
    serializer_class = UserProfileSerializer
  

    def list(self, request, *args, **kwargs):
        try:
            user = request.user.userprofile
            serializser = self.get_serializer(user)
            return Response(serializser.data, status=status.HTTP_200_OK)
        except UserProfile.DoesNotExist:    
            return Response({'message': 'UserProfile does not exist.'}, status=status.HTTP_400_BAD_REQUEST) 


    def put(self, request):
        user = request.user
        # Update fields in User model
        user.first_name = request.data.get('first_name', user.first_name)
        user.last_name = request.data.get('last_name', user.last_name)

        new_email = request.data.get('email')
        if new_email is not None:
            # Validate new email
            try:
                User.objects.exclude(pk=user.pk).get(email=new_email)
                return Response({'message': 'Email already in use.'}, status=status.HTTP_400_BAD_REQUEST)
            except User.DoesNotExist:
                user.email = new_email

        user.save()

        # Update fields in UserProfile model
        try:
            user_profile = UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            return Response({'message': 'UserProfile does not exist.'}, status=status.HTTP_400_BAD_REQUEST)

        user_profile.phone = request.data.get('phone_number', user_profile.phone)

        if 'user_profile_pic' in request.FILES:
            user_profile.user_profile_pic = request.FILES['user_profile_pic']

        user_profile.save()

        return Response({'message': 'Profile updated successfully'}, status=status.HTTP_200_OK)


