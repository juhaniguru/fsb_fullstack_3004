from typing import List

import models
from dtos.categories import CreateCategoryReq
from services.abc_categories_service import ABCCategoryService


class FakeCategoryService(ABCCategoryService):
    # Konstruktorin kautta säädetään, miten fake käyttäytyy.
    # Näin sama luokka kelpaa moneen eri testiin.
    def __init__(self, categories: List[models.Category] | None = None, raises: Exception | None = None):
        self._categories = categories or []
        self._raises = raises

    def create(self, req: CreateCategoryReq) -> models.Category:
        return models.Category(id=1, name=req.name)
