from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status

from authentication.permissions import (
    IsAuthenticated,
    )
from api.permissions import (
    ProjectPermissions
)

from api.models import Project, Issue, Comment
from api.serializers import (
    ProjectSerializer,
    ContributorSerializer,
    IssueSerializer,
    CommentSerializer
    )


class ProjectViewset(ModelViewSet):

    permission_classes = [IsAuthenticated, ProjectPermissions]

    serializer_class = ProjectSerializer

    @action(methods=['put'],
            detail=True,
            url_name='add_contributor',
            serializer_class=ContributorSerializer,
            )
    def add_contributor(self, request, pk, contributor=None):
        # project = self.get_object()
        self.get_object().contributors.add(request.data['contributor'])
        return Response(status='Contributeur ajouté')

    @action(methods=['put'],
            detail=True,
            url_name='remove_contributor',
            serializer_class=ContributorSerializer,
            )
    def remove_contributor(self, request, pk, contributor=None):
        # TODO verif la suppression de manytomany
        self.get_object().remove_contributor(request.data['contributor'])
        return Response(status=status.HTTP_202_ACCEPTED)

    def get_queryset(self):
        queryset = Project.objects.all()
        return queryset


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