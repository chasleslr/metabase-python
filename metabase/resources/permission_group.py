from __future__ import annotations

from typing import List

from metabase.resource import ListResource, CreateResource, GetResource, UpdateResource, DeleteResource


class PermissionGroup(ListResource, CreateResource, GetResource, UpdateResource, DeleteResource):
    ENDPOINT = "/api/permissions/group"

    id: int
    name: str
    member_count: int

    @classmethod
    def list(cls) -> List[PermissionGroup]:
        return super(PermissionGroup, cls).list()

    @classmethod
    def get(cls, id: int) -> PermissionGroup:
        return super(PermissionGroup, cls).get(id)

    @classmethod
    def create(cls, name: str, **kwargs) -> PermissionGroup:
        return super(PermissionGroup, cls).create(name=name, **kwargs)

    def update(self, name: str, **kwargs) -> None:
        return super(PermissionGroup, self).update(name=name, **kwargs)