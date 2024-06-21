#!/usr/bin/env python3
# File: category_schema.py
# Author: Oluwatobiloba Light
"""Category Schema"""


from pydantic import BaseModel

from app.schema.base_schema import ModelBaseInfo
from app.util.schema import AllOptional


class BaseCategory(BaseModel):
    name: str

    class Config:
        orm_mode = True


class CreateCategory(BaseCategory):
    ...


class Category(ModelBaseInfo, BaseCategory, AllOptional):
    ...
