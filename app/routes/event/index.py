#!/usr/bin/env python3
# File: event/index.py
# Author: Oluwatobiloba Light
"""Event Route"""


from fastapi import APIRouter, Depends, responses, status
from app.utils.utils import custom_auth
from schema.event import Event
from schema.user import User


event_router = APIRouter(
    prefix="/event",
    responses={404: {'description': "Not found!"}}, tags=["Event"],
)


@event_router.get("/events", summary="Get all user events",
                  response_model_exclude_none=True,
                  response_model=Event)
def events(user: User = Depends(custom_auth)):
    """"""
    print(user)

    return responses.JSONResponse(
        content={},
        status_code=status.HTTP_200_OK
    )
