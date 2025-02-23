from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj == request.user

class IsAdminUser(BasePermission):
    """
    Разрешение, которое позволяет доступ только администраторам.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin 
    
class IsCrewUser(BasePermission):
    """
    Разрешение, которое позволяет доступ только обычным пользователям (crew).
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and not request.user.is_admin

class IsAdminOrReadOnly(BasePermission):
    """
    Разрешение, которое позволяет администраторам все, а остальным только чтение.
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True  # Разрешить GET, HEAD, OPTIONS всем
        return request.user.is_authenticated and request.user.is_admin

