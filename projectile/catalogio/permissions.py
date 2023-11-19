from rest_framework import permissions

class IsAuthenticatedOrReadOnlyForUserTool(permissions.BasePermission):
    """
    Custom permission to allow read-only access for unauthenticated users
    while requiring authentication for POST requests.
    """

    def has_permission(self, request, view):
        # Allowing read-only access for unauthenticated users
        if request.method in permissions.SAFE_METHODS:
            return True
        # Require authentication for POST requests
        return request.user and request.user.is_authenticated