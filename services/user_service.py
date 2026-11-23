import datetime
import os
import uuid

import jwt
from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerifyMismatchError
from sqlalchemy.orm import Session

import models
from custom_exceptions.conflict_exception import ConflictException
from custom_exceptions.unauthorized_exception import UnauthorizedException
from services.abc_user_service import ABCUserService



class UserService(ABCUserService):

    def __init__(self, _repository: Session):
        self._repository = _repository
        self.ph = PasswordHasher()



    def login(self, username: str, password: str) -> str:
        user = self.get_user_by_username(username)

        # Sama virhe molemmissa tapauksissa, ks. alla
        if user is None:
            raise UnauthorizedException('username or password incorrect')

        # argon2.verify lukee tallennetusta merkkijonosta saltin ja parametrit,
        # laskee niillä hashin annetusta salasanasta ja vertaa vakioaikaisesti
        # HUOM: argumenttien järjestys on verify(hash, password).
        # verify ei palauta False:a, vaan heittää VerifyMismatchErrorin,
        # jos salasana ei täsmää (InvalidHashError, jos hash on rikki).
        try:
            self.ph.verify(user.hashed_password, password)
        except (VerifyMismatchError, InvalidHashError):
            raise UnauthorizedException('username or password incorrect')

        token_key = os.getenv('TOKEN_KEY')

        payload = {
            'sub': str(user.id),
            'name': user.username,
            'role': user.role,
            'jti': str(uuid.uuid4()),
            'exp': datetime.datetime.now(datetime.UTC) + datetime.timedelta(days=7),
        }

        return jwt.encode(payload, token_key, algorithm='HS512')

    def get_user_by_access_token(self, access_token: str) -> models.User | None:
        token_key = os.getenv('TOKEN_KEY')

        try:
            payload = jwt.decode(access_token, token_key, algorithms=['HS512'])
        except jwt.PyJWTError:
            return None

        return self._repository.query(models.User).filter_by(id=int(payload['sub'])).first()

    def get_user_by_username(self, username: str) -> models.User | None:
        return self._repository.query(models.User).filter_by(username=username).first()

    def register(self, username: str, password: str) -> models.User:
        if self.get_user_by_username(username) is not None:
            raise ConflictException('username is already taken')

        # argon2.hash palauttaa merkkijonon, johon on pakattu sekä
        # algoritmin tunniste, parametrit, salt että itse hash.
        # Erillistä salt-saraketta ei siis tarvita.
        hashed_password = self.ph.hash(password)

        user = models.User(
            username=username,
            hashed_password=hashed_password,
            role='borrower',
        )

        self._repository.add(user)
        self._repository.commit()

        return user