from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm.session import Session

from db import get_db
from services.categories_service import CategoryService

OpenSASession = Annotated[Session, Depends(get_db)]


def create_category_service(_repository: OpenSASession) -> CategoryService:
    return CategoryService(_repository)