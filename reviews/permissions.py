from rest_framework import permissions
from users.models import User
from rest_framework.views import View


class IsAccountOwnerReview(permissions.BasePermission):
    def has_object_permission(self, request, view: View, obj: User) -> bool:
        return request.user.is_authenticated and obj.user == request.user