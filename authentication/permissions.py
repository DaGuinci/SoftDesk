from rest_framework.permissions import BasePermission

from api.models import Project


# class IsAdminAuthenticated(BasePermission):

#     def has_permission(self, request, view):
#         return bool(request.user and request.user.is_authenticated and request.user.is_superuser)
class ProjectPermission(BasePermission):

    def is_project_owner(self, request):
        project = Project.objects.get(id=request.data['project'])
        if project.author == request.user:
            return True
        return False


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


class CanModifyProject(ProjectPermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated and self.is_project_owner(request):
            return True

        return False