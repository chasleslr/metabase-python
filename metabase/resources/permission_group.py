from __future__ import annotations

from typing import List

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
    def list(cls) -> List[PermissionGroup]:
        """
        Fetch all PermissionsGroups, including a count of the number of :members in that group.

        You must be a superuser to do this.
        """
        return super(PermissionGroup, cls).list()

    @classmethod
    def get(cls, id: int) -> PermissionGroup:
        """
        Fetch the details for a certain permissions group.

        You must be a superuser to do this.
        """
        return super(PermissionGroup, cls).get(id)

    @classmethod
    def create(cls, name: str, **kwargs) -> PermissionGroup:
        """
        Create a new PermissionsGroup.

        You must be a superuser to do this.
        """
        return super(PermissionGroup, cls).create(name=name, **kwargs)

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
