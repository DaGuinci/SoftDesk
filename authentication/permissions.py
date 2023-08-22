from rest_framework.permissions import BasePermission


class IsAuthenticated(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)


class CanModifyUser(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated and request.user.is_superuser:
            return True
        if request.user == obj:
            return True

        return False
