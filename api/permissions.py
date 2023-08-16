from rest_framework.permissions import BasePermission

from api.models import Project, Contributing


class ProjectPermission(BasePermission):
    # TODO Ctte classe est elle vraiment utile ?
    def is_project_owner(self, request):
        project = Project.objects.get(id=request.data['project'])
        if project.author == request.user:
            return True
        return False


class CanModifyProject(ProjectPermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated and self.is_project_owner(request):
            return True

        return False


class IsContributor(BasePermission):

    def has_permission(self, request, view):
        contributing = Contributing.objects.filter(
            project_id=request.data['project'],
            contributor_id=request.user.id
            )

        if contributing:
            return True

        return False