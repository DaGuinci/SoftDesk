from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status

from authentication.permissions import (
    IsAuthenticated,
    )
from api.permissions import (
    CanModifyProject,
    IsContributor
)

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

    permission_classes = [IsAuthenticated, CanModifyProject]

    serializer_class = ContributeSerializer

    http_method_names = ['post', 'patch']
    # Supprimer un llien projet contributeur à partir
    # des id projet et contributeur
    @action(methods=['patch'], detail=False,
            url_path='delete', url_name='delete_contributor')
    def delete(self, request, project=None, contributor=None):
        project = request.data['project']
        contributor = request.data['contributor']
        contributing = Contributing.objects.filter(project=project, contributor=contributor)
        contributing.delete()
        return Response(status=status.HTTP_202_ACCEPTED)

    def get_queryset(self):
        queryset = Contributing.objects.all()
        return queryset


class IssueViewset(ModelViewSet):

    permission_classes = [IsAuthenticated, IsContributor]

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