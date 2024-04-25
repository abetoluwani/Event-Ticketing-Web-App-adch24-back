#!/usr/bin/env python3
# File: user_services.py
# Author: Oluwatobiloba Light
"""User Services"""


from app.repository.user_repository import UserRepository
from app.services.base_service import BaseService


class UserService(BaseService):
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
        super().__init__(user_repository)

    def remove_by_id(self, user_id: str):
        return self.user_repository.delete_by_id(user_id)
