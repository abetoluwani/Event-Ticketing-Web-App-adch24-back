#!/usr/bin/env python3
# File: event_repository.py
# Author: Oluwatobiloba Light
"""Event Repository"""


from typing import Callable
from sqlalchemy.orm import Session
from app.model.event import Event
from app.repository.base_repository import BaseRepository


class EventRepository(BaseRepository):
    def __init__(self, session_factory: Callable[[], Session]):
        self.session_factory = session_factory
        super().__init__(session_factory, Event)
