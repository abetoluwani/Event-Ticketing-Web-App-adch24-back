#!/usr/bin/env python3
# File: event.py
# Author: Oluwatobiloba Light
"""Validation schema"""


from typing import List
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field
from datetime import datetime
from schema.user import User


class EventImage(BaseModel):
    """Event Image Schema"""
    id: str
    uri: str
    name: str
    event_id: str


class Event(BaseModel):
    """Event Schema"""
    id: str
    name: str
    date_time: datetime
    location: str
    thumbnail: str
    images: List['EventImage']
    user_id: str
    user: 'User'
    created_at: datetime = Field(default=datetime.now())
    updated_at: datetime = Field(default=datetime.now())


class CreateEventInput(BaseModel):
    """Create event schema"""
    name: str
    date_time: datetime
    location: str
    thumbnail: str
    images: List['EventImage'] = []
    user_id: str

    def to_json(self):
        """Convert to json"""
        user_dict = jsonable_encoder(self)
        return user_dict

    class Config:
        orm_mode = True
