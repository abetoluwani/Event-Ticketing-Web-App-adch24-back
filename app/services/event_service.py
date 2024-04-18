#!/usr/bin/env python3
# File: event_services.py
# Author: Oluwatobiloba Light
"""Event Services"""


from app.repository.event_repository import EventRepository
from app.services.base_service import BaseService


class EventService(BaseService):
    def __init__(self, Event_repository: EventRepository):
        self.event_repository = Event_repository
        super().__init__(event_repository)
