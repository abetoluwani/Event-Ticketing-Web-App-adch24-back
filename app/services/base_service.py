#!/usr/bin/env python3
# File: base_service.py
# Author: Oluwatobiloba Light
"""Base Service"""


from uuid import UUID


class BaseService:
    def __init__(self, repository) -> None:
        self._repository = repository

    def get_list(self, schema):
        return self._repository.read_by_options(schema, eager=True)

    def get_by_id(self, id: str):
        return self._repository.read_by_id(UUID(id))

    def add(self, schema):
        return self._repository.create(schema)

    def patch(self, id: UUID, schema):
        return self._repository.update(id, schema)

    def patch_attr(self, id: UUID, attr: str, value):
        return self._repository.update_attr(id, attr, value)

    def put_update(self, id: UUID, schema):
        return self._repository.whole_update(id, schema)

    def remove_by_id(self, id):
        return self._repository.delete_by_id(id)
