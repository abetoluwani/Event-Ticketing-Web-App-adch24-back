#!/usr/bin/env python3
# File: user.py
# Author: Oluwatobiloba Light
"""User DB functions"""


from typing import Union

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from app.db import Database
from prisma.models import User
from app.utils.auth import hash_password, verify_password
from schema.user import CreateUser, CreateUserGoogle, UpdateUser, User as UserSchema
from uuid import uuid4
from prisma.errors import PrismaError


class UserDB(Database):
    """"""

    async def user_exists(self, email: str) -> Union[User, None]:
        """
        Checks if a user exists

        Args:
            email (str) - User's email

        Returns:
            User - The user
        """
        user = await self.db.user.find_unique(where={"email": email})

        if not user or user is None:
            return None

        return user

    async def create_user(self, user: CreateUser) -> Union[UserSchema, None]:
        """
        Creates a new User

        Args:
            - user (CreateUser): User input

        Returns:
            - User: User data
        """
        del user.cpassword

        user.password = hash_password(user.password)

        try:
            user_ = await self.db.user.create(
                data={
                    "id": str(uuid4()),
                    "email": user.email,
                    "username": user.username,
                    "password": user.password,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "is_admin": False
                }
            )

            return UserSchema(**jsonable_encoder(user_)).to_json()
        except (PrismaError, ) as e:
            print("An error occured while creating user...", e)
            return None

    async def create_user_google(self, user: CreateUserGoogle) -> Union[UserSchema, None]:
        """
        Creates a new User

        Args:
            - user (CreateUser): User input

        Returns:
            - User: User data
        """

        try:
            user_ = await self.db.user.create(
                data={
                    "id": str(uuid4()),
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "is_admin": False
                }
            )

            return UserSchema(**jsonable_encoder(user_)).to_json()
        except (PrismaError, ) as e:
            print("An error occured while creating user...", e)
            return None


    async def update_user(self, form_data: UpdateUser, user: UserSchema) -> \
            Union[UserSchema, None]:
        """
        Updates a user

        Args:
            - user (UpdateUser): User input

        Returns:
            - User: User data
        """
        existing_user = await self.user_exists(user.email)

        if existing_user:
            for (key, value) in form_data:
                if key == 'password' and value is not None:
                    if form_data.old_password:
                        if not verify_password(form_data.old_password,
                                               existing_user.password):
                            return None

                        await self.db.user.update(
                            where={"email": user.email},
                            data={
                                "password": hash_password(value)
                            }
                        )

                if (key != 'password' or key != 'old_password') and value is not None:
                    await self.db.user.update(
                        where={"email": user.email},
                        data=jsonable_encoder({key: value})
                    )

        updated_user = await self.user_exists(user.email)

        return UserSchema(**jsonable_encoder(updated_user))
