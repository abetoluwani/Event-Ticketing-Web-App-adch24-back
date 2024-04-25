#!/usr/bin/env python3
# File: event.py
# Author: Oluwatobiloba Light
"""Event endpoint"""


from typing import List
from uuid import UUID
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from app.core.container import Container
from app.core.dependencies import get_current_user
from app.core.security import JWTBearer
from app.model.category import Category
from app.model.user import User
from app.schema.category_schema import CreateCategory
from app.schema.event_schema import CreateEvent, Event, Event_, FindEventQuery, \
    FindEventQueryOptions, FindEventsResult, UpdateEvent
from app.schema.user_schema import User_
from app.services.category_service import CategoryService
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
    events = service.get_list(FindEventQueryOptions(
        **jsonable_encoder(find_query)
    ))

    print("events", events['founds'])

    return events


@router.post("/category/create", summary="Create event category",
             dependencies=[Depends(JWTBearer())],
             response_model=Category)
@inject
async def create_event_category(
    category_info: CreateCategory,
    service: CategoryService = Depends(Provide[Container.category_service]),
    current_user: User = Depends(get_current_user),

):
    """Create event category"""
    category = service.create_category(category_info)

    return category


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

    categories = event.categories

    event = Event(**event.model_dump(), categories=[*categories],
                  owner=User_(**owner.model_dump()))

    return event


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

    categories: List[Category] = []

    for category in event.categories:
        categories.append(Category(**category.model_dump()))

    return Event(**event.model_dump(), categories=categories,
                 owner=User_(**owner.model_dump()))


@router.patch("/{event_id}", summary="Update an event",
              dependencies=[Depends(JWTBearer())],
              response_model=Event
              )
@inject
async def update_event(
    event_id: str,
    event_info: UpdateEvent,
    service: EventService = Depends(Provide[Container.event_service]),
    current_user: User = Depends(get_current_user)
):
    event = service.patch(event_info, UUID(event_id), current_user.id)

    return event


# @router.delete("/{event_id}", summary="Delete an event",
#               dependencies=[Depends(JWTBearer())],
#               response_model=Event
#               )
# @inject
# async def delete_event(
#     event_id: str,
#     event_info: UpdateEvent,
#     service: EventService = Depends(Provide[Container.event_service]),
#     current_user: User = Depends(get_current_user)
# ):
#     event = service.patch(event_info, UUID(event_id), current_user.id)

#     return event


@router.get("/{owner_id}/all", summary="Get all events of a user",
            response_model=FindEventsResult)
@inject
async def get_user_events(
    owner_id: str,
    find_query: FindEventQuery = Depends(),
    service: EventService = Depends(Provide[Container.event_service]),
    user_service: UserService = Depends(Provide[Container.user_service])
):
    events = service.get_events_by_user(find_query, UUID(owner_id))

    for event in events['founds']:
        category_list: List[Category] = []

        for category in event.categories:
            category_list.append(
                Category(**category.model_dump()))

        owner = User_(**event.owner.model_dump())

        event = Event_(**event.model_dump(),
                       categories=category_list, owner=owner)


    return events
