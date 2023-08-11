from rest_framework.viewsets import ModelViewSet

from authentication.permissions import IsAuthenticated

from api.models import Project
from api.serializers import ProjectSerializer


class ProjectViewset(ModelViewSet):

    permission_classes = [IsAuthenticated]

    serializer_class = ProjectSerializer

    def get_queryset(self):
        queryset = Project.objects.all()
        return queryset