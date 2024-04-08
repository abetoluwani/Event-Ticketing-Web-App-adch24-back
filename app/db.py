#!/usr/bin/env python3
# File: db.py
# Author: Oluwatobiloba Light
"""Database init"""
from typing import Union
from prisma import Prisma, Client


class Database:
    """"""
    _client: Union[Prisma, None] = None

    def __init__(self) -> None:
        """Initialize database"""
        if not Database._client:
            print("⏳ Initializing Database...")
            Database._client = Prisma(auto_register=True)

    @property
    def db(self):
        if not Database._client:
            raise RuntimeError("Database client not initialized")
        return Database._client

    async def connect(self):
        """Connect to the database"""
        await self.db.connect()

    async def disconnect(self):
        await self.db.disconnect()
