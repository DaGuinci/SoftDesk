from django.urls import reverse_lazy

from rest_framework.test import APITestCase

from authentication.models import User


class AuthAPITestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):
        # Créons deux catégories dont une seule est active
        cls.user = User.objects.create(
            username='userTest',
            password='passwordTest',
            age=32,
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


class TestUser(AuthAPITestCase):
    url = reverse_lazy('user-list')

    # test de l'appel de liste d'users
    def test_create_no_admin(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), self.get_user_list_data([self.user, self.user2]))