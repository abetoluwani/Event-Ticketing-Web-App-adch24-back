#!/usr/bin/env python3
# File: user.py
# Author: Oluwatobiloba Light
"""User Model"""


from typing import List, Optional
from sqlmodel import Field, Relationship
from app.model.base_model import BaseModel


class User(BaseModel, table=True):
    __tablename__: str = 'users'

    first_name: str = Field(default=None, nullable=True)
    last_name: str = Field(default=None, nullable=True)

    email: str = Field(unique=True)
    password: Optional[str] = Field(default=None, nullable=True)
    user_token: str = Field(unique=True)

    phone_no: str = Field(default=None, nullable=True)
    is_active: bool = Field(default=True)
    is_admin: bool = Field(default=False)

    events: Optional[List["Event"]] = Relationship(back_populates="owner")
