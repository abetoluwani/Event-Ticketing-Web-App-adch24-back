#!/usr/bin/env python3
# File: schema.py
# Author: Oluwatobiloba Light
"""Schema"""


from typing import Optional
from pydantic import BaseModel


class AllOptional(BaseModel):
    # def __new__(cls, name, bases, namespaces, **kwargs):
    #     annotations = namespaces.get("__annotations__", {})

    #     for base in bases:
    #         annotations.update(base.__annotations__)

    #     for field in annotations:
    #         if not field.startswith("__"):
    #             annotations[field] = Optional[annotations[field]]

    #     namespaces["__annotations__"] = annotations

    #     return super().__new__(cls)
    @classmethod
    def __get_annotations__(cls):
        annotations = AllOptional.__get_annotations__()
        print("xx", annotations)
        for field, type_ in annotations.items():
            if not field.startswith("__"):
                annotations[field] = Optional[type_]
        return annotations

    class Config:
        arbitrary_types_allowed = True
