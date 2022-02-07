from __future__ import annotations

from typing import List

from metabase import Metabase
from metabase.resource import (
    CreateResource,
    DeleteResource,
    GetResource,
    ListResource,
    UpdateResource,
)


class PermissionGroup(
    ListResource, CreateResource, GetResource, UpdateResource, DeleteResource
):
    ENDPOINT = "/api/permissions/group"

    id: int
    name: str
    member_count: int

    @classmethod
    def list(cls, using: Metabase) -> List[PermissionGroup]:
        """
        Fetch all PermissionsGroups, including a count of the number of :members in that group.

        You must be a superuser to do this.
        """
        return super(PermissionGroup, cls).list(using=using)

    @classmethod
    def get(cls, id: int, using: Metabase) -> PermissionGroup:
        """
        Fetch the details for a certain permissions group.

        You must be a superuser to do this.
        """
        return super(PermissionGroup, cls).get(id, using=using)

    @classmethod
    def create(cls, using: Metabase, name: str, **kwargs) -> PermissionGroup:
        """
        Create a new PermissionsGroup.

        You must be a superuser to do this.
        """
        return super(PermissionGroup, cls).create(using=using, name=name, **kwargs)

    def update(self, name: str, **kwargs) -> None:
        """
        Update the name of a PermissionsGroup.

        You must be a superuser to do this.
        """
        return super(PermissionGroup, self).update(name=name, **kwargs)

    def delete(self) -> None:
        """
        Delete a specific PermissionsGroup.

        You must be a superuser to do this.
        """
        return super(PermissionGroup, self).delete()
