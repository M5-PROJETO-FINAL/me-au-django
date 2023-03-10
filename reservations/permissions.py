from rest_framework import permissions
from .models import Reservation
from rest_framework.views import View


class IsAccountOwner(permissions.BasePermission):
    def has_object_permission(self, request, view: View, obj: Reservation) -> bool:
        return request.user.is_authenticated and obj.user == request.user


class IsAdm(permissions.BasePermission):
    def has_permission(self, request, view: View) -> bool:
        return request.user.is_authenticated and request.user.is_adm
