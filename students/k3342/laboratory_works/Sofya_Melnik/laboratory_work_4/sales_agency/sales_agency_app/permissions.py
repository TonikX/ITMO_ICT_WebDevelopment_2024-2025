from rest_framework import permissions
from .models import Order

from rest_framework import permissions

class IsClient(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_staff:
            return False
        return True

    def has_object_permission(self, request, view, obj):
        if hasattr(request.user, 'client'):
            return obj.client == request.user.client
        return False


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff