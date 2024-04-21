#!/usr/bin/env python3
# File: user.py
# Author: Oluwatobiloba Light
"""User endpoint"""


from uuid import UUID
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder

from app.core.container import Container
from app.core.dependencies import get_current_user
from app.core.exceptions import ValidationError
from app.core.security import JWTBearer, get_password_hash
from app.schema.base_schema import Blank
from app.schema.event_schema import FindEventQuery, GetUserEventsQuery
from app.schema.user_schema import FindUserQuery, \
    FindUserQueryOptions, FindUserResult, UpsertUser, User
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


@router.get("/events")
@inject
async def get_user_events(
    find_query: FindEventQuery = Depends(),
    event_service: EventService = Depends(Provide[Container.event_service]),
    current_user: User = Depends(get_current_user),
):
    events = event_service.get_events_by_user(find_query, current_user.id)

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


@router.patch("/{user_id}", response_model=User)
@inject
async def update_user(
    user_id: UUID,
    user: UpsertUser,
    service: UserService = Depends(Provide[Container.user_service]),
    current_user: User = Depends(get_current_user),
):

    if user.password and len(user.password) < 6:
        raise ValidationError("Password is too short!")
    elif user.password and len(user.password) >= 6:
        user.password = get_password_hash(user.password)

    updated_user = service.patch(user_id, user)

    delattr(updated_user, 'password')

    return updated_user


@router.delete("/{user_id}", response_model=Blank)
@inject
async def delete_user(
    user_id: str,
    service: UserService = Depends(Provide[Container.user_service]),
    current_user: User = Depends(get_current_user),
):
    return service.remove_by_id(user_id)
