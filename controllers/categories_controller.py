from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from custom_exceptions.business_rule_exception import BusinessRuleException
from custom_exceptions.not_found_exception import NotFoundException
from db import get_db
from dtos.categories import CategoryDto, CreateCategoryReq
from factories.services import create_category_service
from models import Category, Item
from services.abc_categories_service import ABCCategoryService

router = APIRouter(prefix="/api/categories", tags=["categories"])

CategoryServ = Annotated[ABCCategoryService, Depends(create_category_service)]


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_category(_service: CategoryServ, req: CreateCategoryReq) -> CategoryDto:
    category = _service.create(req)
    return CategoryDto.model_validate(category)

@router.delete('/{category_id}', status_code=status.HTTP_204_NO_CONTENT)
def remove_category(category_id: int, _service: CategoryServ):
    try:
        _service.delete(category_id)
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except BusinessRuleException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))




    return None





