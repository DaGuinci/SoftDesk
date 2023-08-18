from rest_framework.permissions import BasePermission

from api.models import Project, Contributing


class ProjectPermissions(BasePermission):
    # TODO Ctte classe est elle vraiment utile ?
    def has_object_permission(self, request, view, obj):
        if view.action in ['create']:
            return request.user.is_authenticated
        elif view.action in ['retrieve']:
            return request.user in obj.get_contributors()
        elif view.action in ['update', 'partial_update', 'destroy']:
            return obj.author == request.user
        else:
            return False


# class IsProjectOwner(BasePermission):

#     def has_object_permission(self, request, view, obj):
#         if obj.author == request.user:
#             return True
#         return False


# class IsContributor(BasePermission):

#     def has_permission(self, request, view):
# #         contributing = Contributing.objects.filter(
# #             project_id=request.pk,
# #             contributor_id=request.user.id
# #             )

# #         if contributing:
# #             return True

#         return False