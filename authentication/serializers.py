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
            'can_data_be_shared'
            ]


class RegisterSerializer(ModelSerializer):

    # password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    # password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'password',
            # 'password2',
            'age',
            'can_be_contacted',
            'can_data_be_shared'
            )

    def validate(self, attrs):
        if attrs['age'] < 15:
            raise ValidationError({"age": "L'âge minimu requis est de 15 ans"})

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
