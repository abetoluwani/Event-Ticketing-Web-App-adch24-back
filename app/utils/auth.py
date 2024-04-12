#!/usr/bin/env python3
# File: utils/auth.py
# Author: Oluwatobiloba Light
"""Utils module"""


import google.auth
import google.auth.exceptions
import google.auth.transport
import google.auth.transport.requests
from google_auth_oauthlib.flow import Flow
from typing import Any, Dict, Mapping, Tuple, Union
from fastapi.encoders import jsonable_encoder
import oauthlib
import oauthlib.oauth2
import oauthlib.oauth2.rfc6749
from passlib.context import CryptContext
from jose import JWTError, jwt, ExpiredSignatureError
from datetime import datetime, timezone, timedelta
from os import getenv
from fastapi import Depends, HTTPException, Request, status
from schema.user import User
import google.oauth2.id_token
import os


password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

GOOGLE_CLIENT_ID = getenv('GOOGLE_CLIENT_ID') or None

GOOGLE_CLIENT_SECRET = getenv('GOOGLE_CLIENT_SECRET') or None

if GOOGLE_CLIENT_ID is None or GOOGLE_CLIENT_SECRET is None:
    raise BaseException('Missing env variables')


client_secret = os.path.join("./", "client_secret.json")

# client_secret = {"web": {"client_id": GOOGLE_CLIENT_ID, "project_id": "event-ticketing-419913", "auth_uri": "https://accounts.google.com/o/oauth2/auth", "token_uri": "https://oauth2.googleapis.com/token",
#                          "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs", "client_secret": GOOGLE_CLIENT_SECRET, "redirect_uris": ["http://127.0.0.1:8000/auth"], "javascript_origins": ["http://127.0.0.1:8000"]}
#                  }

print(client_secret)

flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secret,
    redirect_uri="http://127.0.0.1:8000/auth",
    scopes=['https://www.googleapis.com/auth/userinfo.profile',
            'https://www.googleapis.com/auth/userinfo.email', 'openid'])


def hash_password(password: str) -> str:
    """
    Hash a plain-text password using a secure hashing algorithm.

    Args:
        password (str): The plain-text password to be hashed.

    Returns:
        str: The hashed representation of the input password.
    """
    return password_context.hash(password)


def verify_password(password: str, hashed_pass: str) -> bool:
    """
    Verify whether a given plain-text password matches a hashed password.

    Args:
        password (str): The plain-text password to be verified.
        hashed_pass (str): The hashed password for comparison.

    Returns:
        bool: True if the plain-text password matches the hashed password,
        False otherwise.
    """
    return password_context.verify(password, hashed_pass)


def create_access_token(data: dict, expires_delta:
                        Union[timedelta, None] = None) -> str:
    """"""
    SECRET_KEY = getenv("SECRET_KEY")

    if SECRET_KEY is None:
        raise Exception("🚨 JWT SECRET KEY NOT SET")

    to_encode = data.copy()

    if expires_delta:
        system_tz_offset = timezone(timedelta(hours=1))

        local_time = datetime.now()

        expire = local_time.astimezone(system_tz_offset) + expires_delta
    else:
        expire = datetime.now().astimezone(timezone(timedelta(hours=1)))\
            + timedelta(minutes=60)

    to_encode.update({"exp": expire})

    encoded_jwt = None

    encoded_jwt = jwt.encode(
        to_encode, key=SECRET_KEY, algorithm=getenv("JWT_ALGORITHM") or "HS256")

    return encoded_jwt


def verify_access_token(request: Request) -> Union[dict, None]:
    """"""
    SECRET_KEY = getenv("SECRET_KEY")

    if SECRET_KEY is None:
        raise Exception("🚨 JWT SECRET KEY NOT SET")

    token: str

    authorization = request.headers.get("Authorization")

    if authorization is None:
        return None

    authorization = authorization.split()

    if len(authorization) < 2:
        return None

    token = authorization[1]

    try:
        payload = jwt.decode(token, key=SECRET_KEY,
                             algorithms=getenv("JWT_ALGORITHM") or "HS256")
        return payload
    except (JWTError, ExpiredSignatureError) as e:
        print("🚨 Token Error:", e)
        # get refresh token here...

    return None


async def custom_auth(payload: Dict[str, Any] =
                      Depends(verify_access_token)) -> User:
    """"""
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Unauthorized!",
                            headers={"Authorization": "Bearer"})

    from app.helpers.user import UserDB  # importing here to avoid circular import

    user = await UserDB().user_exists(email=payload["sub"])

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Unauthorized!",
                            headers={"Authorization": "Bearer"})

    return User(**jsonable_encoder(user))


def get_google_auth_state() -> Tuple[str, str]:
    """"""
    authorization_url, state = flow.authorization_url(
        # Recommended, enable offline access so that you can refresh an access token without
        # re-prompting the user for permission. Recommended for web server apps.
        access_type='offline',
        # # Optional, enable incremental authorization. Recommended as a best practice.
        include_granted_scopes='true',
        # # Recommended, state value can increase your assurance that an incoming connection is the result
        # # of an authentication request.
        # # state=state,
        # # Optional, if your application knows which user is trying to authenticate, it can use this
        # # parameter to provide a hint to the Google Authentication Server.
        # login_hint='hint@example.com',
        # # Optional, set prompt to 'consent' will prompt the user for consent
        # prompt='consent'
    )

    return (authorization_url, state)


def google_auth_flow(code: str):
    """"""
    try:
        flow.fetch_token(code=code)

        return flow
    except (oauthlib.oauth2.rfc6749.errors.InvalidGrantError, ) as e:
        return None


def verify_google_token(id_token: Any) -> Union[Mapping[str, Any], None]:
    """"""
    token_request = google.auth.transport.requests.Request()

    try:
        user_info = google.oauth2.id_token.verify_oauth2_token(
            id_token=id_token, request=token_request,
            audience=GOOGLE_CLIENT_ID)

        return user_info
    except (google.auth.exceptions.InvalidValue,
            google.auth.exceptions.InvalidOperation) as e:
        """"""
        return None
