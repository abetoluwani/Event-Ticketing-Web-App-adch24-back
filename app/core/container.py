#!/usr/bin/env python3
# File: container.py
# Author: Oluwatobiloba Light
"""Container"""

from dependency_injector import containers, providers

from app.core.config import configs
from app.core.database import Database
from app.repository import *
from app.repository.event_repository import EventRepository
from app.services import *
from app.services.auth_service import AuthService
from app.services.event_service import EventService


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "app.api.endpoints.auth",
            "app.api.endpoints.user",
            "app.api.endpoints.event",
            "app.core.dependencies",
        ]
    )

    db = providers.Singleton(
        Database, db_url=configs.DATABASE_URI)

    # Asynchronous session provider (if needed)
    # async_db = providers.Singleton(
    #     AsyncDatabase, db_url=configs.DATABASE_URI, engine_type="prisma"
    # )

    user_repository = providers.Factory(
        UserRepository, session_factory=db.provided.session)

    # async_user_repository = providers.Factory(
    #     UserRepository, session_factory=async_db.provided.session)

    event_repository = providers.Factory(EventRepository,
                                         session_factory=db.provided.session)

    auth_service = providers.Factory(
        AuthService, user_repository=user_repository)

    user_service = providers.Factory(
        UserService, user_repository=user_repository)

    # async_user_service = providers.Factory(
    #     UserService, user_repository=async_user_repository)

    event_service = providers.Factory(
        EventService, event_repository=event_repository)
