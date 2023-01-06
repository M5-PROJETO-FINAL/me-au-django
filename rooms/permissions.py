from rest_framework import permissions
from users.models import User
from rest_framework.views import View


class IsAccountOwner(permissions.BasePermission):
    def has_object_permission(self, request, view: View, obj: User) -> bool:
        return request.user.is_authenticated and obj == request.user


class IsAdm(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_adm)


SAFE_METHODS = ("GET", "HEAD", "OPTIONS")


class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or request.user and request.user.is_adm
        )
