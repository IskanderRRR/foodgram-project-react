from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS, BasePermission


class ReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class IsAuthorOrAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated or request.method in SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser or obj.author == request.user:
            return True
        return request.method in SAFE_METHODS
