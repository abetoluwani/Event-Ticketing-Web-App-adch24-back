#!/usr/env/bin python3
# File: helpers/event.py
# Author: Oluwatobiloba Light
"""Evenrt helper class"""


from typing import List, Any
from app.db import Database
from schema.event import CreateEventInput, Event
from prisma.errors import PrismaError


class EventDb(Database):
    """"""

    async def all_events(self, user_id: str):
        """Returns all user events"""
        events = await self.db.event.find_many(where={"user_id": user_id})
        events_json: List[Any] = []

        for i in range(len(events)):
            events_json.append(events[i])

        print(events_json)
        return events_json

    async def create_event(self, user_id: str, form_data: CreateEventInput):
        """"""
        try:
            await self.db.event.create(
                data={
                    **form_data.to_json()
                }
            )

        except (PrismaError, ) as e:
            pass
