#!/usr/bin/env python3
# File: main.py
# Author: Oluwatobiloba Light
"""Event Ticketing entry point"""

from app import api
from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.db import Database
from fastapi.middleware.cors import CORSMiddleware
from prisma import errors
from os import getenv
from starlette.middleware.sessions import SessionMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and Shutdown events"""
    db = Database()

    try:
        await db.connect()
        print("✅ Database Connected!")
    except errors.PrismaError as e:
        print("error: ", e)
        print("❌ DB Connection failed")
        raise Exception("🚨 Database connection failed! 🚨")

    yield
    await db.disconnect()


def init_app():
    """Initialize app"""
    init = FastAPI(version="1.0.0", lifespan=lifespan)

    origins = [
        "http://localhost.tiangolo.com",
        "https://localhost.tiangolo.com",
        "http://localhost:8000",
        "http://localhost:3000",
        "http://localhost",
    ]

    init.add_middleware(CORSMiddleware,
                        allow_origins=origins,
                        allow_credentials=True,
                        allow_methods=["*"],
                        allow_headers=["*"]
                        # allow_methods=["GET", "POST", "PUT", "DELETE",
                        #                "OPTION"],
                        # allow_headers=["Content-Type", "Authorization",
                        #                "WWW-AUTHENTICATE"]
                        )

    SECRET_KEY = getenv('SECRET_KEY') or None

    if SECRET_KEY is None:
        raise RuntimeError('Missing SECRET_KEY')

    init.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

    init.include_router(api)

    return init


app = init_app()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_, exc):
    errors = []
    for error in exc.errors():
        field = ''.join(error['loc'][1]) if len(
            error['loc']) > 1 else error['loc'][0]
        print(error)
        errors.append({
            'field': field,
            'message': error['msg']
        })
    return JSONResponse(status_code=422, content={
        "detail": "Validation error", "errors": errors})
