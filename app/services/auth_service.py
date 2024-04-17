#!/usr/bin/env python3
# File: auth_service.py
# Author: Oluwatobiloba Light
"""Auth Service"""


from datetime import timedelta
from typing import Any, List, Mapping, Optional

from app.core.config import configs
from app.core.exceptions import AuthError
from app.core.security import create_access_token, get_password_hash, \
    verify_password
from app.model.user import User
from app.repository.user_repository import UserRepository
from app.schema.auth_schema import GoogleSignIn, Payload, SignIn, SignUp
from app.schema.user_schema import FindUser
from app.services.base_service import BaseService
from app.util.hash import get_rand_hash


class AuthService(BaseService):
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
        super().__init__(user_repository)

    def sign_in(self, sign_in_info: SignIn):
        find_user = FindUser(email=sign_in_info.email)

        # find_user.email__eq = sign_in_info.email__eq

        user: List[User] = self.user_repository.read_by_options(find_user)[
            "founds"]

        if len(user) < 1:
            raise AuthError(detail="Incorrect email or password")

        found_user = user[0]

        if not found_user.is_active:
            raise AuthError(detail="Account is not active")

        if found_user.password and\
                not verify_password(sign_in_info.password, found_user.password):
            raise AuthError(detail="Incorrect email or password")

        delattr(found_user, "password")

        payload = Payload(
            id=found_user.id,
            email=found_user.email,
            name=found_user.first_name + found_user.last_name,
            is_admin=found_user.is_admin,
        )

        token_lifespan = timedelta(minutes=configs.ACCESS_TOKEN_EXPIRE_MINUTES)

        access_token, expiration_datetime = create_access_token(
            payload.model_dump(), token_lifespan)

        sign_in_result = {
            "access_token": access_token,
            "expiration": expiration_datetime,
            "user_info": found_user,
        }

        return sign_in_result

    def sign_up(self, user_info: SignUp):
        user_token = get_rand_hash()

        user = User(**user_info.model_dump(exclude_none=True),
                    is_active=True, is_admin=False, user_token=user_token)

        user.password = get_password_hash(user_info.password)

        created_user = self.user_repository.create(user)

        delattr(created_user, "password")

        return created_user

    def google_sign_up(self, user_info: GoogleSignIn):
        """Google Login"""
        find_user = FindUser(email=user_info.email)

        user_exists: List[User] = self.user_repository.read_by_options(find_user)[
            "founds"]

        if len(user_exists) < 1:
            # register user here
            user_token = get_rand_hash()

            user = User(**user_info.model_dump(),
                        first_name=user_info.given_name
                        if user_info.given_name else "",
                        last_name=user_info.family_name
                        if user_info.family_name else "",
                        is_active=True,
                        is_admin=False,
                        user_token=user_token)

            created_user = self.user_repository.create(user)

            payload = Payload(
                id=created_user.id,
                email=created_user.email,
                name=created_user.first_name + created_user.last_name,
                is_admin=created_user.is_admin,
            )

            token_lifespan = timedelta(
                minutes=configs.ACCESS_TOKEN_EXPIRE_MINUTES)

            access_token, expiration_datetime = create_access_token(
                payload.model_dump(), token_lifespan)

            google_signup_result = {
                "access_token": access_token,
                "expiration": expiration_datetime,
                "user_info": created_user,
            }

            return google_signup_result

        return self.sign_in(sign_in_info=SignIn(email=user_info.email))
