from asyncio import AbstractServer
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class UserProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, null=True, blank=True)
    otp = models.CharField(max_length=6, null=True, blank=True)
    otp_created_at = models.DateTimeField(default=timezone.now)
    otp_used = models.BooleanField(default=False) 


    def __str__(self):
        return self.user.username
    


