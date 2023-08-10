from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet

from authentication.models import User
from authentication.serializers import UserSerializer, RegisterSerializer
from authentication.permissions import IsAdminAuthenticated

from rest_framework.generics import CreateAPIView


class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    # TODO vérifier ligne suivante
    # permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

class UserViewset(ReadOnlyModelViewSet):

    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.all()


class AdminUserViewset(ModelViewSet):

    permission_classes = [IsAdminAuthenticated]

    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.all()
