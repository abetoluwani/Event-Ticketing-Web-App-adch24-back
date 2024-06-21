#!/usr/bin/env python3
# File: event_schema.py
# Author: Oluwatobiloba Light
"""Event Schema"""


from datetime import datetime, date as dt, time
from typing import List, Optional, Union
from uuid import UUID
from fastapi import Request
from pydantic import BaseModel, Field
from app.model.event import Event as EventModel
from app.model.event import EventType
from app.model.category import Category
# from app.schema.category_schema import Category
from app.schema.user_schema import User_
from app.schema.base_schema import FindBase, FindQueryOptions, FindResult, ModelBaseInfo, SearchOptions
from app.util.schema import AllOptional


class BaseEvent(ModelBaseInfo):
    name: str
    description: str

    categories: Optional[List[Category]] = None

    date: dt = Field(default=dt.today())

    location: str
    image: str

    class Config:
        orm_mode = True


class Event(BaseEvent, AllOptional):
    ...
    # start_time: str
    # end_time: str
    categories: List[Category]
    owner_id: UUID
    owner: Optional[User_]


class Event_(BaseEvent, AllOptional):
    ...
    # start_time: str
    # end_time: str
    categories: List[Category]
    owner_id: UUID
    owner: Optional[User_]


class CreateEvent(BaseEvent):

    ...
    categories: List[str]
    evt_type: EventType


class UpdateEvent(BaseEvent):
    ...
    name: Optional[str] = None
    description: Optional[str] = None

    categories: Optional[List[str]] = None

    date: Optional[dt] = None

    location: Optional[str] = None
    image: Optional[str] = None


class DeleteEvent(ModelBaseInfo):
    ...



class GetUserEventsQuery(BaseModel):
    owner_id: Optional[str] = None
    event_id: Optional[str] = None


class FindEventQuery(BaseModel):
    page: Optional[int] = None
    page_size: Optional[Union[str, int]] = None
    ordering: Optional[str] = None
    ...

    class Config:
        arbitrary_types_allowed = True


class FindEventQueryOptions(FindQueryOptions):
    ...


class FindEventsResult(BaseModel):
    founds: Optional[List[Event_]]
    search_options: Optional[SearchOptions]


class FindUserEventsResult(BaseModel):
    founds: Optional[List[Event_]]
    search_options: Optional[SearchOptions]
