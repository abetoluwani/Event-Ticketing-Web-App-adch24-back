#!/usr/bin/env python3
# File: user_repository.py
# Author: Oluwatobiloba Light
"""User Repository"""


from typing import Callable
from sqlalchemy.orm import Session
from app.model.user import User
from app.repository.base_repository import BaseRepository


class UserRepository(BaseRepository):
    def __init__(self, session_factory: Callable[[], Session]):
        self.session_factory = session_factory
        self.model = User

        super().__init__(session_factory, User)
