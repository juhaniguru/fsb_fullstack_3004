from sqlalchemy.orm import Session

import models
from custom_exceptions.business_rule_exception import BusinessRuleException
from custom_exceptions.not_found_exception import NotFoundException
from dtos.categories import CreateCategoryReq
from services.abc_categories_service import ABCCategoryService


class CategoryService(ABCCategoryService):






    def __init__(self, _repository: Session):
        self._repository = _repository

    def get_by_id(self, _id: int) -> models.Category:
        category = self._repository.query(models.Category).filter_by(id=_id).first()

        if category is None:
            raise NotFoundException(f'category {_id} not found')

        return category

    def delete(self, _id: int) -> None:
        category = self.get_by_id(_id)
        if category.items:
            raise BusinessRuleException(f'category {_id} still has items')

        self._repository.delete(category)
        self._repository.commit()

    def create(self, req: CreateCategoryReq) -> models.Category:
        category = models.Category(name=req.name)

        self._repository.add(category)
        self._repository.commit()

        return category