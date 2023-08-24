from django.urls import reverse_lazy

from .tests_datas_setup import TestSetupAPITestCase

from api.models import User

# Mise en place des datas pour test
class ApiAPITestCase(TestSetupAPITestCase):

    pass


class CommentTestCases(ApiAPITestCase):

    def test_add_comment(self):

        url = reverse_lazy('comment-list')
        post_datas = {
            'description': 'Parti discuter avec Hector.',
            'issue': self.issue_1.id
        }
        self.client.force_authenticate(user=self.ulysse)
        response = self.client.post(url, post_datas, format='json')
        self.assertEqual(response.status_code, 201)  # 201 Created

        # Create by a non contributor
        self.client.force_authenticate(user=self.hector)
        post_datas['description'] = 'Vous ne le reverrez plus.'
        response = self.client.post(url, post_datas, format='json')
        self.assertEqual(response.status_code, 403)  # 403 Forbidden

    def test_get_comments_list(self):
        url = reverse_lazy('comment-list')

        # Unauthentified
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401) # 401 Unauthorized

        # Authentified
        self.client.force_authenticate(user=self.hector)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403) # 403 Forbidden

        # Superuser
        self.client.force_authenticate(user=self.zeus)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200) # 200 OK

    def test_get_issue_comments_list(self):
        url = reverse_lazy('issue-get_comments', kwargs={'pk': self.issue_1.id})

        # Unauthentified
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401) # 401 Unauthorized

        # Authentified not contributor
        self.client.force_authenticate(user=self.hector)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403) # 403 Forbidden

        # Authentified contributor
        self.client.force_authenticate(user=self.ulysse)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200) # 200 OK

    def test_get_comment(self):
        url = reverse_lazy('comment-detail', kwargs={'pk': self.comment_1.id})

        # Unauthentified
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401) # 401 Unauthorized

        # Authentified not contributor
        self.client.force_authenticate(user=self.hector)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403) # 403 Forbidden

        # Authentified contributor
        self.client.force_authenticate(user=self.ulysse)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200) # 200 OK

    def test_update_comment(self):
        url = reverse_lazy('comment-detail', kwargs={'pk': self.comment_1.id})
        post_datas = {
            'description': 'Des nouvelles de Patrocle ? Je suis inquiet',
        }

        # Unauthentified
        response = self.client.put(url, post_datas)
        self.assertEqual(response.status_code, 401) # 401 Unauthorized

        # Authentified not contributor
        self.client.force_authenticate(user=self.hector)
        response = self.client.put(url, post_datas)
        self.assertEqual(response.status_code, 403) # 403 Forbidden

        # Authentified contributor
        self.client.force_authenticate(user=self.ulysse)
        response = self.client.put(url, post_datas)
        self.assertEqual(response.status_code, 403) # 403 Forbidden

        # Authentified comment's author
        self.client.force_authenticate(user=self.achille)
        response = self.client.patch(url, post_datas)
        self.assertEqual(response.status_code, 200) # 200 OK
        self.assertEqual(
            response.data['description'],
            'Des nouvelles de Patrocle ? Je suis inquiet'
            )

    def test_delete_comment(self):
        url = reverse_lazy('comment-detail', kwargs={'pk': self.comment_1.id})

        # Unauthentified
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 401) # 401 Unauthorized

        # Authentified not contributor
        self.client.force_authenticate(user=self.hector)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 403) # 403 Forbidden

        # Authentified contributor not author
        self.client.force_authenticate(user=self.ulysse)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 403) # 403 Forbidden

        # Authentified contributor author
        self.client.force_authenticate(user=self.achille)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204) # 204 No content