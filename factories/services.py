from fastapi import Depends
from sqlalchemy.orm.session import Session

from db import get_db
from services.categories_service import CategoryService


def create_category_service(_repository: Session = Depends(get_db)) -> CategoryService:
    return CategoryService(_repository)