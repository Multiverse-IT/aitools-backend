from rest_framework import permissions
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomIdentityHeaderPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        identity = request.headers.get("identity")
        if not identity:
            return False

        user = User.objects.filter(id=identity).first()
        return user is not None