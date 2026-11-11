
from sqlalchemy import select

import models
from tests.integration.base import IntegrationTestCase

URL = "/api/categories/"


class TestRemoveCategory(IntegrationTestCase):
    def create_category(self, name: str) -> models.Category:
        # Lisätään testidata suoraan kantaan, jotta testi ei riipu create-endpointista
        category = models.Category(name=name)
        self.session.add(category)
        self.session.commit()
        return category

    def create_item(self, category: models.Category, name: str = "Vasara") -> models.Item:
        item = models.Item(name=name, category_id=category.id)
        self.session.add(item)
        self.session.commit()
        return item

    def get_saved_categories(self) -> list[models.Category]:
        # Haetaan testikannasta suoraan, ei luoteta API:n paluuarvoon
        return list(self.session.scalars(select(models.Category)))

    def test_returns_204_and_empty_body(self):
        category = self.create_category("Työkalut")

        response = self.client.delete(f"{URL}{category.id}")

        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.content, b"")

    def test_removes_category_from_database(self):
        category = self.create_category("Työkalut")

        self.client.delete(f"{URL}{category.id}")

        self.assertEqual(self.get_saved_categories(), [])

    def test_removes_only_the_given_category(self):
        removed = self.create_category("Työkalut")
        kept = self.create_category("Urheilu")
        kept_id = kept.id

        self.client.delete(f"{URL}{removed.id}")

        saved = self.get_saved_categories()
        self.assertEqual(len(saved), 1)
        self.assertEqual(saved[0].id, kept_id)
        self.assertEqual(saved[0].name, "Urheilu")

    def test_nonexistent_category_returns_404(self):
        response = self.client.delete(f"{URL}999")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["detail"], "category 999 not found")

    def test_removing_same_category_twice_returns_404(self):
        category = self.create_category("Työkalut")
        category_id = category.id

        first = self.client.delete(f"{URL}{category_id}")
        second = self.client.delete(f"{URL}{category_id}")

        self.assertEqual(first.status_code, 204)
        self.assertEqual(second.status_code, 404)

    def test_category_with_items_returns_409_and_is_not_removed(self):
        # Liiketoimintasääntö: kategoriaa ei saa poistaa, jos siihen kuuluu vielä tavaroita
        category = self.create_category("Työkalut")
        category_id = category.id
        self.create_item(category)

        response = self.client.delete(f"{URL}{category_id}")

        self.assertEqual(response.status_code, 409)
        self.assertEqual(response.json()["detail"], f"category {category_id} still has items")
        # Kategorian pitää edelleen löytyä kannasta
        saved = self.get_saved_categories()
        self.assertEqual(len(saved), 1)
        self.assertEqual(saved[0].id, category_id)

    def test_invalid_id_returns_422(self):
        # category_id on tyypitetty int:ksi, joten FastAPI hylkää muut arvot jo ennen serviceä
        for category_id in ["abc", "1.5"]:
            with self.subTest(category_id=category_id):
                response = self.client.delete(f"{URL}{category_id}")

                self.assertEqual(response.status_code, 422)
