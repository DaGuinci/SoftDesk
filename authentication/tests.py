from django.urls import reverse_lazy
# from django.contrib.auth.hashers import make_password

from rest_framework.test import (APITestCase,
                                 APIClient,
                                 )

from authentication.models import User

# Mise en place des datas pour test
class AuthAPITestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):
        # Création de deux users
        cls.user = User.objects.create(
            username='hector',
            password='passwordTest',
            age=17,
            can_be_contacted=False,
            can_data_be_shared=False,
            )
        cls.user2 = User.objects.create(
            username='achille',
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

    @classmethod
    def expected_reponses_content(self, test):
        if test == 'can_register':
            return {
                'username': 'Ulysse',
                'age': 16,
                'can_be_contacted': True,
                'can_data_be_shared': False
            }
        if test == 'is_too_young':
            return {'age': ["L'âge minimum requis est de 15 ans"]}
        if test == 'unauthenticated':
            return {'detail': "Informations d'authentification non fournies."}
        if test == 'modified_profile':
            return {
            'username': 'hector',
            'age': 27,
            'can_be_contacted': True,
            'can_data_be_shared': False
            }
        return None

    @classmethod
    def check_in_terminal(self, items):
        print('----------------- Comparing values -----------------')
        for item in items:
            print(item)


class UserTestCases(AuthAPITestCase):
    client = APIClient()
    # factory = APIRequestFactory()

    # Création d'un utilisateur
    def test_can_register(self):
        url = reverse_lazy('auth_register')
        response = self.client.post(url, {
            'username': 'Ulysse',
            'password': 'personne',
            'age': 16,
            'can_be_contacted': True,
            'can_data_be_shared': False
            }, format='json')
        response.json().pop('password')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(),
                         self.expected_reponses_content('can_register'))

    # Création d'un utilisateur trop jeune
    def test_is_too_young(self):
        url = reverse_lazy('auth_register')
        response = self.client.post(url, {
            'username': 'Ulysse',
            'password': 'personne',
            'age': 14,
            'can_be_contacted': True,
            'can_data_be_shared': False
            }, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
                         self.expected_reponses_content('is_too_young'))

    # Visualisation et modification de profil utilisateur
    def test_can_view_profile(self):
        hector = User.objects.get(username='hector')
        url = reverse_lazy('user-detail', kwargs={'pk' : hector.id, })

        # depuis user non authentifié
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)

        # depuis autre user non authentifié
        achille = User.objects.get(username='achille')
        self.client.force_authenticate(user=achille)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

        # depuis user sur son profil
        self.client.force_authenticate(user=hector)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    # test des update
    def test_can_update_profile(self):
        post_data = {
            'username': 'hector',
            'password': 'passwordTest',
            'age': 27,
            'can_be_contacted': True,
            'can_data_be_shared': False
            }
        hector = User.objects.get(username='hector')
        url = reverse_lazy('user-detail', kwargs={'pk' : hector.id, })

        # test methode post
        response = self.client.post(url, post_data, format='json')
        self.assertEqual(response.status_code, 405)

        # sans authentification
        response = self.client.patch(url, post_data, format='json')
        self.assertEqual(response.status_code, 401)

        # depuis autre user
        achille = User.objects.get(username='achille')
        self.client.force_authenticate(user=achille)
        response = self.client.patch(url, post_data, format='json')
        self.assertEqual(response.status_code, 403)

        # depuis user lui-même
        self.client.force_authenticate(user=hector)
        response = self.client.patch(url, post_data, format='json')
        response.json().pop('id')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
                         self.expected_reponses_content('modified_profile'))

    # test de l'appel de liste d'users
    def test_can_get_users_list(self):
        url = reverse_lazy('user-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            self.get_user_list_data([self.user, self.user2])
            )
