#!/usr/bin/env python3
# File: user/index.py
# Author: Oluwatobiloba Light
"""User route"""


from fastapi.encoders import jsonable_encoder
from app.utils.user import UserDB
from fastapi import APIRouter, Depends, responses, status
from app.utils.utils import custom_auth
from schema.user import UpdateUser, User


user_router = APIRouter(
    responses={404: {'description': "Not found!"}}, tags=["User"],
    prefix="/user"
)


@user_router.get("/profile", summary="User profile",
                 response_model_exclude_none=True)
async def user_profile(user: User = Depends(custom_auth)):
    """"""
    return responses.JSONResponse(
        content=user.to_json(),
        status_code=status.HTTP_200_OK
    )


@user_router.patch("/profile", summary="Update a user's data",
                   response_model_exclude_none=True,
                   response_model=User)
async def update_user_profile(form_data: UpdateUser,
                              user: User = Depends(custom_auth)):
    """"""
    update_user = await UserDB().update_user(form_data, user=user)

    if update_user:
        return responses.JSONResponse(content=update_user.to_json())

    return responses.JSONResponse(content=user.to_json())
