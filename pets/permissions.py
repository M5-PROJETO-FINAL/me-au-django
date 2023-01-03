from rest_framework import permissions
from rest_framework.views import Request, View
from pets.models import Pet



class IsAdminOrPetOwner(permissions.BasePermission):
    def has_object_permission(self, request: Request, view: View, obj: Pet):
        return request.user == obj.user_id or request.user.is_adm == True