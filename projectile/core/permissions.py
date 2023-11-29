from rest_framework import permissions

from .choices import UserRole


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if user.is_active:
            return user.role in [
                UserRole.ADMIN,
                UserRole.OWNER
            ]
        return False
