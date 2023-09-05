from django.shortcuts import get_object_or_404

from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination

from authentication.permissions import (
    IsAuthenticated,
    )
from authentication.models import User

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

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 1000

class ProjectViewset(ModelViewSet):

    permission_classes = [IsAuthenticated, ProjectPermissions]
    pagination_class = StandardResultsSetPagination

    http_method_names = ['get', 'post', 'patch', 'delete']

    serializer_class = ProjectSerializer

    @action(methods=['patch'],
            detail=True,
            url_name='add_contributor',
            basename='add_contributor',
            serializer_class=ContributorSerializer,
            )
    def add_contributor(self, request, pk, contributor=None):
        new_contributor = get_object_or_404(User, pk=request.data['contributor'])
        if new_contributor not in self.get_object().contributors.all():
            self.get_object().contributors.add(request.data['contributor'])
            return Response('Contributeur ajouté')
        else:
            return Response('Cet utilisateur est déjà contributeur du projet.')

    @action(methods=['patch'],
            detail=True,
            url_name='remove_contributor',
            serializer_class=ContributorSerializer,
            )
    def remove_contributor(self, request, pk, contributor=None):
        new_contributor = get_object_or_404(User, pk=request.data['contributor'])
        if new_contributor in self.get_object().contributors.all():
            self.get_object().contributors.remove(request.data['contributor'])
            return Response('Contributeur supprimé')
        else:
            return Response('L\'utilisateur n\'est pas contributeur de ce projet.')


    @action(methods=['get'],
            detail=True,
            url_name='get_issues',
            url_path='get_issues',
            serializer_class=IssueSerializer,
            )
    def get_project_issues(self, request, pk):
        queryset = Issue.objects.filter(project=self.get_object())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        queryset = Project.objects.all()
        return queryset


class IssueViewset(ModelViewSet):

    permission_classes = [IsAuthenticated, IssuePermissions]
    pagination_class = StandardResultsSetPagination

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
    pagination_class = StandardResultsSetPagination

    serializer_class = CommentSerializer

    def get_queryset(self):
        queryset = Comment.objects.all()
        return queryset