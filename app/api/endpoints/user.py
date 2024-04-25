#!/usr/bin/env python3
# File: user.py
# Author: Oluwatobiloba Light
"""User endpoint"""


from typing import List
from uuid import UUID
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder

from app.core.container import Container
from app.core.dependencies import get_current_user
from app.core.exceptions import ValidationError
from app.core.security import JWTBearer, get_password_hash
from app.model.category import Category
from app.model.event import Event
from app.schema.base_schema import Blank
from app.schema.event_schema import Event_, FindEventQuery, FindEventsResult, FindUserEventsResult, GetUserEventsQuery
from app.schema.user_schema import FindUserQuery, \
    FindUserQueryOptions, FindUserResult, UpsertUser, User, User_
from app.services.event_service import EventService
from app.services.user_service import UserService

router = APIRouter(
    prefix="/user", tags=["user"], dependencies=[Depends(JWTBearer())])


@router.get("/all", response_model=FindUserResult)
@inject
async def get_user_list(
    find_query: FindUserQuery = Depends(),
    service: UserService = Depends(Provide[Container.user_service]),
    # current_user: User = Depends(get_current_super_user),
):
    return service.get_list(FindUserQueryOptions(
        **jsonable_encoder(find_query.request.query_params)
    ))


@router.get("/events", summary="List of events by user",
            response_model=FindUserEventsResult
            )
@inject
async def get_user_events(
    find_query: FindEventQuery = Depends(),
    event_service: EventService = Depends(Provide[Container.event_service]),
    current_user: User = Depends(get_current_user),
):
    events = event_service.get_events_by_user(find_query, current_user.id)

    for event in events['founds']:
        category_list: List[Category] = []

        for category in event.categories:
            category_list.append(
                Category(**category.model_dump()))

        owner = User_(**event.owner.model_dump())

        event = Event_(**event.model_dump(),
                       categories=category_list, owner=owner)

    return events


@router.get("/{user_id}", response_model=User)
@inject
async def get_user(
    user_id: str,
    service: UserService = Depends(Provide[Container.user_service]),
    current_user: User = Depends(get_current_user),
):
    user = service.get_by_id(user_id)

    delattr(user, "password")

    return user


# @router.post("", response_model=User)
# @inject
# async def create_user(
#     user: UpsertUser,
#     service: UserService = Depends(Provide[Container.user_service]),
#     current_user: User = Depends(get_current_super_user),
# ):
#     return service.add(user)


@router.patch("/", response_model=User)
@inject
async def update_user(
    # user_id: UUID,
    user: UpsertUser,
    service: UserService = Depends(Provide[Container.user_service]),
    current_user: User = Depends(get_current_user),
):

    if user.password and len(user.password) < 6:
        raise ValidationError("Password is too short!")
    elif user.password and len(user.password) >= 6:
        user.password = get_password_hash(user.password)

    updated_user = service.patch(current_user.id, user)

    delattr(updated_user, 'password')

    return updated_user


@router.delete("/", response_model=None)
@inject
async def delete_user(
    service: UserService = Depends(Provide[Container.user_service]),
    current_user: User = Depends(get_current_user),
):
    user = service.remove_by_id(str(current_user.id))

    return {
        "message": "Account deleted successfully!"
    }
