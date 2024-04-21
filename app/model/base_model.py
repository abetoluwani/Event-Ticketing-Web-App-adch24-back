#!/usr/bin/env python3
# File: base_model.py
# Author: Oluwatobiloba Light
"""Base Model"""


from datetime import datetime
from uuid import UUID, uuid4
from sqlmodel import DateTime, Field, SQLModel, func

from app.core.database import Base


class BaseModel(SQLModel  ):
    id: UUID = Field(primary_key=True, default=uuid4())

    created_at: datetime = Field(default=func.now())

    updated_at: datetime = Field(default=func.now())
