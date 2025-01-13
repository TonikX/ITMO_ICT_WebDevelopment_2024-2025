from rest_framework.permissions import BasePermission

class IsAdminOrManager(BasePermission):
    """
    Доступ разрешен только администраторам и менеджерам.
    """
    def has_permission(self, request, view):
        # Проверяем, аутентифицирован ли пользователь
        if not request.user.is_authenticated:
            return False
        
        # Проверяем роль пользователя
        return getattr(request.user, 'role', None) in ['admin', 'manager']