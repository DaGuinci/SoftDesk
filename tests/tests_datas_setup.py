from rest_framework.test import APITestCase

from rest_framework.test import APIClient

from authentication.models import User

from django.contrib.auth import get_user_model


from api.models import (
    Project,
    Contributing,
    Issue,
    Comment
    )


# Mise en place des datas pour test

class TestSetupAPITestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()

        # Création de deux users
        UserModel = get_user_model()
        cls.zeus = UserModel.objects.create_superuser('Zeus', 'admin@oc.drf', 'olympe')

        cls.hector = User.objects.create(
            username='hector',
            password='passwordTest',
            age=17,
            can_be_contacted=False,
            can_data_be_shared=False,
            )
        cls.achille = User.objects.create(
            username='achille',
            password='passwordTest',
            age=28,
            can_be_contacted=True,
            can_data_be_shared=True,
            )

        cls.ulysse = User.objects.create(
            username='ulysse',
            password='passwordTest',
            age=28,
            can_be_contacted=True,
            can_data_be_shared=True,
            )

        # Création de projet
        cls.project_1 = Project.objects.create(
            title='Prise de Troie',
            author=cls.achille,
            description='Récupérer Hélène',
            type='FE'
        )

        # Nomination d'un contributeur
        cls.contributing = Contributing.objects.create(
            contributor=cls.ulysse,
            project=cls.project_1
        )

        # Creation d'un issue
        cls.issue_1 = Issue.objects.create(
            author=cls.ulysse,
            title='Artemis semble em colère',
            description='Agamemnon l\'a provoquée',
            status='TD',
            priority='MD',
            assigned_to=cls.achille,
            tag='TAS',
            project=cls.project_1
        )

        # Creation d'un comment
        cls.comment_1 = Comment.objects.create(
            author=cls.achille,
            description='Des nouvelles de Patrocle ?',
            issue=cls.issue_1,
        )

    @classmethod
    def check_in_terminal(self, items):
        print('----------------- Comparing values -----------------')
        for item in items:
            print(item)