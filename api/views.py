from rest_framework.viewsets import ModelViewSet

from authentication.permissions import IsAuthenticated

from api.serializers import ProjectSerializer


class ProjectViewset(ModelViewSet):

    permission_classes = [IsAuthenticated]

    serializer_class = ProjectSerializer