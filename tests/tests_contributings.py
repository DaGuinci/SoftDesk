from django.urls import reverse_lazy

from rest_framework.test import APIClient

from .tests_datas_setup import TestSetupAPITestCase


# Mise en place des datas pour test
class ApiAPITestCase(TestSetupAPITestCase):

    def get_project_list_data(self, projects):
        return [
            {
                'id': project.id,
                'title': project.title,
                'description': project.description,
                'type': project.type,
                'author': project.author.id,
            } for project in projects
        ]

    def expected_reponses_content(self, test):
        if test == 'get_project_1':
            return (
                {
                    'id': self.project_1.id,
                    'title': self.project_1.title,
                    'author': self.project_1.author.id,
                    'description': self.project_1.description,
                    'type': self.project_1.type,
                }
            )
        if test == 'updated_project':
            return (
                {
                    'id': self.project_1.id,
                    'title': 'Venger Patrocle',
                    'author': self.project_1.author.id,
                    'description': 'Tuer Hector en faisant attention à mon talon',
                    'type': 'BE',
                }
            )

        return None


class ProjectTestCases(ApiAPITestCase):

    def test_get_contributors_by_project(self):
        contributors = self.project_1.get_contributors()
        self.assertEqual(contributors, [self.achille, self.ulysse])

    def test_access_contributed_project(self):
        url = reverse_lazy('project-detail', kwargs={'pk': self.project_1.id})

        # Get
        self.client.force_authenticate(user=self.ulysse)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)  # 200 OK

        #




    # # exit()
    # def test_get_project_details(self):
    #     url = reverse_lazy('project-detail', kwargs={'pk': self.project_1.id})

    #     # Non authentifié
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, 401)  # 401 Unauthorized

    #     # Authentifié par autre user, non contributeur, non auteur
    #     self.client.force_authenticate(user=self.hector)
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, 200)  # 403 Forbidden

    #     # Authentifié comme auteur
    #     self.client.force_authenticate(user=self.achille)
    #     response = self.client.get(url)
    #     response.json().pop('created_time')
    #     self.assertEqual(response.status_code, 200)  # 200 OK
    #     self.assertEqual(response.json(),
    #                      self.expected_reponses_content('get_project_1'))

    # def test_create_project(self):
    #     url = reverse_lazy('project-list')
    #     post_datas = {
    #         'title': 'Prise de Troie',
    #         'description': 'Récupérer Hélène',
    #         'type': 'FE'
    #     }

    #     # Non authentifié
    #     response = self.client.post(url, post_datas)
    #     self.assertEqual(response.status_code, 401)  # 401 Unauthorized

    #     # Authentifié
    #     self.client.force_authenticate(user=self.hector)
    #     response = self.client.post(url, post_datas)
    #     self.assertEqual(response.status_code, 201)  # 201 Created

    # def test_update_project(self):
    #     url = reverse_lazy('project-detail', kwargs={'pk': self.project_1.id})
    #     post_datas = {
    #         'title': 'Venger Patrocle',
    #         'description': 'Tuer Hector en faisant attention à mon talon',
    #         'type': 'BE'
    #     }
    #     # Non authentifié
    #     response = self.client.put(url, post_datas)
    #     self.assertEqual(response.status_code, 401)  # 401 Unauthorized

    #     # Authentifié par autre user, non contributeur, non auteur
    #     self.client.force_authenticate(user=self.hector)
    #     response = self.client.put(url, post_datas)
    #     self.assertEqual(response.status_code, 403)  # 403 Forbidden

    #     # Authentifié comme auteur
    #     self.client.force_authenticate(user=self.achille)
    #     response = self.client.put(url, post_datas)
    #     response.json().pop('created_time')
    #     self.assertEqual(response.status_code, 200)  # 200 OK
    #     self.assertEqual(response.json(),
    #                      self.expected_reponses_content('updated_project'))
