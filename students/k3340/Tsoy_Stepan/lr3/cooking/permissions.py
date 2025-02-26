from djoser import permissions
from rest_framework.permissions import BasePermission


class IsAuthorOrReadonly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_superuser or obj.author == request.user


class IsMealAuthorOrReadonly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_superuser or obj.meal.author == request.user