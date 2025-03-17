from rest_framework import permissions
from .models import Order

from rest_framework import permissions

class IsClient(permissions.BasePermission):
    def has_permission(self, request, view):
        # Проверяем, является ли пользователь администратором
        if request.user.is_staff:
            return False  # Если пользователь администратор, разрешаем доступ только администраторам
        return True  # Все остальные считаются клиентами

    def has_object_permission(self, request, view, obj):
        # Для объекта (например, заказов) предоставляем доступ только клиентам
        if hasattr(request.user, 'client'):  # Проверяем, связан ли пользователь с клиентом
            return obj.client == request.user.client
        return False  # Если пользователя нет в базе клиентов, доступ запрещен


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff