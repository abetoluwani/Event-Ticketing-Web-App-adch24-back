#!/usr/bin/env python3
# File: base_model.py
# Author: Oluwatobiloba Light
"""Base Model"""


from datetime import datetime
from uuid import UUID, uuid4
from sqlmodel import Column, DateTime, Field, SQLModel, func


class BaseModel(SQLModel):
    id: UUID = Field(primary_key=True, default=uuid4())
    created_at: datetime = Field(Column(
        DateTime(timezone=True), default=func.now()))

    updated_at: datetime = Field(Column(
        DateTime(timezone=True), default=func.now(), onupdate=func.now()))
