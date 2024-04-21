#!/usr/bin/env python3
# File: event.py
# Author: Oluwatobiloba Light
"""Event Model"""


from app.util.date import format_time_with_am_pm
from datetime import date as dt, datetime, time
from typing import Optional
from uuid import UUID
from sqlalchemy import Column, Date, DateTime, TIME
from sqlmodel import Field, Relationship, ForeignKey
from app.model.base_model import BaseModel
from .user import User


class Event(BaseModel,  table=True):
    __tablename__: str = 'events'

    name: str = Field(default=None, nullable=False)

    start_time: time = Field(sa_column=Column(TIME))

    end_time: time = Field(sa_column=Column(TIME))

    date: dt = Field(sa_column=Column(Date))

    location: str = Field(default=None, nullable=True)

    image: str = Field(default=None, nullable=True)

    owner_id: Optional[UUID] = Field(
        default=None, nullable=False, foreign_key="users.id")

    owner: Optional['User'] = Relationship(back_populates="events")

    @property
    def formatted_start_time(self) -> Optional[str]:
        """
        This property returns the start_time with AM/PM format.
        """
        return format_time_with_am_pm(self.start_time)

    @property
    def formatted_end_time(self) -> Optional[str]:
        """
        This property returns the end_time with AM/PM format.
        """
        return format_time_with_am_pm(self.end_time)
