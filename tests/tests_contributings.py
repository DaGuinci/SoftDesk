from django.urls import reverse_lazy

from api.views import ProjectViewset as view

from .tests_datas_setup import TestSetupAPITestCase

from rest_framework import routers

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


class ContributingTestCases(ApiAPITestCase):

    def test_get_contributors_by_project(self):
        contributors = self.project_1.contributors.all()
        self.assertEqual(list(contributors), [self.achille, self.ulysse])

    def test_add_contributor(self):

        url = reverse_lazy('project-add_contributor', kwargs={'pk': self.project_1.id})
        post_datas = {
            'contributor': self.hector.id
        }

        # Authentifié non auteur
        self.client.force_authenticate(user=self.hector)
        response = self.client.patch(url, post_datas)
        self.assertEqual(response.status_code, 403)  # 403 Forbidden

        # Authentifié contributeur
        self.client.force_authenticate(user=self.ulysse)
        response = self.client.patch(url, post_datas)
        self.assertEqual(response.status_code, 403)  # 403 Forbidden

        # Authentifié auteur
        self.client.force_authenticate(user=self.achille)
        response = self.client.patch(url, post_datas)
        self.assertEqual(response.status_code, 200)  # 200 OK

        # Répétition contributings
        response = self.client.patch(url, post_datas)
        self.assertEqual(response.status_code, 200)  # 200 OK

    def test_remove_contributor(self):

        url = reverse_lazy('project-remove_contributor', kwargs={'pk': self.project_1.id})
        post_datas = {
            'contributor': self.ulysse.id
        }

        # Authentifié non auteur
        self.client.force_authenticate(user=self.hector)
        response = self.client.patch(url, post_datas)
        self.assertEqual(response.status_code, 403)  # 403 Forbidden

        # Authentifié contributeur
        self.client.force_authenticate(user=self.ulysse)
        response = self.client.patch(url, post_datas)
        self.assertEqual(response.status_code, 403)  # 403 Forbidden

        # Authentifié auteur
        self.client.force_authenticate(user=self.achille)
        response = self.client.patch(url, post_datas)
        self.assertEqual(response.status_code, 200)  # 200 OK
