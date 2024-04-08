#!/usr/bin/env python3
# File: index.py
# Author: Oluwatobiloba Light
"""Index Router"""


from fastapi import APIRouter, responses, status


index_router = APIRouter(
    responses={404: {'description': "Not found!"}}, tags=["Index"]
)


@index_router.get("/", summary="Index route")
def index():
    return responses.JSONResponse(
        content={"status": "OK", "message": "Weclome to Event Ticketting!"},
        status_code=status.HTTP_200_OK)
