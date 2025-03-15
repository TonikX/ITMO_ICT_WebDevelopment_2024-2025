from rest_framework.permissions import BasePermission


class IsApprovedUser(BasePermission):
    """
    Allows access only to approved users.
    """

    def has_permission(self, request, view):
        user = request.user
        if user.is_authenticated:
            return user.is_approved if hasattr(user, "is_approved") else user.profile.is_approved
        return False
