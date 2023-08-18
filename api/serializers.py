from rest_framework.serializers import ModelSerializer

from api.models import (
    Project,
    Contributing,
    Issue,
    Comment)


class PostSerializer(ModelSerializer):

    def set_user(self):
        request = self.context.get("request", None)
        if request:
            return request.user


class ProjectSerializer(PostSerializer):

    class Meta:
        model = Project
        fields = '__all__'
        read_only_fields = ("author", "id")

    def create(self, validated_data):

        project = Project.objects.create(
            title=validated_data["title"],
            description=validated_data["description"],
            type=validated_data["type"],
            author=self.set_user(),
        )

        project.save()

        return project


class ContributorSerializer(ModelSerializer):

    class Meta:
        model = Contributing
        fields = ['contributor']


class IssueSerializer(PostSerializer):

    class Meta:
        model = Issue
        fields = '__all__'
        read_only_fields = ("author", "id")

    def create(self, validated_data):

        issue = Issue.objects.create(
            title=validated_data["title"],
            description=validated_data["description"],
            status=validated_data["status"],
            priority=validated_data["priority"],
            assigned=validated_data["assigned"],
            tag=validated_data["tag"],
            project=validated_data["project"],

            author=self.set_user(),
        )

        issue.save()

        return issue


class CommentSerializer(ModelSerializer):

    class Meta:
        model = Comment
        fields = '__all__'

    def set_user(self):
        request = self.context.get("request", None)
        if request:
            return request.user

    def create(self, validated_data):

        comment = Issue.objects.create(
            title=validated_data["title"],
            description=validated_data["description"],
            uuid=validated_data["uuid"],
            issue=validated_data["issue"],

            author=self.set_user(),
        )
        # Vrefifier que l'user est bien contributeur
        comment.save()

        return comment