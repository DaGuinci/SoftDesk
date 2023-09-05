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


class Command(BaseCommand):

    help = 'Initialize project for local development'

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING(self.help))

        UserModel.objects.all().delete()
        Project.objects.all().delete()
        Contributing.objects.all().delete()

        # Création des utilisateurs
        for user in USERS:
            UserModel.objects.create_user(
                username=user['username'],
                password=user['password']
                )

        achille = UserModel.objects.get(username='Achille')
        hector = UserModel.objects.get(username='Hector')
        ulysse = UserModel.objects.get(username='Ulysse')

        # Création de projets
        first_project = Project.objects.create(
            title='Prendre Troie',
            description='Récupérer Hélène.',
            type='FE',
            author_id=achille.id
        )

        Project.objects.create(
            title='Survivre à l\'attaque des Grecs',
            description='Résister aux Grecs.',
            type='IO',
            author_id=hector.id
        )

        # Ajout d'un contributeur
        first_project.contributors.add(ulysse)

        # Création d'issues
        first_issue = Issue.objects.create(
            author=achille,
            title='Patrocle ne revient pas',
            description='Quelqu\'un l\'a vu depuis ce matin ?',
            status='TD',
            priority='MD',
            assigned_to=achille,
            tag='TAS',
            project=first_project
        )

        Issue.objects.create(
            author=ulysse,
            title='Artemis semble em colère',
            description='Agamemnon l\'a provoquée',
            status='TD',
            priority='MD',
            assigned_to=achille,
            tag='TAS',
            project=first_project
        )

        Issue.objects.create(
            author=ulysse,
            title='Faire rentrer nos armées dans la ville',
            description='Trouver une astuce.',
            status='TD',
            priority='MD',
            assigned_to=achille,
            tag='TAS',
            project=first_project
        )

        Issue.objects.create(
            author=ulysse,
            title='Construire un cheval en bois',
            description='Si possible assez grand:',
            status='TD',
            priority='MD',
            assigned_to=achille,
            tag='TAS',
            project=first_project
        )

        Issue.objects.create(
            author=ulysse,
            title='Venger Patrocle',
            description='Voir avec Hector.',
            status='TD',
            priority='MD',
            assigned_to=achille,
            tag='TAS',
            project=first_project
        )

        # Création de commentaires
        Comment.objects.create(
            author=ulysse,
            description='Il n\'avait pas rendez-vous avec Hector, ce matin ?',
            issue=first_issue
        )

        Comment.objects.create(
            author=achille,
            description='C\'est bien ce qui m\'inquiète.\
                Hector est un peu soupe au lait.',
            issue=first_issue
        )

        Comment.objects.create(
            author=ulysse,
            description='Non, pas de souci, il aboie plus qu\'il ne mord.\
                Patrocle sera de retour pour le déjeuner.',
            issue=first_issue
        )

        Comment.objects.create(
            author=achille,
            description='Tu as raison. Surtout qu\'aujourd\'hui c\'est des\
                frites à la cantine, il ne raterait pas ça.',
            issue=first_issue
        )

        # Création d'un superuser
        # UserModel.objects.create_superuser('Zeus', 'admin@oc.drf', 'string')
        UserModel.objects.create_superuser(username='Zeus', password='string')

        self.stdout.write(self.style.SUCCESS("All Done !"))
