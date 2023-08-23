from rest_framework.permissions import BasePermission

from api.models import Project, Contributing


class IsProjectContributor():

    def is_contributor(self, user, project):
        return user in project.contributors.all()


class ProjectPermissions(BasePermission):

    def has_object_permission(self, request, view, obj):
        if view.action in ['create']:
            return request.user.is_authenticated
        elif view.action in [
                'retrieve',
                'get_project_issues'
                ]:
            return request.user in list(obj.contributors.all())
        elif view.action in [
                'update',
                'partial_update',
                'destroy',
                'add_contributor',
                'remove_contributor']:
            return obj.author == request.user
        else:
            return False


class IssuePermissions(BasePermission, IsProjectContributor):
    # message = 'You must be the owner of this object.'
    def has_permission(self, request, view):
        if view.action == 'create':
            project = Project.objects.get(id=request.data['project'])
            if not request.user in project.contributors.all():
                self.message = 'Permissions refusée: vous devez être contributeur du projet'
                return False
            else:
                return True
        elif view.action == 'list':
            return request.user.is_authenticated and request.user.is_superuser
        else:
            return view.action in ['retrieve', 'update', 'partial_update', 'delete']

    def has_object_permission(self, request, view, obj):
        if view.action == 'retrieve':
            return self.is_contributor(request.user, obj.project)
        if view.action in ('update', 'partial_update', 'delete'):
            return obj.author == request.user
        return False