from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrReadOnly(BasePermission):
    message = "You may only modify your own records."

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated) or \
               request.method in SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.created_by == request.user


class IsAdminRole(BasePermission):
    message = "Admin privileges required."

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated) and \
               getattr(request.user, 'profile', None) and \
               request.user.profile.role == 'A'
