from __future__ import annotations

from typing import List

from requests import HTTPError

from metabase.resource import CreateResource, DeleteResource, ListResource


class PermissionMembership(ListResource, CreateResource, DeleteResource):
    ENDPOINT = "/api/permissions/membership"
    PRIMARY_KEY = "membership_id"

    membership_id: int
    group_id: int
    user_id: int

    # TODO: allow for bulk updates through /api/permissions/membership/graph

    @classmethod
    def list(cls) -> List[PermissionMembership]:
        """
        Fetch a map describing the group memberships of various users. This map’s format is:

        {<user-id> [{:membership_id <id>
                     :group_id      <id>}]}.
        You must be a superuser to do this.
        """
        response = cls.connection().get(cls.ENDPOINT)
        all_memberships = [
            item for sublist in response.json().values() for item in sublist
        ]
        records = [cls(**record) for record in all_memberships]
        return records

    @classmethod
    def create(cls, group_id: int, user_id: int, **kwargs) -> PermissionMembership:
        """
        Add a User to a PermissionsGroup. Returns updated list of members belonging to the group.

        You must be a superuser to do this.
        """
        response = cls.connection().post(
            cls.ENDPOINT, json={"group_id": group_id, "user_id": user_id}
        )

        if response.status_code != 200:
            raise HTTPError(response.content.decode())

        # metabase returns a list of all memberships for the given group_id
        membership = next(filter(lambda x: x["user_id"] == user_id, response.json()))

        return cls(**membership)
