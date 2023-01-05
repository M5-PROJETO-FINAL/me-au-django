from rest_framework import permissions
from .models import Service
from rest_framework.views import View


class IsAccountOwner(permissions.BasePermission):
    def has_object_permission(self, request, view: View, obj: Service) -> bool:
        return request.user.is_authenticated and obj == request.user or request.user.is_authenticated and request.user.is_adm == True


class IsAdm(permissions.BasePermission):
    def has_object_permission(self, request, view: View, obj: Service) -> bool:
        return request.user.is_authenticated and request.user.is_adm == True
