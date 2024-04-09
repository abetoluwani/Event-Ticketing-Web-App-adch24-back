#!/usr/bin/env python3
# File: __init__.py
# Author: Oluwatobiloba Light
"""Init file"""


from fastapi import APIRouter
from app.routes.index import index_router as IndexRouter
from app.routes.auth.index import auth_router as AuthRouter
from app.routes.user.index import user_router as UserRouter


api = APIRouter()

api.include_router(IndexRouter)
api.include_router(AuthRouter)
api.include_router(UserRouter)

__all__ = ["api"]
