#!/usr/bin/env python3
# File: event_repository.py
# Author: Oluwatobiloba Light
"""Event Repository"""


import json
from typing import Callable, List
from uuid import UUID, uuid4
from fastapi.encoders import jsonable_encoder
from sqlalchemy import String, Uuid, func, or_, cast
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.core.exceptions import DuplicatedError, NotFoundError
from app.model.category import Category
from app.model.event import Event
from app.model.user import User
from app.repository.base_repository import BaseRepository
from app.schema.event_schema import FindEventsResult, FindUserEventsResult
from app.util.query_builder import dict_to_sqlalchemy_filter_options
from app.core.config import configs
from sqlalchemy.orm import joinedload


class EventRepository(BaseRepository):
    def __init__(self, session_factory: Callable[[], Session]):
        self.session_factory = session_factory
        self.model = Event  # I want the type

        super().__init__(session_factory, Event)

    def create(self, schema, user_id: UUID):
        with self.session_factory() as session:
            category_session = session.query(
                Category)

            categories: List['Category'] = [*schema.categories]

            delattr(schema, 'categories')

            query = self.model(id=uuid4(), **schema.dict())

            query.owner_id = user_id

            for category in categories:
                cat = category_session.filter(cast(Category.name, String)
                                              == cast(category.name, String)).all()

                if len(cat) < 1:
                    # create new category here
                    pass
                else:
                    query.categories.append(cat[0])

            try:
                session.add(query)

                session.commit()

                event_with_categories = session.query(
                    self.model).filter_by(id=query.id).options(joinedload(Event.categories)).first()

                # session.refresh(query)
                if event_with_categories:
                    return event_with_categories
                else:
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

            query = filtered_query.order_by(order_query).options(
                joinedload(self.model.categories), joinedload(self.model.owner))

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

            query = filtered_query.order_by(order_query).options(
                joinedload(self.model.categories), joinedload(self.model.owner))

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

    def get_event_by_id(self, event_id: UUID, eager=False):
        with self.session_factory() as session:
            query = session.query(self.model)

            if eager:
                for eager in getattr(self.model, "eagers", []):
                    query = query.options(
                        joinedload(getattr(self.model, eager)))

            query = query.filter(cast(self.model.id, Uuid) == cast(event_id, Uuid))\
                .options(joinedload(self.model.categories), joinedload(self.model.owner)).first()

            if not query:
                raise NotFoundError(detail=f"not found id : {id}")
            return query

    def update_event(self, schema, event_id: UUID, user_id: UUID, eager=False):
        """Update an event by ID"""
        with self.session_factory() as session:
            category_session = session.query(
                Category)

            categories: List['Category'] = [*schema.categories]

            delattr(schema, 'categories')

            query = self.model(**schema.dict())

            for category in categories:
                cat = category_session.filter(cast(Category.name, String)
                                              == cast(category, String)).all()

                if len(cat) < 1:
                    # create new category here
                    pass
                else:
                    query.categories.append(cat[0])

            event = session.get(self.model, event_id)

            if event:
                for [k, v] in query.model_dump().items():
                    if v is not None and k not in ['id', 'owner_id', 'created_at', 'updated_at']:
                        setattr(event, k, v)

            # session.query(self.model)\
            #     .filter(cast(self.model.id, Uuid) == cast(event_id, Uuid),
            #             cast(self.model.owner_id, Uuid) == cast(user_id, Uuid))\
            #     .update({'name': 'oops', 'categories': query.categories}, synchronize_session='fetch')

            session.commit()

            return self.get_event_by_id(event_id)

    def delete_event_by_id(self, id: str, user_id: str):
        with self.session_factory() as session:
            query = session.query(self.model).filter(cast(self.model.id, Uuid) == cast(
                id, Uuid), cast(self.model.owner_id, Uuid) == cast(user_id, Uuid)).first()

            if not query:
                raise NotFoundError(detail=f"not found id : {id}")

            session.delete(query)

            session.commit()

            print(query)

            return None
