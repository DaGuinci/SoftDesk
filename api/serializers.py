from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from api.models import (
    User,
    Project,
    Contributing,
    Issue,
    Comment)


class PostSerializer(ModelSerializer):

    def set_user(self):
        request = self.context.get('request', None)
        if request:
            return request.user


class ProjectSerializer(PostSerializer):

    contributors = serializers.StringRelatedField(many=True)
    author = serializers.StringRelatedField(many=False)

    class Meta:
        model = Project
        fields = [
            'id',
            'title',
            'author',
            'description',
            'contributors',
            'type',
            'created_time'
        ]
        read_only_fields = ['author']

    def create(self, validated_data):
        validated_data['author'] = self.set_user()

        return super(ProjectSerializer, self).create(validated_data)


class ContributorSerializer(ModelSerializer):

    class Meta:
        model = Contributing
        fields = ['contributor']


class IssueSerializer(PostSerializer):

    # S'assurer que l'issue est attribuée à un contributeur
    def validate_assigned_to(self, value):
        if value:
            project = Project.objects.get(id=self.initial_data['project'])
            if value not in project.contributors.all():
                raise serializers.ValidationError('Vous ne pouvez assigner une issue qu\'à un contributeur.')
        return value

    class Meta:
        model = Issue
        fields = '__all__'
        read_only_fields = ('author', 'id')

    def create(self, validated_data):
        validated_data['author'] = self.set_user()
        return super(IssueSerializer, self).create(validated_data)


class CommentSerializer(ModelSerializer):

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['author']

    def set_user(self):
        request = self.context.get('request', None)
        if request:
            return request.user

    def create(self, validated_data):
        validated_data['author'] = self.set_user()

        return super(CommentSerializer, self).create(validated_data)
