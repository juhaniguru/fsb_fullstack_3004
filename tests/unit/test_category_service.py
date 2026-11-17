
import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import models
from custom_exceptions.business_rule_exception import BusinessRuleException
from custom_exceptions.not_found_exception import NotFoundException
from db import Base
from dtos.categories import CreateCategoryReq
from services.categories_service import CategoryService


class CategoryServiceTests(unittest.TestCase):

    def setUp(self):
        # sqlite:///:memory: luo tietokannan muistiin.
        # setUp ajetaan ennen jokaista testiä, joten
        # jokainen testi saa oman tyhjän kantansa.
        self.engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(self.engine)
        self.session = sessionmaker(bind=self.engine)()

        self.service = CategoryService(self.session)

    def tearDown(self):
        self.session.close()
        self.engine.dispose()


    def test_delete_category_with_items_raises(self):
        created = self.service.create(CreateCategoryReq(name='Kamerat'))
        self.session.add(models.Item(name='Canon EOS R50', category_id=created.id))
        self.session.commit()

        with self.assertRaises(BusinessRuleException) as ctx:
            self.service.delete(created.id)

        self.assertIn('still has items', str(ctx.exception))
        # kategoria on yhä tallella
        self.assertIsNotNone(self.service.get_by_id(created.id))

    def test_create_returns_category_with_id(self):
        # Act
        created = self.service.create(CreateCategoryReq(name='Kamerat'))

        # Assert
        self.assertIsNotNone(created.id)
        self.assertEqual('Kamerat', created.name)

    def test_get_all_returns_all_categories(self):
        self.service.create(CreateCategoryReq(name='Kamerat'))
        self.service.create(CreateCategoryReq(name='Kannettavat'))

        names = [category.name for category in self.service.get_all()]

        # assertCountEqual ei välitä järjestyksestä, koska kysely ei järjestä rivejä
        self.assertCountEqual(['Kamerat', 'Kannettavat'], names)

    def test_get_by_id_returns_category(self):
        created = self.service.create(CreateCategoryReq(name='Kamerat'))

        found = self.service.get_by_id(created.id)

        self.assertEqual('Kamerat', found.name)

    def test_get_by_id_unknown_raises_not_found(self):
        with self.assertRaises(NotFoundException):
            self.service.get_by_id(999)

    def test_delete_removes_category(self):
        created = self.service.create(CreateCategoryReq(name='Kamerat'))

        self.service.delete(created.id)

        with self.assertRaises(NotFoundException):
            self.service.get_by_id(created.id)


if __name__ == '__main__':
    unittest.main()