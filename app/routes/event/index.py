#!/usr/bin/env python3
# File: event/index.py
# Author: Oluwatobiloba Light
"""Event Route"""


from typing import List
from fastapi import APIRouter, Depends, responses, status
from app.helpers.event import EventDb
from app.utils.utils import custom_auth
from schema.event import Event
from schema.user import User


event_router = APIRouter(
    prefix="/event",
    responses={404: {'description': "Not found!"}}, tags=["Event"],
)


@event_router.get("/all", summary="Get all user events",
                  response_model_exclude_none=True,
                  response_model=List[Event])
async def events(user: User = Depends(custom_auth)):
    """"""
    events = await EventDb().all_events(user.id)

    return responses.JSONResponse(
        content={"events": events},
        status_code=status.HTTP_200_OK
    )


@event_router.post("/new", summary="Create a new event",
                   response_model_exclude_none=True,
                   response_model=Event)
async def create_event():
    """"""


    return responses.JSONResponse(
        content={"event": {}},
        status_code=status.HTTP_200_OK
    )
