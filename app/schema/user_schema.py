#!/usr/bin/env python3
# File: user_schema.py
# Author: Oluwatobiloba Light
"""User Schema"""


from typing import List, Optional, Union

from fastapi import Request
from pydantic import BaseModel, Field

from app.schema.base_schema import FindBase, FindQueryOptions, ModelBaseInfo, SearchOptions
from app.util.schema import AllOptional


class BaseUser(BaseModel):
    email: str
    # password: Optional[str]
    user_token: Optional[str]

    first_name: Optional[str]
    last_name: Optional[str]

    is_active: bool
    is_admin: bool

    phone_no: Optional[str]

    class Config:
        orm_mode = True


class BaseUserWithPassword(BaseUser):
    password: str


class User(ModelBaseInfo, BaseUser, AllOptional):
    password: Union[str, None] = Field(default=None)
    ...


class User_(ModelBaseInfo, BaseUser, AllOptional):
    ...


class FindUser(BaseModel):
    email: str
    ...


class FindUserQuery(BaseModel):
    request: Request
    ...

    class Config:
        arbitrary_types_allowed = True


class FindUserQueryOptions(FindQueryOptions):
    ...


class UpsertUser(BaseModel):
    email: Optional[str] = Field(default=None)
    password: Optional[str] = Field(default=None)

    first_name: Optional[str] = Field(default=None)
    last_name: Optional[str] = Field(default=None)

    phone_no: Optional[str] = Field(default=None)
    ...


class FindUserResult(BaseModel):
    founds: Optional[List[User_]]
    search_options: Optional[SearchOptions]
