from rest_framework.permissions import BasePermission

class IsAgent(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Agent').exists()

class IsOrganizationAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Organization Admin').exists()
