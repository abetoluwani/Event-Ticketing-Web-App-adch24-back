#!/usr/bin/env python3
# File: event_services.py
# Author: Oluwatobiloba Light
"""Event Services"""


from typing import Any, Dict
from uuid import UUID
from app.model.user import User
from app.model.event import Event
from app.repository.event_repository import EventRepository
from app.schema.user_schema import UpsertUser, User_, User as u
from app.services.base_service import BaseService
from app.schema.event_schema import CreateEvent, Event as ev
from app.util.date import format_time_with_am_pm


class EventService(BaseService):
    def __init__(self, event_repository: EventRepository):
        self.event_repository = event_repository

        super().__init__(event_repository)

    def create_event(self, event_info: CreateEvent, user: User) -> Event:
        """Creates a new event"""
        schema = Event(**event_info.model_dump(), owner_id=user.id)

        event = self.event_repository.create(schema)

        return event

    def get_list(self, schema):
        return self.event_repository.read_by_options(schema)

    def get_events_by_user(self, schema, owner_id: UUID):
        """"""
        return self.event_repository.get_events_by_user(schema, owner_id)
