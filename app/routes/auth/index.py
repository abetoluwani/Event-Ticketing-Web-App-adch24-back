#!/usr/bin/env python3
# File: auth.py
# Author: Oluwatobiloba Light
"""Authentication Router"""


from fastapi import APIRouter, responses, status
from app.utils.user import UserDB
from schema.user import CreateUser, User


auth_router = APIRouter(
    responses={404: {'description': "Not found!"}}, tags=["Authentication"]
)


@auth_router.post("/create", summary="Create an account",
                  response_model_exclude_none=True)
async def signup(user: CreateUser):
    """"""
    if len(user.password) < 6:
        return responses.JSONResponse(
            content={"detail": "Password is too short!"},
            status_code=status.HTTP_400_BAD_REQUEST)

    if user.password != user.cpassword:
        return responses.JSONResponse(
            content={"detail": "Password does not match!"},
            status_code=status.HTTP_400_BAD_REQUEST)

    existing_user = await UserDB().user_exists(user.email)

    if not existing_user:
        try:
            new_user = await UserDB().create_user({**user.to_json()})

            return responses.JSONResponse(
                content={
                    "message": "Account created successfully!",
                    "user": User(**new_user).to_json()
                },
                status_code=status.HTTP_201_CREATED)
        except:
            return responses.JSONResponse(
                content={
                    "detial": "Could not create an account! Please, try again"
                },
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return responses.JSONResponse(
        content={"detail": "User account exists!"},
        status_code=status.HTTP_200_OK)


# @auth_router.post("/login", summary="User login",
#                   response_model_exclude_none=True)
# async def login(user: UserLogin):
#     """"""
#     existing_user = await UserDB().user_exists(user.email)

#     if not existing_user:
#         return responses.JSONResponse(
#             content={"detail": "Invalid login!"},
#             status_code=status.HTTP_401_UNAUTHORIZED
#         )

#     user_password = jsonable_encoder(existing_user).get('password')
#     print(user_password)
#     if not verify_password(user.password, user_password):
#         return responses.JSONResponse(
#             content={"detail": "Invalid login!"},
#             status_code=status.HTTP_401_UNAUTHORIZED
#         )

#     return responses.JSONResponse(
#         content={"detail": "Ok!"},
#         status_code=status.HTTP_200_OK
#     )
