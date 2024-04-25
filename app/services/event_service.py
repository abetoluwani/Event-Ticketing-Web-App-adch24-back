#!/usr/bin/env python3
# File: event_services.py
# Author: Oluwatobiloba Light
"""Event Services"""


from typing import Any, Dict
from uuid import UUID
from app.model.category import Category
from app.model.user import User
from app.model.event import Event
# from app.schema.event_schema import Event
from app.repository.event_repository import EventRepository
from app.schema.user_schema import UpsertUser, User_, User as u
from app.services.base_service import BaseService
from app.schema.event_schema import CreateEvent, Event as ev, UpdateEvent
from app.util.date import format_time_with_am_pm


class EventService(BaseService):
    def __init__(self, event_repository: EventRepository):
        self.event_repository = event_repository

        super().__init__(event_repository)

    def create_event(self, event_info: CreateEvent, user: User) -> Event:
        """Creates a new event"""
        categories = []

        for category in event_info.categories:
            categories.append(Category(name=category))

        event_info.categories = categories

        event = self.event_repository.create(event_info, user.id)

        return event

    def get_list(self, schema):
        return self.event_repository.read_by_options(schema)

    def get_events_by_user(self, schema, owner_id: UUID):
        """"""
        events = self.event_repository.get_events_by_user(schema, owner_id)

        return events

    def get_by_id(self, id: str):
        return self.event_repository.get_event_by_id(UUID(id))

    def patch(self, event_info: UpdateEvent, event_id: UUID, user_id: UUID):
        return self.event_repository.update_event(event_info, event_id, user_id)
