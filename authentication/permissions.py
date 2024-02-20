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

# class IsRentalOwner(permissions.BasePermission):
#     """
#     Custom permission to only allow owners of an object to edit it.
#     """


#     def has_object_permission(self, request, view, obj):
#         # Write permissions are only allowed to the owner of the snippet
#         return obj.user == request.user or request.user.is_staff
#     def has_permission(self, request, view):
#         return request.user.has_perm('can_add_property')   
       