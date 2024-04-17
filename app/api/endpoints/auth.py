#!/usr/bin/env python3
# File: auth.py
# Author: Oluwatobiloba Light
"""Auth endpoint"""


from typing import Any, Mapping, Optional
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Request, responses, status
from fastapi.encoders import jsonable_encoder

from app.core.container import Container
from app.core.dependencies import get_current_active_user
from app.schema.auth_schema import GoogleSignIn, SignIn, SignInResponse, SignUp
from app.schema.user_schema import User
from app.services.auth_service import AuthService
from app.util.google import get_google_auth_state, google_auth_flow, verify_google_token

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/sign-in", response_model=SignInResponse)
@inject
async def sign_in(user_info: SignIn, service: AuthService =
                  Depends(Provide[Container.auth_service])):
    return service.sign_in(user_info)


@router.post("/sign-up", response_model=User)
@inject
async def sign_up(user_info: SignUp, service: AuthService =
                  Depends(Provide[Container.auth_service])):
    return service.sign_up(user_info)


@router.get("/google/login", summary="Google Login Authentication")
async def google_login(request: Request):
    """"""
    authorization_url, state = get_google_auth_state()

    request.session['state'] = state

    return responses.RedirectResponse(authorization_url)


@router.get("/", summary="Google Login Authentication")
@inject
async def google_login_callback(request: Request, service: AuthService =
                                Depends(Provide[Container.auth_service])):
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

    user_info: Optional[Mapping[str, Any]] = verify_google_token(
        id_token=credentials._id_token)

    return service.google_sign_up(GoogleSignIn(**jsonable_encoder(user_info)))


@router.get("/me", response_model=User)
@inject
async def get_me(current_user: User = Depends(get_current_active_user)):
    return current_user
