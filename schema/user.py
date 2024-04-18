#!/usr/bin/env python3
# File: user.py
# Author: Oluwatobiloba Light
"""User validation schema"""


from typing import Union
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime


class User(BaseModel):
    """User schema"""
    id: str
    email: EmailStr
    first_name: Union[str, None] = Field(default=None, title="First Name",
                                         description="User's first name")
    last_name: Union[str, None] = Field(default=None, title="Last Name",
                                        description="User's last name")

    phone_no: Union[int, None] = Field(default=None, title="Phone Number",
                                       description="User's phone number")

    is_admin: bool = False
    created_at: datetime = Field(default=datetime.now())
    updated_at: datetime = Field(default=datetime.now())

    def to_json(self):
        """Convert to json"""
        user_dict = jsonable_encoder(self)
        return user_dict


class CreateUser(BaseModel):
    """Create user schema"""
    first_name: Union[str, None] = Field(default=None, title="First Name",
                                         description="User's first name")

    last_name: Union[str, None] = Field(default=None, title="Last Name",
                                        description="User's last name")
    email: EmailStr

    phone_no: Union[int, None] = Field(default=None, title="Phone Number",
                                       description="User's phone number")

    password: str = Field(min_length=6)

    cpassword: str

    def to_json(self):
        """Convert to json"""
        user_dict = jsonable_encoder(self)
        del user_dict["cpassword"]
        return user_dict


class CreateUserGoogle(BaseModel):
    """Create User from Google Authentication"""
    first_name: Union[str, None] = Field(default=None, title="First Name",
                                         description="User's first name")
    last_name: Union[str, None] = Field(default=None, title="Last Name",
                                        description="User's last name")
    email: EmailStr

    class Config:
        from_attributes = True

class UpdateUser(BaseModel):
    """Update User schema"""
    first_name: Union[str, None] = Field(default=None, title="First Name",
                                         description="User's first name")

    last_name: Union[str, None] = Field(default=None, title="Last Name",
                                        description="User's last name")

    phone_no: Union[int, None] = Field(default=None, title="Phone Number",
                                       description="User's phone number")

    password: Union[str, None] = Field(min_length=6, default=None)

    old_password: Union[str, None] = Field(min_length=6, default=None)

    def to_json(self):
        """Convert to json"""
        user_dict = jsonable_encoder(self)
        return user_dict


class UserLogin(BaseModel):
    """User login schema"""
    email: EmailStr
    password: str = Field(min_length=6)
