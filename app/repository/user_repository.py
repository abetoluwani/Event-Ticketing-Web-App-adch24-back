#!/usr/bin/env python3
# File: user_repository.py
# Author: Oluwatobiloba Light
"""User Repository"""


from typing import Callable
from uuid import UUID
from sqlalchemy import Uuid, cast, text
from sqlalchemy.orm import Session
from app.core.exceptions import NotFoundError
from app.model.user import User
from app.repository.base_repository import BaseRepository


class UserRepository(BaseRepository):
    def __init__(self, session_factory: Callable[[], Session]):
        self.session_factory = session_factory
        self.model = User

        super().__init__(session_factory, User)

    def delete_by_id(self, user_id: str):
        with self.session_factory() as session:
            query = session.query(self.model).filter(
                cast(self.model.id, Uuid) == cast(user_id, Uuid)).first()

            if not query:
                raise NotFoundError(detail=f"not found id : {user_id}")

            self.model.delete_user_events(session, user_id=user_id)

            session.delete(query)

            session.commit()
