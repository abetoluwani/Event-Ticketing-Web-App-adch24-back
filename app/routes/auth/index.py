#!/usr/bin/env python3
# File: auth.py
# Author: Oluwatobiloba Light
"""Authentication Router"""


from fastapi import APIRouter, Request, responses, status
from fastapi.encoders import jsonable_encoder
import google.oauth2.id_token
from app.helpers.user import UserDB
from app.utils.auth import create_access_token, get_google_auth_state, \
    google_auth_flow, verify_google_token, verify_password
from app.utils.utils import get_remaining_minutes
from schema.user import CreateUser, CreateUserGoogle, User, UserLogin
from datetime import timedelta
import google.oauth2.credentials


auth_router = APIRouter(
    responses={404: {'description': "Not found!"}}, tags=["Authentication"],
    prefix="/auth"
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
            new_user = await UserDB().create_user(user)

            return responses.JSONResponse(
                content={
                    "message": "Account created successfully!",
                    "user": jsonable_encoder(new_user)
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


@auth_router.post("/login", summary="User login",
                  response_model_exclude_none=True, response_model=User)
async def login(user: UserLogin):
    """"""
    existing_user = jsonable_encoder(await UserDB().user_exists(user.email))

    if not existing_user:
        return responses.JSONResponse(
            content={"detail": "Invalid login!"},
            status_code=status.HTTP_401_UNAUTHORIZED
        )

    user_password = existing_user['password']

    if not verify_password(user.password, user_password):
        return responses.JSONResponse(
            content={"detail": "Invalid login!"},
            status_code=status.HTTP_401_UNAUTHORIZED
        )

    access_token_expires = timedelta(minutes=60)

    token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires)

    return responses.JSONResponse(
        content={"user": existing_user,
                 "access_token": token},
        status_code=status.HTTP_200_OK
    )


@auth_router.get("/google", summary="Google Login")
async def google_login(request: Request):
    """"""
    authorization_url, state = get_google_auth_state()

    request.session['state'] = state

    return responses.RedirectResponse(authorization_url)


@auth_router.get("/", summary="Google Authentication Callback",
                 response_model_exclude_none=True,
                 response_model=User)
async def google_auth_callback(request: Request):
    """"""
    flow = google_auth_flow(str(request.query_params.get('code')))

    if flow is None:
        return responses.JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "An error has occured!"})

    if not request.session['state'] == request.query_params['state']:
        return responses.JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED,
                                      content={"detail": "Unauthorized"})

    credentials = flow.credentials

    request.session['credentials'] = {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes,
    }

    user_info = verify_google_token(id_token=credentials._id_token)

    if user_info is None:
        return responses.JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": "An error has occured!"})

    remaining_minutes = get_remaining_minutes(user_info)

    existing_user = await UserDB().user_exists(user_info['email'])

    if existing_user:
        token = create_access_token(
            data={"sub": existing_user.email},
            expires_delta=timedelta(minutes=int(remaining_minutes)))

        return responses.JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"user": User(**jsonable_encoder(existing_user)).to_json(),
                     "access_token": token})

    new_user = CreateUserGoogle(
        first_name=user_info['given_name'],
        last_name=user_info['family_name'],
        email=user_info['email'])

    user = await UserDB().create_user_google(new_user)

    if user is None:
        return responses.JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail":
                     "An error occured while creating a new account!"})

    token = create_access_token(
        data={"sub": user.email},
        expires_delta=timedelta(minutes=int(remaining_minutes)))

    return responses.JSONResponse(
        content={
            "user": User(**jsonable_encoder(user)).to_json(),
            "access_token": token
        })
