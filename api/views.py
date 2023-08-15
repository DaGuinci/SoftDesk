from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status

from authentication.permissions import IsAuthenticated, CanModifyProject

from api.models import Project, Issue, Comment, Contributing
from api.serializers import (
    ProjectSerializer,
    ContributeSerializer,
    IssueSerializer,
    CommentSerializer
    )


class ProjectViewset(ModelViewSet):

    permission_classes = [IsAuthenticated]

    serializer_class = ProjectSerializer

    def get_queryset(self):
        queryset = Project.objects.all()
        return queryset


class ContributeViewset(ModelViewSet):

    permission_classes = [CanModifyProject]

    serializer_class = ContributeSerializer

    http_method_names = ['post']

    @action(methods=['post'], detail=False,
            url_path='delete', url_name='change_password')
    def delete(self, request, project=None, contributor=None):
        project = request.data['project']
        contributor = request.data['contributor']
        contributing = Contributing.objects.filter(project=project, contributor=contributor)
        contributing.delete()
        return Response(status=status.HTTP_202_ACCEPTED)

    def get_queryset(self):
        queryset = Contributing.objects.all()
        return queryset


class DeleteContributorViewset(ModelViewSet):
    pass

class IssueViewset(ModelViewSet):

    permission_classes = [IsAuthenticated]

    serializer_class = IssueSerializer

    def get_queryset(self):
        queryset = Issue.objects.all()
        return queryset


class CommentViewset(ModelViewSet):

    permission_classes = [IsAuthenticated]

    serializer_class = CommentSerializer

    def get_queryset(self):
        queryset = Comment.objects.all()
        return queryset