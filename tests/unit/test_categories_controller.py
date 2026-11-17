
import unittest

from fastapi.testclient import TestClient

import models
from custom_exceptions.not_found_exception import NotFoundException
from factories.services import create_category_service
from main import app
from tests.fakes import FakeCategoryService


class CategoriesControllerTests(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)

    def tearDown(self):
        # Siivotaan korvaukset, etteivät ne vuoda seuraaviin testeihin
        app.dependency_overrides.clear()

    def test_get_all_returns_200_and_categories(self):
        # Arrange
        app.dependency_overrides[create_category_service] = \
            lambda: FakeCategoryService(categories=[models.Category(id=1, name='Kamerat')])

        # Act
        response = self.client.get('/api/categories/')

        # Assert
        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(response.json()))
        self.assertEqual('Kamerat', response.json()[0]['name'])

    def test_get_by_id_not_found_returns_404(self):
        app.dependency_overrides[create_category_service] = \
            lambda: FakeCategoryService(raises=NotFoundException('category 42 not found'))

        response = self.client.get('/api/categories/42')

        self.assertEqual(404, response.status_code)

    def test_create_returns_201(self):
        app.dependency_overrides[create_category_service] = lambda: FakeCategoryService()

        response = self.client.post('/api/categories/', json={'name': 'Kannettavat'})

        self.assertEqual(201, response.status_code)
        self.assertEqual('Kannettavat', response.json()['name'])

    def test_create_with_too_short_name_returns_422(self):
        app.dependency_overrides[create_category_service] = lambda: FakeCategoryService()

        response = self.client.post('/api/categories/', json={'name': 'K'})

        self.assertEqual(422, response.status_code)

    def test_delete_returns_204(self):
        app.dependency_overrides[create_category_service] = lambda: FakeCategoryService()

        response = self.client.delete('/api/categories/1')

        self.assertEqual(204, response.status_code)


if __name__ == '__main__':
    unittest.main()