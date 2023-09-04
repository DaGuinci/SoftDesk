from rest_framework.serializers import (
    ModelSerializer,
    ValidationError
    )

from authentication.models import User


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'age',
            'can_be_contacted',
            'can_data_be_shared',
            ]
        extra_kwargs = {"password": {"write_only": True}}

    def __str__(self):
        return self.username

    # def __repr__(self):
    #     return self.username



class RegisterSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username',
            'password',
            'age',
            'can_be_contacted',
            'can_data_be_shared'
            )

    def validate(self, attrs):
        if attrs['age'] < 15:
            raise ValidationError({"age": "L'âge minimum requis est de 15 ans"})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            age=validated_data['age'],
            can_be_contacted=validated_data['can_be_contacted'],
            can_data_be_shared=validated_data['can_data_be_shared']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user
