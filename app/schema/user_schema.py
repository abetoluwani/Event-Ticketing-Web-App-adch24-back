#!/usr/bin/env python3
# File: user_schema.py
# Author: Oluwatobiloba Light
"""User Schema"""


from typing import List, Optional, Union

from pydantic import BaseModel, Field

from app.schema.base_schema import FindBase, ModelBaseInfo, SearchOptions
from app.util.schema import AllOptional


class BaseUser(BaseModel):
    email: str
    user_token: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    is_active: bool
    is_admin: bool

    class Config:
        orm_mode = True


class BaseUserWithPassword(BaseUser):
    password: str


class User(ModelBaseInfo, BaseUser, AllOptional):
    ...


class FindUser(BaseModel):
    # email__eq: Optional[str] = Field(default=None)
    email: str
    ...


class UpsertUser(BaseUser, AllOptional):
    ...


class FindUserResult(BaseModel):
    founds: Optional[List[User]]
    search_options: Optional[SearchOptions]
