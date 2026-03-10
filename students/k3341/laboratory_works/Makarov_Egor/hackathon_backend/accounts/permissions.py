from rest_framework.permissions import BasePermission
from .models import UserRole

def _role(user):
    if not user or not user.is_authenticated:
        return None
    if user.is_superuser:
        return UserRole.ADMIN
    try:
        return user.profile.role
    except Exception:
        return None

class IsAdminRole(BasePermission):
    """Доступ только главному администратору (или superuser)."""
    def has_permission(self, request, view):
        return _role(request.user) == UserRole.ADMIN

class IsJuryRole(BasePermission):
    def has_permission(self, request, view):
        return _role(request.user) == UserRole.JURY

class IsCuratorRole(BasePermission):
    def has_permission(self, request, view):
        return _role(request.user) == UserRole.CURATOR

class IsCaptainRole(BasePermission):
    def has_permission(self, request, view):
        return _role(request.user) == UserRole.CAPTAIN

class IsAdminOrReadOnly(BasePermission):
    """Изменять может только админ, смотреть могут все авторизованные."""
    def has_permission(self, request, view):
        if request.method in ("GET", "HEAD", "OPTIONS"):
            return request.user and request.user.is_authenticated
        return _role(request.user) == UserRole.ADMIN
