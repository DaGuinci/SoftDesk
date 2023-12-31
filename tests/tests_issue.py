from django.urls import reverse_lazy

from .tests_datas_setup import TestSetupAPITestCase

from api.models import User

# Mise en place des datas pour test
class ApiAPITestCase(TestSetupAPITestCase):

    pass


class IssueTestCases(ApiAPITestCase):

    def test_add_issue(self):

        url = reverse_lazy('issue-list')
        post_datas = {
            'title': 'test_issue',
            'description': 'string',
            'status': 'TD',
            'priority': 'LO',
            'tag': 'BUG',
            'project': self.project_1.id,
            'assigned_to': ''  # Ecrire null en toute lettre
        }
        self.client.force_authenticate(user=self.ulysse)
        response = self.client.post(url, post_datas, format='json')
        self.assertEqual(response.status_code, 201)  # 201 Created

        # Assign to non contriutor user
        post_datas['title'] = 'test_issue_2'
        post_datas['assigned_to'] = 2  # Hector's id
        response = self.client.patch(url, post_datas, format='json')
        self.assertEqual(response.status_code, 403)  # 403 Forbidden

        # Create by a non contributor
        self.client.force_authenticate(user=self.hector)
        response = self.client.post(url, post_datas, format='json')
        self.assertEqual(response.status_code, 403)  # 403 Forbidden

        # Assign to inexistant user
        post_datas['title'] = 'test_issue_2'
        post_datas['assigned_to'] = 27
        self.client.force_authenticate(user=self.achille)
        response = self.client.patch(url, post_datas, format='json')
        self.assertEqual(response.status_code, 403)  # 403 Forbidden


    def test_get_issue_list(self):
        url = reverse_lazy('issue-list')

        # Unauthentified
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401) # 401 Unauthorized

        # Authentified
        self.client.force_authenticate(user=self.hector)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200) # 200 OK
        # Superuser
        self.client.force_authenticate(user=self.zeus)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200) # 200 OK


    def test_get_project_issues_list(self):
        url = reverse_lazy('project-get_issues', kwargs={'pk': self.project_1.id})

        # Unauthentified
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401) # 401 Unauthorized

        # Authentified not contributor
        self.client.force_authenticate(user=self.hector)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200) # 200 OK

        # Authentified contributor
        self.client.force_authenticate(user=self.ulysse)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200) # 200 OK

    def test_get_issue(self):
        url = reverse_lazy('issue-detail', kwargs={'pk': self.issue_1.id})

        # Unauthentified
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401) # 401 Unauthorized

        # Authentified not contributor
        self.client.force_authenticate(user=self.hector)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200) # 200 OK

        # Authentified contributor
        self.client.force_authenticate(user=self.ulysse)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200) # 200 OK

    def test_update_issue(self):
        url = reverse_lazy('issue-detail', kwargs={'pk': self.issue_1.id})
        post_datas = {
            'title':'Artemis semble en colère',
            'description': 'Agamemnon l\'a provoquée',
            'status': 'PR',
            'priority': 'MD',
            'assigned_to': self.ulysse.id,
            'project': self.project_1.id,
            'tag': 'TAS',
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
        response = self.client.get(url, post_datas)
        # Á ce stade, l'issue est attribuée à achille
        self.assertEqual(
            User.objects.get(id=response.data['assigned_to']),
            User.objects.get(username='achille')
            )
        response = self.client.put(url, post_datas)
        self.assertEqual(response.status_code, 200) # 200 OK
        # L'user associé a été modifié pour Ulysse
        self.assertEqual(
            User.objects.get(id=response.data['assigned_to']),
            User.objects.get(username='ulysse')
            )

    def test_delete_issue(self):
        url = reverse_lazy('issue-detail', kwargs={'pk': self.issue_1.id})

        # Unauthentified
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 401) # 401 Unauthorized

        # Authentified not contributor
        self.client.force_authenticate(user=self.hector)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 403) # 403 Forbidden

        # Authentified contributor not author
        self.client.force_authenticate(user=self.achille)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 403) # 403 Forbidden

        # Authentified contributor author
        self.client.force_authenticate(user=self.ulysse)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204) # 204 No content