#!/usr/bin/env python3
# File: auth.py
# Author: Oluwatobiloba Light
"""Authentication Router"""


import pathlib
from fastapi import APIRouter, Request, responses, status
from fastapi.encoders import jsonable_encoder
import google.auth
import google.auth.exceptions
import google.auth.transport
import google.auth.transport.requests
import google.oauth2.id_token
import oauthlib
import oauthlib.oauth2
import oauthlib.oauth2.rfc6749
from app.helpers.user import UserDB
from app.utils.utils import create_access_token, get_google_auth_state, get_remaining_minutes, google_auth_flow, verify_google_token, verify_password
from schema.user import CreateUser, CreateUserGoogle, User, UserLogin
from datetime import timedelta
from starlette.config import Config
from authlib.integrations.starlette_client import OAuth
from os import getenv
import google.oauth2.credentials
from google_auth_oauthlib.flow import Flow
import os
from datetime import datetime, timezone
from time import time


auth_router = APIRouter(
    responses={404: {'description': "Not found!"}}, tags=["Authentication"],
    prefix="/auth"
)

# OAuth settings

# # Set up oauth
# config_data = {'GOOGLE_CLIENT_ID': GOOGLE_CLIENT_ID,
#                'GOOGLE_CLIENT_SECRET': GOOGLE_CLIENT_SECRET}

# starlette_config = Config(environ=config_data)

# client_secret = os.path.join("./", "client_secret.json")

# flow = Flow.from_client_secrets_file(
#     client_secrets_file=client_secret,
#     redirect_uri="http://127.0.0.1:8000/auth",
#     scopes=['https://www.googleapis.com/auth/userinfo.profile', 'https://www.googleapis.com/auth/userinfo.email', 'openid'])

# oauth = OAuth2()

# oauth.(
#     name='google',
#     server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
#     client_kwargs={'scope': 'openid email profile',
#                    'redirect_url': 'http://127.0.0.1:8000/auth'}
# )


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

    print(existing_user)
    user_password = existing_user['password']

    if not verify_password(user.password, user_password):
        return responses.JSONResponse(
            content={"detail": "Invalid login!"},
            status_code=status.HTTP_401_UNAUTHORIZED
        )

    access_token_expires = timedelta(minutes=60*2)

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
    # authorization_url, state = flow.authorization_url(
    #     # Recommended, enable offline access so that you can refresh an access token without
    #     # re-prompting the user for permission. Recommended for web server apps.
    #     access_type='offline',
    #     # # Optional, enable incremental authorization. Recommended as a best practice.
    #     include_granted_scopes='true',
    #     # # Recommended, state value can increase your assurance that an incoming connection is the result
    #     # # of an authentication request.
    #     # # state=state,
    #     # # Optional, if your application knows which user is trying to authenticate, it can use this
    #     # # parameter to provide a hint to the Google Authentication Server.
    #     # login_hint='hint@example.com',
    #     # # Optional, set prompt to 'consent' will prompt the user for consent
    #     # prompt='consent'
    # )

    authorization_url, state = get_google_auth_state()

    request.session['state'] = state

    return responses.RedirectResponse(authorization_url)


@auth_router.get("/", summary="Google Authentication Callback",
                 response_model_exclude_none=True,
                 response_model=User)
async def google_auth(request: Request):
    """"""

    # try:
    #     flow.fetch_token(code=request.query_params.get('code'))
    # except (oauthlib.oauth2.rfc6749.errors.InvalidGrantError, ) as e:
    #     return responses.JSONResponse(
    #         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #         content={"detail": "An error has occured!",
    #                  "error": jsonable_encoder(e)})

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

    # try:
    #     user_info = google.oauth2.id_token.verify_oauth2_token(
    #         id_token=credentials._id_token, request=token_request,
    #         audience=GOOGLE_CLIENT_ID)
    # except (google.auth.exceptions.InvalidValue,
    #         google.auth.exceptions.InvalidOperation) as e:
    #     """"""
    #     return responses.JSONResponse(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         content={"detail": "An error has occured!", "error": e})

    # current_time_stamp = user_info['exp']

    # system_tz_offset = timezone(timedelta(hours=1))

    # # Get current time in system time zone (naive object)
    # local_time = datetime.now()

    # # Convert local time to UTC (considering system time zone offset)
    # current_utc_time = local_time.astimezone(system_tz_offset).timestamp()

    # time_delta = timedelta(seconds=current_time_stamp - int(current_utc_time))

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
            content={"detail": "An error occured while creating a new account!"})

    token = create_access_token(
        data={"sub": user.email},
        expires_delta=timedelta(minutes=int(remaining_minutes)))

    return responses.JSONResponse(
        content={
            "user": User(**jsonable_encoder(user)).to_json(),
            "access_token": token
        })
