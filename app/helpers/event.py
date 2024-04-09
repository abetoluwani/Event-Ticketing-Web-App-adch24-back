#!/usr/env/bin python3
# File: helpers/event.py
# Author: Oluwatobiloba Light
"""Evenrt helper class"""


from typing import List, Any
from app.db import Database
from schema.event import Event


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
