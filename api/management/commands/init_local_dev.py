from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model, authenticate, login
from requests import request
# from django.contrib.auth.models import get_user_model

from api.models import Project, Contributing

UserModel = get_user_model()

USERS = [
    {
        'username': 'string',
        'password': 'string',
    },
    {
        'username': 'John',
        'password': 'string',
    },
    {
        'username': 'Ringo',
        'password': 'string',
    },
]

ADMIN_ID = 'admin-oc'
ADMIN_PASSWORD = 'password-oc'


class Command(BaseCommand):

    help = 'Initialize project for local development'

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING(self.help))

        UserModel.objects.all().delete()
        Project.objects.all().delete()
        Contributing.objects.all().delete()

        # Création des utilisateurs
        for user in USERS:
            UserModel.objects.create_user(username=user['username'], password=user['password'])

        # exit()
        john = UserModel.objects.get(username='John')
        ringo = UserModel.objects.get(username='Ringo')
        string = UserModel.objects.get(username='string')

        # Création de projets
        first_project = Project.objects.create(
            title='Premier projet',
            description='Description du premier projet',
            type='FE',
            author_id=string.id
        )

        Project.objects.create(
            title='Second projet',
            description='Description du deuxième projet',
            type='IO',
            author_id=ringo.id
        )

        # Création de contributeurs
        Contributing.objects.create(
            contributor_id=john.id,
            project_id=first_project.id
        )

        UserModel.objects.create_superuser(ADMIN_ID, 'admin@oc.drf', ADMIN_PASSWORD)

        self.stdout.write(self.style.SUCCESS("All Done !"))
