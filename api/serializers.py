from rest_framework.serializers import ModelSerializer

from api.models import Project


class ProjectSerializer(ModelSerializer):

    class Meta:
        model = Project
        fields = "__all__"
        read_only_fields = ("author", "id")

    def _user(self):
        request = self.context.get("request", None)
        if request:
            return request.user

    def create(self, validated_data):

        project = Project.objects.create(
            # title=validated_data["title"],
            description=validated_data["description"],
            type=validated_data["type"],
            author=self._user(),
        )
        project.save()

        return project