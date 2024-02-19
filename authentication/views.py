from datetime import timedelta
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from rest_framework import  viewsets
from rest_framework.response import Response


from authentication.serializers import UserSerializer, RegisterSerializer
from .models import User, UserProfile
import random
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User
from django.utils import timezone
from rest_framework.permissions import AllowAny
from django.core.validators import validate_email




class RegisterUserModelView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            otp = random.randint(100000, 999999)
            UserProfile.objects.create( 
                user=user, otp=otp,
                otp_created_at=timezone.localtime(timezone.now()))

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
        if user_profile.otp_used:
            return Response({'error': 'OTP already used'}, status=status.HTTP_400_BAD_REQUEST)

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
        


