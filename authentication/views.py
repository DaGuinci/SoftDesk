from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet

from authentication.models import User
from authentication.serializers import UserSerializer
from authentication.permissions import IsAdminAuthenticated


class UserViewset(ReadOnlyModelViewSet):

    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.all()


class AdminUserViewset(ModelViewSet):

    permission_classes = [IsAdminAuthenticated]

    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.all()