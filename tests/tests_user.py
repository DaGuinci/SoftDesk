from django.urls import reverse_lazy

from authentication.models import User

from .tests_datas_setup import TestSetupAPITestCase


# Mise en place des datas pour test
class AuthAPITestCase(TestSetupAPITestCase):

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

    def expected_reponses_content(self, test):
        if test == 'can_register':
            return {
                'username': 'agamemnon',
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


class UserTestCases(AuthAPITestCase):

    # Création d'un utilisateur
    def test_can_register(self):
        url = reverse_lazy('auth_register')
        response = self.client.post(url, {
            'username': 'agamemnon',
            'password': 'pass',
            'age': 16,
            'can_be_contacted': True,
            'can_data_be_shared': False
            }, format='json')
        response.json().pop('password')
        self.assertEqual(response.status_code, 201)  # 201 Created
        self.assertEqual(response.json(),
                         self.expected_reponses_content('can_register'))

    # Création d'un utilisateur trop jeune
    def test_is_too_young(self):
        url = reverse_lazy('auth_register')
        response = self.client.post(url, {
            'username': 'agamemnon',
            'password': 'pass',
            'age': 14,
            'can_be_contacted': True,
            'can_data_be_shared': False
            }, format='json')
        self.assertEqual(response.status_code, 400)  # 400 Bad Request
        self.assertEqual(response.json(),
                         self.expected_reponses_content('is_too_young'))

    # Visualisation et modification de profil utilisateur
    def test_can_view_profile(self):
        url = reverse_lazy('user-detail', kwargs={'pk': self.hector.id, })

        # depuis user non authentifié
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)  # 401 Unauthorized

        # depuis autre user non authentifié
        self.client.force_authenticate(user=self.achille)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)  # 403 Forbidden

        # depuis user sur son profil
        self.client.force_authenticate(user=self.hector)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)  # 200 OK

    # test des update
    def test_can_update_profile(self):
        post_data = {
            'username': 'hector',
            'password': 'passwordTest',
            'age': 27,
            'can_be_contacted': True,
            'can_data_be_shared': False
            }
        url = reverse_lazy('user-detail', kwargs={'pk': self.hector.id, })

        # test methode post
        response = self.client.post(url, post_data, format='json')
        self.assertEqual(response.status_code, 405)  # 405 Method Not Allowed

        # sans authentification
        response = self.client.patch(url, post_data, format='json')
        self.assertEqual(response.status_code, 401)

        # depuis autre user
        self.client.force_authenticate(user=self.achille)
        response = self.client.patch(url, post_data, format='json')
        self.assertEqual(response.status_code, 403)

        # depuis user lui-même
        self.client.force_authenticate(user=self.hector)
        response = self.client.patch(url, post_data, format='json')
        response.json().pop('id')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
                         self.expected_reponses_content('modified_profile'))

    # test de suppression
    def test_can_delete_profile(self):
        url = reverse_lazy('user-detail', kwargs={'pk': self.hector.id, })

        # user non authentifié
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 401)

        # autre user
        self.client.force_authenticate(user=self.achille)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 403)

        # lui même
        self.client.force_authenticate(user=self.hector)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)  # 204 Ok, No Content
        # l'user est il bien supprimé ?
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)  # 404 Not Found

    # test de l'appel de liste d'users
    def test_can_get_users_list(self):
        url = reverse_lazy('user-list')
        response = self.client.get(url)
        ulysse = User.objects.get(username='ulysse')
        self.assertEqual(response.status_code, 200)
        # self.assertEqual(
        #     response.json(),
        #     self.get_user_list_data([self.hector, self.achille, ulysse])
        #     )
