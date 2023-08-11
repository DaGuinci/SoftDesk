from rest_framework.serializers import ModelSerializer

from api.models import Project


class ProjectSerializer(ModelSerializer):

    class Meta:
        model = Project
        fields = ['author', 'description', 'type', 'created_time']
