from rest_framework import permissions
from django.contrib.auth.models import User


class IsValidLogin(permissions.BasePermission):
    """
    Custom permission to only allow clients who are the owner of the object.
    """

    def has_permission(self, request, view):
        try:
            user = User.objects.get(id=request.user.id)
            if user.is_active:
                return True
            else:
                print('User is not active')
                return False
        except User.DoesNotExist:
            print('User does not exist')
            return False

class IsRentalOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_permission(self, request, view):
        if request.user.groups.filter(name='Rental Owner').exists() and request.user.is_staff:
             return True
        else:
            print('User is not a rental owner')
            return False
       