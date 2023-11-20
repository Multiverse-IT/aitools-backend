from rest_framework import permissions
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomIdentityHeaderPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        # Get the identity from the headers
        identity = request.headers.get("identity")

        # If identity is not present, deny permission
        if not identity:
            return False

        # Check if the identity corresponds to a valid user
        user = User.objects.filter(id=identity).first()

        # If user is found, grant permission
        return user is not None