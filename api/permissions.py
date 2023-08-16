# TODO demenager les perms
# class CanModifyProject(ProjectPermission):

#     def has_permission(self, request, view):
#         if request.user.is_authenticated and self.is_project_owner(request):
#             return True

#         return False


# class IsContributor(BasePermission):

#     def has_permission(self, request, view):
#         contributing = Contributing.objects.filter(
#             project_id=request.data['project'],
#             contributor_id=request.user.id
#             )

#         if contributing:
#             return True

#         return False