
import models
from dtos.categories import CreateCategoryReq
from services.abc_categories_service import ABCCategoryService


class FakeCategoryService(ABCCategoryService):


    # Konstruktorin kautta säädetään, miten fake käyttäytyy.
    # Näin sama luokka kelpaa moneen eri testiin.
    def __init__(self, categories: list[models.Category] | None = None, raises: Exception | None = None):
        self._categories = categories or []
        self._raises = raises

    def delete(self, _id: int) -> None:
        self.get_by_id(_id)
        if self._raises:
            raise self._raises
        return None

    def get_by_id(self, _id: int) -> models.Category:

        if self._raises:


            raise self._raises

        return models.Category(id=1, name='Kategoria')

    def create(self, req: CreateCategoryReq) -> models.Category:
        return models.Category(id=1, name=req.name)
