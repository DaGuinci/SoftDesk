from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from api.models import Project, Contributing, Issue, Comment

UserModel = get_user_model()

USERS = [
    {
        'username': 'string',
        'password': 'string',
    },
    {
        'username': 'Achille',
        'password': 'string',
    },
    {
        'username': 'Hector',
        'password': 'string',
    },
    {
        'username': 'Ulysse',
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

        achille = UserModel.objects.get(username='Achille')
        hector = UserModel.objects.get(username='Hector')
        ulysse = UserModel.objects.get(username='Ulysse')

        # Création de projets
        first_project = Project.objects.create(
            title='Prendre Troie',
            description='Récupérer Hélène',
            type='FE',
            author_id=achille.id
        )

        Project.objects.create(
            title='Survivre',
            description='Résister aux Grecs',
            type='IO',
            author_id=hector.id
        )

        # Ajout d'un contributeur
        first_project.contributors.add(ulysse)

        # Création d'une issue
        first_issue = Issue.objects.create(
            author=ulysse,
            title='Artemis semble em colère',
            description='Agamemnon l\'a provoquée',
            status='TD',
            priority='MD',
            assigned_to=achille,
            tag='TAS',
            project=first_project
        )


        # Création d'un superuser
        UserModel.objects.create_superuser(ADMIN_ID, 'admin@oc.drf', ADMIN_PASSWORD)

        self.stdout.write(self.style.SUCCESS("All Done !"))
