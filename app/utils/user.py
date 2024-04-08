#!/usr/bin/env python3
# File: user.py
# Author: Oluwatobiloba Light
"""User DB functions"""


from typing import Union

from fastapi.encoders import jsonable_encoder
from app.db import Database
from prisma.models import User
from app.utils.utils import hash_password
from schema.user import CreateUser
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
        return jsonable_encoder(await self.db.user
                                .find_unique(where={"email": email}))

    async def create_user(self, user: CreateUser):
        """
        Creates a new User
        
        Args:
            - user (CreateUser): User input
            
        Returns:
            - User: User data
        """
        user['password'] = hash_password(user['password'])
        try:
            user = await self.db.user.create(
                data={
                    "id": str(uuid4()),
                    **user,
                    "is_admin": False
                }
            )

            return jsonable_encoder(user)
        except (PrismaError, ) as e:
            print("An error occured while creating user...", e)
            return None
