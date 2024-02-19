from rest_framework import permissions
from django.contrib.auth.models import User


class IsValidLogin(permissions.BasePermission):
    """
    Custom permission to only allow clients who are the owner of the customer
    """

    def has_permission(self, request, view):
        try:
            user = User.objects.get(id=request.data['username'])
            if user.is_active:
                return True
            else:
                return False
        except User.DoesNotExist:
            return False    
        # user = User.objects.get(id=request.data['username'])
       