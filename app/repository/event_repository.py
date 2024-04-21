#!/usr/bin/env python3
# File: event_repository.py
# Author: Oluwatobiloba Light
"""Event Repository"""


from typing import Callable
from uuid import UUID
from sqlalchemy import String, Uuid, func, or_, cast
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.core.exceptions import DuplicatedError
from app.model.event import Event
from app.model.user import User
from app.repository.base_repository import BaseRepository
from app.util.query_builder import dict_to_sqlalchemy_filter_options
from app.core.config import configs
from sqlalchemy.orm import joinedload


class EventRepository(BaseRepository):
    def __init__(self, session_factory: Callable[[], Session]):
        self.session_factory = session_factory
        self.model = Event  # I want the type

        super().__init__(session_factory, Event)

    def create(self, schema):
        with self.session_factory() as session:
            query = self.model(**schema.dict())

            try:
                session.add(query)

                session.commit()

                session.refresh(query)
            except IntegrityError as e:
                print(e.orig)
                if "duplicate" in str(e.orig):
                    raise DuplicatedError(detail="Event already exists!")
                raise DuplicatedError(detail=str(e.orig))

            return query

    def read_by_options(self, schema, eager=False):
        with self.session_factory() as session:
            # if schema and schema.model_dump():
            schema_as_dict = schema.dict(
                exclude_none=True) if schema and schema.model_dump() else {}

            ordering = schema_as_dict.get("ordering", configs.ORDERING)

            order_query = (
                getattr(self.model, ordering[1:]).desc()
                if ordering.startswith("-")
                else getattr(self.model, ordering).asc()
            )

            page = schema_as_dict.get("page", configs.PAGE)

            page_size = schema_as_dict.get("page_size", configs.PAGE_SIZE)

            filter_options = dict_to_sqlalchemy_filter_options(
                self.model, schema.dict(exclude_none=True))

            query = session.query(self.model)

            if eager:
                for eager in getattr(self.model, "eagers", []):
                    query = query.options(
                        joinedload(getattr(self.model, eager)))

            filtered_query = query.filter(filter_options)

            query = filtered_query.order_by(order_query)

            total_count = filtered_query.count()

            if page_size == "all":
                query = query.all()
                pages = 1
            else:
                page_size = int(page_size)
                pages = 0 if total_count < 1 else (1 if page_size > total_count else int(
                    total_count / page_size))

                query = query.limit(page_size).offset(
                    (page - 1) * page_size).all()

            return {
                "founds": query,
                "search_options": {
                    "page": page,
                    "pages": pages,
                    "page_size": page_size,
                    "ordering": ordering,
                    "total_count": total_count,
                },
            }

    def get_events_by_user(self, schema, owner_id: UUID, eager=False):
        """"""
        with self.session_factory() as session:
            schema_as_dict = schema.dict(
                exclude_none=True) if schema and schema.model_dump() else {}

            ordering = schema_as_dict.get("ordering", configs.ORDERING)

            order_query = (
                getattr(self.model, ordering[1:]).desc()
                if ordering.startswith("-")
                else getattr(self.model, ordering).asc()
            )

            page = schema_as_dict.get("page", configs.PAGE)

            page_size = schema_as_dict.get("page_size", configs.PAGE_SIZE)

            query = session.query(self.model)

            if eager:
                for eager in getattr(self.model, "eagers", []):
                    query = query.options(
                        joinedload(getattr(self.model, eager)))

            filtered_query = query.filter(
                cast(self.model.owner_id, Uuid) == cast(owner_id, Uuid))

            query = filtered_query.order_by(order_query)

            total_count = filtered_query.count()

            if page_size == "all":
                query = query.all()
                pages = 1
            else:
                page_size = int(page_size)
                pages = 0 if total_count < 1 else (1 if page_size > total_count else int(
                    total_count / page_size))

                query = query.limit(page_size).offset(
                    (page - 1) * page_size).all()

            return {
                "founds": query,
                "search_options": {
                    "page": page,
                    "pages": pages,
                    "page_size": page_size,
                    "ordering": ordering,
                    "total_count": total_count,
                },
            }
