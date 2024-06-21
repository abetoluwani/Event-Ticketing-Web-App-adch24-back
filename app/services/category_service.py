#!/usr/bin/env python3
# File: category_services.py
# Author: Oluwatobiloba Light
"""Category Services"""


from app.model.category import Category
from app.repository.category_repository import CategoryRepository
from app.schema.category_schema import CreateCategory
from app.services.base_service import BaseService


class CategoryService(BaseService):
    def __init__(self, category_repository: CategoryRepository):
        self.category_repository = category_repository

        super().__init__(category_repository)

    def create_category(self, category_info: CreateCategory) -> Category:
        """Creates a new category"""
        schema = Category(**category_info.model_dump())

        category = self.category_repository.create(schema)

        return category
