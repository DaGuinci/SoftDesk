from rest_framework.permissions import BasePermission

from api.models import Project, Issue


class IsProjectContributor():

    def is_contributor(self, user, project):
        return user in project.contributors.all()


class ProjectPermissions(BasePermission):

    def has_permission(self, request, view):
        if view.action in ['list']:
            return request.user.is_authenticated and request.user.is_superuser
        return super().has_permission(request, view)

    def has_object_permission(self, request, view, obj):
        if view.action in ['create']:
            return request.user.is_authenticated
        elif view.action in [
                'retrieve',
                'get_project_issues'
                ]:
            return request.user in list(obj.contributors.all()) or request.user.is_superuser
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
        if view.action in ['create']:
            project = Project.objects.get(id=request.data['project'])
            if request.user not in project.contributors.all():
                self.message = 'Permissions refusée: vous devez être contributeur du projet'
                return False
            else:
                return True
        elif view.action == 'list':
            return request.user.is_authenticated and request.user.is_superuser
        else:
            return view.action in ['retrieve', 'update', 'partial_update', 'destroy', 'get_issue_comments']

    def has_object_permission(self, request, view, obj):
        if view.action in ['retrieve', 'get_issue_comments']:
            return self.is_contributor(request.user, obj.project)
        elif view.action in ('update', 'partial_update', 'destroy'):
            return obj.author == request.user
        return False


class CommentPermissions(BasePermission, IsProjectContributor):

    # message = 'You must be the owner of this object.'
    def has_permission(self, request, view):
        if view.action == 'create':
            issue = Issue.objects.get(id=request.data['issue'])
            if request.user not in issue.project.contributors.all():
                self.message = 'Permissions refusée: vous devez être contributeur du projet'
                return False
            else:
                return True
        elif view.action == 'list':
            return request.user.is_authenticated and request.user.is_superuser
        else:
            return view.action in ['retrieve', 'update', 'partial_update', 'destroy']

    def has_object_permission(self, request, view, obj):
        if view.action == 'retrieve':
            return self.is_contributor(request.user, obj.issue.project)
        if view.action in ('update', 'partial_update', 'destroy'):
            return obj.author == request.user
        return False