#!/usr/bin/env python3
# File: database.py
# Author: Oluwatobiloba Light
"""Database"""

from contextlib import contextmanager
import os
from pathlib import Path
from typing import Any, AsyncGenerator, Generator, Optional, Union

from prisma import Prisma
from sqlalchemy import create_engine, orm
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session


Base = declarative_base()


# @as_declarative()
# class BaseModel:
#     id: Any
#     __name__: str

#     # Generate __tablename__ automatically
#     @declared_attr
#     def __tablename__(cls) -> str:
#         return cls.__name__.lower()


class Database:
    # _client: Optional[Prisma] = None

    def __init__(self, db_url: str) -> None:
        self._engine = create_engine(db_url, echo=False)

        self._session_factory = orm.scoped_session(
            orm.sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self._engine,
            ),
        )

    def create_database(self) -> None:
        Base.metadata.create_all(self._engine)

    @contextmanager
    def session(self) -> Generator[Session, None, None]:
        session: Session = self._session_factory()
        try:
            yield session
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
