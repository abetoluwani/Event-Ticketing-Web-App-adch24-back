#!/usr/bin/env python3
# File: security.py
# Author: Oluwatobiloba Light
"""Security"""


from datetime import datetime, timedelta, timezone
from typing import Optional, Tuple
from fastapi import Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt
from passlib.context import CryptContext
from app.core.config import configs
from app.core.exceptions import AuthError


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ALGORITHM = "HS256"


def create_access_token(subject: dict, expires_delta:
                        Optional[timedelta] = None) -> Tuple[str, str]:
    if expires_delta:
        system_tz_offset = timezone(
            timedelta(minutes=configs.ACCESS_TOKEN_EXPIRE_MINUTES))

        local_time = datetime.now()

        expire = local_time.astimezone(system_tz_offset) + expires_delta
    else:
        system_tz_offset = timezone(
            timedelta(minutes=configs.ACCESS_TOKEN_EXPIRE_MINUTES))

        local_time = datetime.now()

        expire = local_time.astimezone(system_tz_offset) + \
            timedelta(minutes=configs.ACCESS_TOKEN_EXPIRE_MINUTES)

    payload = {"exp": expire, **subject}

    encoded_jwt = jwt.encode(payload, configs.SECRET_KEY, algorithm=ALGORITHM)

    expiration_datetime = expire.strftime(configs.DATETIME_FORMAT)

    return encoded_jwt, expiration_datetime


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def decode_jwt(token: str) -> dict:
    try:
        decoded_token = jwt.decode(
            token, configs.SECRET_KEY, algorithms=ALGORITHM)
        # return decoded_token if decoded_token["exp"] >= \
        #     int(round(datetime.utcnow().timestamp())) else {}
        expiration_time = datetime.fromtimestamp(
            decoded_token["exp"], timezone.utc)

        if expiration_time >= datetime.now(timezone.utc):
            return decoded_token
        else:
            return {}
    except Exception as e:
        return {}


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: Optional[HTTPAuthorizationCredentials] = \
            await super(JWTBearer, self).__call__(request)

        if credentials:
            if not credentials.scheme == "Bearer":
                raise AuthError(detail="Invalid authentication scheme.")

            if not self.verify_jwt(credentials.credentials):
                raise AuthError(detail="Invalid token or expired token.")

            return credentials.credentials
        else:
            raise AuthError(detail="Invalid authorization code.")

    def verify_jwt(self, jwt_token: str) -> bool:
        is_token_valid: bool = False

        try:
            payload = decode_jwt(jwt_token)
        except Exception as e:
            payload = None

        if payload:
            is_token_valid = True
        return is_token_valid
