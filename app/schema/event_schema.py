#!/usr/bin/env python3
# File: event_schema.py
# Author: Oluwatobiloba Light
"""Event Schema"""


from datetime import datetime, date as dt, time
from typing import List, Optional, Union
from uuid import UUID
from fastapi import Request
from pydantic import BaseModel, Field
from app.model.user import User
from app.schema.user_schema import User_
from app.schema.base_schema import FindBase, FindQueryOptions, FindResult, ModelBaseInfo, SearchOptions
from app.util.schema import AllOptional


class BaseEvent(BaseModel):
    name: str

    start_time: time
    end_time: time
    date: dt

    location: str
    image: str

    # user: Optional[User_]

    class Config:
        orm_mode = True


class Event(ModelBaseInfo, BaseEvent, AllOptional):
    ...
    # start_time: str
    # end_time: str
    owner_id: UUID
    owner: Optional[User_]


class Event_(ModelBaseInfo, BaseEvent, AllOptional):
    ...
    # start_time: str
    # end_time: str
    owner_id: UUID
    # owner: Optional[User_]


class CreateEvent(BaseEvent):
    start_time: time
    end_time: time
    ...
    # user: Optional[User] = Field(default=None)


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
