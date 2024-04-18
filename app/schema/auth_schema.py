#!/usr/bin/env python3
# File: user_schema.py
# Author: Oluwatobiloba Light
"""User Schema"""


from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from app.schema.user_schema import User


class SignIn(BaseModel):
    email: str
    password: Optional[str] = Field(default=None)


class SignUp(BaseModel):
    email: str
    password: str
    first_name: str
    last_name: str


class GoogleSignIn(BaseModel):
    iss: str
    email: str
    email_verified: Optional[bool]
    family_name: Optional[str]
    given_name: Optional[str]
    exp: int


class Payload(BaseModel):
    id: int
    email: str
    name: str
    is_admin: bool


class SignInResponse(BaseModel):
    access_token: str
    expiration: datetime
    user_info: User
