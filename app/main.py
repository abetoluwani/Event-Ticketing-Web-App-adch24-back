#!/usr/bin/env python3
# File: main.py
# Author: Oluwatobiloba Light
"""Event Ticketing entry point"""

from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
import uvicorn
from app.db import Database
from fastapi.middleware.cors import CORSMiddleware
from prisma import errors


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
                        allow_methods=["GET", "POST", "PUT", "DELETE",
                                       "OPTION"],
                        allow_headers=["Content-Type", "Authorization",
                                       "WWW-AUTHENTICATE"])

    # db = Database()

    # @init.on_event("startup")
    # async def startup():
    #     try:
    #         await db.connect()
    #         print("✅ Database Connected!")
    #     except errors.PrismaError as e:
    #         print("error: ", e)
    #         print("❌ DB Connection failed")
    #         raise Exception("🚨 Database connection failed! 🚨")

    # @init.on_event("shutdown")
    # async def shutdown():
    #     await db.disconnect()

    from app import api

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


if __name__ == "__main__":
    uvicorn.run('app.main:app',
                host="0.0.0.0", port=8000, reload=True)
