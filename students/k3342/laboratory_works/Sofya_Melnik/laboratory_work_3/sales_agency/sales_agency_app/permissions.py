from rest_framework import permissions
from .models import Order

class IsClient(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='client').exists()
    
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Order):
            return obj.client == request.user.client
        return True

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff