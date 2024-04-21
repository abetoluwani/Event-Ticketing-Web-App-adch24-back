#!/usr/bin/env python3
# File: event.py
# Author: Oluwatobiloba Light
"""Event endpoint"""


from typing import List, Optional
from uuid import UUID
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from app.core.container import Container
from app.core.dependencies import get_current_user
from app.core.security import JWTBearer
from app.model.user import User
from app.schema.event_schema import CreateEvent, Event, Event_, FindEventQuery, FindEventQueryOptions, FindEventsResult, GetUserEventsQuery
from app.schema.user_schema import User_
from app.services.event_service import EventService
from app.services.user_service import UserService


router = APIRouter(
    prefix="/event", tags=["event"],
    # dependencies=[Depends(JWTBearer())]
)


@router.get("/all", summary="All events", response_model=FindEventsResult)
@inject
async def get_events(
    find_query: FindEventQuery = Depends(),
    service: EventService = Depends(Provide[Container.event_service]),
):
    # print(find_query)
    events = service.get_list(FindEventQueryOptions(
        **jsonable_encoder(find_query)
    ))

    return events


@router.post("/create", summary="Create an event",
             dependencies=[Depends(JWTBearer())],
             response_model=Event
             )
@inject
async def create_event(
    event_info: CreateEvent,
    service: EventService = Depends(Provide[Container.event_service]),
    user_service: UserService = Depends(Provide[Container.user_service]),
    current_user: User = Depends(get_current_user),
):
    event = service.create_event(event_info, current_user)

    owner = user_service.get_by_id(str(current_user.id))

    return Event(**event.model_dump(), owner=User_(**owner.model_dump()))


@router.get("/{event_id}", summary="Get an event", response_model=Event)
@inject
async def get_event(
    event_id: str,
    service: EventService = Depends(Provide[Container.event_service]),
    user_service: UserService = Depends(Provide[Container.user_service])
):
    event = service.get_by_id(event_id)

    owner = user_service.get_by_id(str(event.owner_id))

    delattr(owner, "password")

    return Event(**event.model_dump(), owner=User_(**owner.model_dump()))


@router.get("/{owner_id}/all", summary="Get all events of a user")
@inject
async def get_user_events(
    owner_id: str,
    find_query: FindEventQuery = Depends(),
    service: EventService = Depends(Provide[Container.event_service]),
    user_service: UserService = Depends(Provide[Container.user_service])
):
    events = service.get_events_by_user(find_query, UUID(owner_id))

    return events
