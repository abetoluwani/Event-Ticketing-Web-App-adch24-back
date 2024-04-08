#!/usr/bin/env python3
# File: __init__.py
# Author: Oluwatobiloba Light
"""Init file"""


from fastapi import APIRouter
from app.routes.index import index_router as IndexRouter
from app.routes.auth.index import auth_router as AuthRouter


api = APIRouter()

api.include_router(IndexRouter)
api.include_router(AuthRouter)

__all__ = ["api"]
