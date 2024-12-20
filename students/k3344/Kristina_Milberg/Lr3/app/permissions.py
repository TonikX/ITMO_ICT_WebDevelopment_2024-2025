from rest_framework.permissions import BasePermission


class IsBroker(BasePermission):
    def has_permission(self, request, view):
        return (request.user and
                request.user.is_authenticated
                and hasattr(request.user, 'brokerinfo') or request.user.is_superuser)
