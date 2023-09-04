from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action

from authentication.permissions import (
    IsAuthenticated,
    )

from api.permissions import (
    ProjectPermissions,
    IssuePermissions,
    CommentPermissions
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

    http_method_names = ['get', 'post', 'patch', 'delete']

    serializer_class = ProjectSerializer

    @action(methods=['patch'],
            detail=True,
            url_name='add_contributor',
            basename='add_contributor',
            serializer_class=ContributorSerializer,
            )
    def add_contributor(self, request, pk, contributor=None):
        self.get_object().contributors.add(request.data['contributor'])
        return Response()

    @action(methods=['patch'],
            detail=True,
            url_name='remove_contributor',
            serializer_class=ContributorSerializer,
            )
    def remove_contributor(self, request, pk, contributor=None):
        self.get_object().contributors.remove(request.data['contributor'])
        return Response()

    @action(methods=['get'],
            detail=True,
            url_name='get_issues',
            url_path='get_issues',
            serializer_class=IssueSerializer,
            )
    def get_project_issues(self, request, pk):
        queryset = Issue.objects.filter(project=self.get_object())
        serializer = IssueSerializer(queryset, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        queryset = Project.objects.all()
        return queryset


class IssueViewset(ModelViewSet):

    permission_classes = [IsAuthenticated, IssuePermissions]

    serializer_class = IssueSerializer

    @action(methods=['get'],
            detail=True,
            url_name='get_comments',
            url_path='get_comments',
            serializer_class=CommentSerializer,
            )
    def get_issue_comments(self, request, pk):
        queryset = Comment.objects.filter(issue=self.get_object())
        serializer = CommentSerializer(queryset, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        queryset = Issue.objects.all()
        return queryset


class CommentViewset(ModelViewSet):

    permission_classes = [IsAuthenticated, CommentPermissions]

    serializer_class = CommentSerializer

    def get_queryset(self):
        queryset = Comment.objects.all()
        return queryset