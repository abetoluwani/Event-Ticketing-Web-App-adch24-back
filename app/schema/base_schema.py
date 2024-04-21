#!/usr/bin/env python3
# File: base_schema.py
# Author: Oluwatobiloba Light
"""Base Schema"""


from datetime import datetime
from typing import List, Optional, Union
from uuid import UUID
from pydantic import BaseModel, Field


class ModelBaseInfo(BaseModel):
    id: UUID
    created_at: datetime
    updated_at: datetime


class FindBase(BaseModel):
    ordering: Optional[str]
    page: Optional[int]
    page_size: Optional[Union[int, str]]
    pages: Optional[int]


class FindQueryOptions(BaseModel):
    page: Optional[int] = Field(default=None)
    ordering: Optional[str] = Field(default=None)
    page_size: Optional[Union[int, str]] = Field(default=None)


class SearchOptions(FindBase):
    total_count: Optional[int]


class FindResult(BaseModel):
    founds: Optional[List]
    search_options: Optional[SearchOptions]


class FindDateRange(BaseModel):
    created_at__lt: str
    created_at__lte: str
    created_at__gt: str
    created_at__gte: str


class Blank(BaseModel):
    pass
