#!/usr/bin/env python3
# File: event.py
# Author: Oluwatobiloba Light
"""Event Model"""


from datetime import date as dt, datetime
from uuid import UUID
from sqlalchemy import Column, Date, DateTime, ForeignKey, Uuid
from sqlmodel import Field, Relationship
from app.model.base_model import BaseModel
from app.model.user import User


class Event(BaseModel, table=True):
    __tablename__: str = 'events'

    name: str = Field(default=None, nullable=False)

    start_time: datetime = Field(sa_column=Column(DateTime))

    end_time: datetime = Field(sa_column=Column(DateTime))

    date: dt = Field(sa_column=Column(Date))

    location: str = Field(default=None, nullable=True)

    image: str = Field(default=None, nullable=True)

    user_id: UUID = Field(ForeignKey("user.id"), sa_column=Column(Uuid))

    user: User = Relationship(back_populates="events")
