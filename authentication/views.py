from rest_framework.viewsets import ModelViewSet

from authentication.models import User
from authentication.serializers import UserSerializer, RegisterSerializer
from authentication.permissions import UserPermission

from drf_spectacular.utils import extend_schema_view, extend_schema

from rest_framework.generics import CreateAPIView

@extend_schema_view(
    list=extend_schema(
        summary="Récupérer tous les profils.",
        description="Autorisation: superuser.",
    ),
    retrieve=extend_schema(
        summary="Récupérer un profil.",
        description="Autorisation: superuser, propriétaire du profil.",
    ),
    partial_update=extend_schema(
        description="Autorisation: superuser, propriétaire du profil.",
    ),
    destroy=extend_schema(
        description="Autorisation: superuser, propriétaire du profil.",
    ),
)
class UserViewset(ModelViewSet):
    permission_classes = [UserPermission]

    http_method_names = ['get', 'patch', 'delete']

    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.all()


class RegisterView(CreateAPIView):
    """
        Ajoute un utilisateur.
        L'age doit être de 15 ans minimum.

        Autorisation: sans restriction.
    """

    queryset = User.objects.all()

    serializer_class = RegisterSerializer