#!/usr/bin/env python3
# File: category_repository.py
# Author: Oluwatobiloba Light
"""Category Repository"""


from typing import Callable
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.core.exceptions import DuplicatedError
from app.model.category import Category
from app.repository.base_repository import BaseRepository


class CategoryRepository(BaseRepository):
    def __init__(self, session_factory: Callable[[], Session]):
        self.session_factory = session_factory
        self.model = Category

        super().__init__(session_factory, Category)

    def create(self, schema) -> Category:
        """"""
        with self.session_factory() as session:
            query = self.model(**schema.dict())

            try:
                session.add(query)

                session.commit()

                session.refresh(query)
            except IntegrityError as e:
                raise DuplicatedError(detail=str(e.orig))

            return query
