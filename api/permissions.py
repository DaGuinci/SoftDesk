from rest_framework.permissions import BasePermission

from api.models import Project, Contributing


class ProjectPermission(BasePermission):
    # TODO Ctte classe est elle vraiment utile ?
    def is_project_owner(self, request, projetc_id):
        project = projetc_id
        if project.author == request.user:
            return True
        return False


class IsProjectOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        if obj.author == request.user:
            return True
        return False


class IsContributor(BasePermission):

    def has_permission(self, request, view):
#         contributing = Contributing.objects.filter(
#             project_id=request.pk,
#             contributor_id=request.user.id
#             )

#         if contributing:
#             return True

        return False