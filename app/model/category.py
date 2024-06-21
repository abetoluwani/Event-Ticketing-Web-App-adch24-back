#!/usr/bin/env python3
# File: category.py
# Author: Oluwatobiloba Light
"""Category Model"""


from typing import List, Optional
from sqlmodel import Field, Relationship
from app.model.base_model import BaseModel
from sqlalchemy import Column, String

# from app.model.event import EventCategory, event_categories


class Category(BaseModel, table=True):
    __tablename__: str = "categories"

    name: str = Field(sa_column=Column(String(50), default=None,
                      nullable=False, unique=True))

    events: List['Event'] = Relationship(
        back_populates="categories", sa_relationship_kwargs={"secondary": 'event_categories'})
