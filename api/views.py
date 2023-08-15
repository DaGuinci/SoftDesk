from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action

from authentication.permissions import IsAuthenticated, CanModifyProject

from api.models import Project, Issue, Comment
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

    http_method_names = ['post', 'delete']

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