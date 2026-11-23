
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

import dtos.register
from dtos import  register, login
from custom_exceptions.conflict_exception import ConflictException
from custom_exceptions.unauthorized_exception import UnauthorizedException
from factories.services import user_service_factory
from services.abc_user_service import ABCUserService

router = APIRouter(prefix='/api/users', tags=['users'])

UserServ = Annotated[ABCUserService, Depends(user_service_factory)]


@router.post('/register', status_code=status.HTTP_201_CREATED)
def register(request_data: register.RegisterReq,
             _user_service: UserServ) -> register.RegisterRes:
    try:
        user = _user_service.register(request_data.username, request_data.password)
        return dtos.register.RegisterRes(id=user.id, username=user.username, role=user.role)
    except ConflictException as error:
        raise HTTPException(status_code=409, detail=str(error))


@router.post('/login')
def login(request_data: login.LoginReq,
          _user_service: UserServ) -> login.LoginRes:
    try:
        token = _user_service.login(request_data.username, request_data.password)
        return login.LoginRes(token=token)
    except UnauthorizedException as error:
        raise HTTPException(status_code=401, detail=str(error))