
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

import dtos.categories
from custom_exceptions.business_rule_exception import BusinessRuleException
from custom_exceptions.not_found_exception import NotFoundException
from factories.services import create_category_service
from services.abc_categories_service import ABCCategoryService

router = APIRouter(prefix='/api/categories', tags=['categories'])

CategoryServ = Annotated[ABCCategoryService, Depends(create_category_service)]


@router.get('/')
def get_all(_service: CategoryServ) -> list[dtos.categories.CategoryDto]:
    category_dtos = [dtos.categories.CategoryDto.model_validate(c) for c in _service.get_all()]
    return category_dtos


@router.get('/{category_id}')
def get_by_id(category_id: int, _service: CategoryServ) -> dtos.categories.CategoryDto:
    try:
        return dtos.categories.CategoryDto.model_validate(_service.get_by_id(category_id))
    except NotFoundException as error:
        raise HTTPException(status_code=404, detail=str(error))


@router.post('/', status_code=status.HTTP_201_CREATED)
def create(req: dtos.categories.CreateCategoryReq,
           _service: CategoryServ) -> dtos.categories.CategoryDto:
    return dtos.categories.CategoryDto.model_validate(_service.create(req))
    # return _service.create(req)

@router.put('/{category_id}')
def update(category_id: int, req: dtos.categories.CreateCategoryReq,
           _service: CategoryServ) -> dtos.categories.CategoryDto:
    try:
        return dtos.categories.CategoryDto.model_validate(_service.update(category_id, req))
    except NotFoundException as error:
        raise HTTPException(status_code=404, detail=str(error))



@router.delete('/{category_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete(category_id: int, _service: CategoryServ):
    try:
        _service.delete(category_id)
    except NotFoundException as error:
        raise HTTPException(status_code=404, detail=str(error))
    except BusinessRuleException as error:
        raise HTTPException(status_code=409, detail=str(error))