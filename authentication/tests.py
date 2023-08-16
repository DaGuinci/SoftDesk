from django.urls import reverse_lazy

from rest_framework.test import APITestCase, APIRequestFactory, APIClient

from authentication.models import User

# Mise en place des datas pour test
class AuthAPITestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):
        # Création de deux users
        cls.user = User.objects.create_user(
            username='userTest',
            password='passwordTest',
            age=14,
            can_be_contacted=False,
            can_data_be_shared=False,
            )
        cls.user2 = User.objects.create(
            username='userTest2',
            password='passwordTest',
            age=28,
            can_be_contacted=True,
            can_data_be_shared=True,
            )

    def get_user_list_data(self, users):

        return [
            {
                'id': user.id,
                'username': user.username,
                'age': user.age,
                'can_be_contacted': user.can_be_contacted,
                'can_data_be_shared': user.can_data_be_shared,
            } for user in users
        ]


class UserTestCases(AuthAPITestCase):

    # Création d'un utilisateur
    def test_can_register(self):
        url = reverse_lazy('auth_register')
        self.client = APIClient()
        response = self.client.post(url, {
            'username': 'Ulysse',
            'password': 'personne',
            'age': 16,
            'can_be_contacted': True,
            'can_data_be_shared': False
            }, format='json')
        # response = self.client.get(url)
        print('------response-----------')
        print(response.data)
        self.assertEqual(response.status_code, 201)
        # self.assertEqual(response.json(), self.get_user_list_data([self.user, self.user2]))

    # test de l'appel de liste d'users
    def test_can_get_users_list(self):
        url = reverse_lazy('user-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), self.get_user_list_data([self.user, self.user2]))

    # modifier un user
    def unauthorized_user_cant_patch(self):
        # factory = APIRequestFactory()
        # request = factory.post('/notes/', {'title': 'new idea'})
        pass