from django.urls import reverse_lazy

from rest_framework.test import APIClient

from .tests_datas_setup import TestSetupAPITestCase


# Mise en place des datas pour test
class ApiAPITestCase(TestSetupAPITestCase):

    def get_project_list_data(self, projects):
        for project in projects:
            contributors = list(self.project_1.contributors.all())
            project.contributors_id = []
            for contributor in contributors:
                project.contributors_id.append(contributor.id)
        return [
            {
                'id': project.id,
                'title': project.title,
                'description': project.description,
                'type': project.type,
                'author': project.author.id,
                'contributors': project.contributors_id
            } for project in projects
        ]

    def expected_reponses_content(self, test):
        if test == 'get_project_1':
            contributors = list(self.project_1.contributors.all())
            contributors_id = []
            for contributor in contributors:
                contributors_id.append(contributor.id)
            return (
                {
                    'id': self.project_1.id,
                    'title': self.project_1.title,
                    'author': self.project_1.author.id,
                    'description': self.project_1.description,
                    'type': self.project_1.type,
                    'contributors': contributors_id
                }
            )
        if test == 'updated_project':
            contributors = list(self.project_1.contributors.all())
            contributors_id = []
            for contributor in contributors:
                contributors_id.append(contributor.id)
            return (
                {
                    'id': self.project_1.id,
                    'title': 'Venger Patrocle',
                    'description': 'Tuer Hector en faisant attention à mon talon',
                    'type': 'BE',
                    'author': self.project_1.author.id,
                    'contributors': contributors_id
                }
            )

        return None


class ProjectTestCases(ApiAPITestCase):

    def test_get_projects_list(self):
        url = reverse_lazy('project-list')

        # Non authentifié
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)  # 401 Unauthorized

        # Authentifié
        # TODO Etudier le niveau de detail accessible en liste
        self.client.force_authenticate(user=self.hector)
        response = self.client.get(url)
        for project in response.json():
            project.pop('created_time')
        self.assertEqual(response.status_code, 200)  # 200 OK
        self.assertEqual(response.json(),
                         self.get_project_list_data([self.project_1]))

    def test_get_project_details(self):
        url = reverse_lazy('project-detail', kwargs={'pk': self.project_1.id})

        # Non authentifié
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)  # 401 Unauthorized

        # Authentifié par autre user, non contributeur, non auteur
        self.client.force_authenticate(user=self.hector)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)  # 403 Forbidden

        # authentifié comme contributeur
        self.client.force_authenticate(user=self.ulysse)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)  # 200 OK

        # Authentifié comme auteur
        self.client.force_authenticate(user=self.achille)
        response = self.client.get(url)
        response.json().pop('created_time')
        self.assertEqual(response.status_code, 200)  # 200 OK
        self.assertEqual(response.json(),
                         self.expected_reponses_content('get_project_1'))

    def test_create_project(self):
        url = reverse_lazy('project-list')
        post_datas = {
            'title': 'Prise de Troie',
            'description': 'Récupérer Hélène',
            'type': 'FE'
        }

        # Non authentifié
        response = self.client.post(url, post_datas)
        self.assertEqual(response.status_code, 401)  # 401 Unauthorized

        # Authentifié
        self.client.force_authenticate(user=self.hector)
        response = self.client.post(url, post_datas)
        self.assertEqual(response.status_code, 201)  # 201 Created

    def test_update_project(self):
        url = reverse_lazy('project-detail', kwargs={'pk': self.project_1.id})
        post_datas = {
            'title': 'Venger Patrocle',
            'description': 'Tuer Hector en faisant attention à mon talon',
            'type': 'BE'
        }
        # Non authentifié
        response = self.client.put(url, post_datas)
        self.assertEqual(response.status_code, 401)  # 401 Unauthorized

        # Authentifié par autre user, non contributeur, non auteur
        self.client.force_authenticate(user=self.hector)
        response = self.client.put(url, post_datas)
        self.assertEqual(response.status_code, 403)  # 403 Forbidden

        # Authentifié comme auteur
        self.client.force_authenticate(user=self.achille)
        response = self.client.put(url, post_datas)
        response.json().pop('created_time')
        self.assertEqual(response.status_code, 200)  # 200 OK
        self.assertEqual(response.json(),
                         self.expected_reponses_content('updated_project'))
