from rest_framework import permissions
from .models import User
from rest_framework.views import View
import ipdb


class IsAuthenticatedOrPost(permissions.BasePermission):
    def has_permission(self, request, view: View) -> bool:
        if request.method == "POST":
            return True
        return request.user.is_authenticated


class IsAccountOwner(permissions.BasePermission):
    def has_object_permission(self, request, view: View, obj: User) -> bool:
        return request.user.is_authenticated and obj == request.user


class IsAdm(permissions.BasePermission):
    def has_permission(self, request, view: View) -> bool:
        return request.user.is_authenticated and request.user.is_adm
