#!/usr/bin/env python3
# File: container.py
# Author: Oluwatobiloba Light
"""Container"""

from dependency_injector import containers, providers

from app.core.config import configs
from app.core.database import Database
from app.repository import *
from app.services import *
from app.services.auth_service import AuthService


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "app.api.endpoints.auth",
            "app.api.endpoints.user",
            "app.core.dependencies",
        ]
    )

    db = providers.Singleton(Database, db_url=configs.DATABASE_URI)

    user_repository = providers.Factory(
        UserRepository, session_factory=db.provided.session)

    auth_service = providers.Factory(
        AuthService, user_repository=user_repository)

    user_service = providers.Factory(
        UserService, user_repository=user_repository)
