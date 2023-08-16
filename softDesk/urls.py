"""softDesk URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
    )

from authentication.views import UserViewset, UserViewset, RegisterView
from api.views import (
    ProjectViewset,
    # ContributeViewset,
    IssueViewset,
    CommentViewset)

from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

# from rest_framework_swagger.views import get_swagger_view

# schema_view = get_swagger_view(title='Pastebin API')


authRouter = routers.SimpleRouter()
# Creer un user (tous)
# Modifier son profil
# Modifier un user (admin)
authRouter.register('user', UserViewset, basename='user')
# authRouter.register('admin/user', AdminUserViewset, basename='admin-user')

apiRouter = routers.SimpleRouter()

# Creer un nouveau projet (utilisateur)
apiRouter.register('project', ProjectViewset, basename='project')
# Ajouter un contributeur (auteur)
# Supprimer un contributeur (auteur)
# apiRouter.register('contributor', ContributeViewset, basename='contributor')

# Modifier le projet (auteur)

# Créer une issue (contributeur)
# Modifier une issue (auteur)
apiRouter.register('issue', IssueViewset, basename='issue')

# Créer un commentaire (contributeur)
# Modifier un commentaire (auteur)
apiRouter.register('comment', CommentViewset, basename='comment')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/register/', RegisterView.as_view(), name='auth_register'),
    # path('api-auth/', include('rest_framework.urls')),
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/', include(authRouter.urls)),
    path('api/', include(apiRouter.urls)),
    path('docs/swagger/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('docs/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]