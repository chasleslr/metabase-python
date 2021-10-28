from dataclasses import dataclass
from typing import List

from metabase.resource import ListResource, CreateResource, GetResource, UpdateResource, DeleteResource


@dataclass
class PermissionGroup(ListResource, CreateResource, GetResource, UpdateResource, DeleteResource):
    ENDPOINT = "/api/permissions/group"

    id: int
    name: str
    member_count: int

    @classmethod
    def create(cls, name: str, **kwargs) -> "PermissionGroup":
        response = cls.connection().post(
            cls.ENDPOINT,
            json={
                "name": name,
                **kwargs
            }
        )
        return cls.from_dict(response.json())


@dataclass
class PermissionMembership(ListResource, CreateResource, GetResource, UpdateResource, DeleteResource):
    ENDPOINT = "/api/permissions/membership"
    PRIMARY_KEY = "membership_id"

    membership_id: int
    user_id: int
    group_id: int

    @classmethod
    def list(cls) -> List["PermissionMembership"]:
        response = cls.connection().get(cls.ENDPOINT)
        all_memberships = [item for sublist in response.json().values() for item in sublist]
        records = [cls.from_dict(record) for record in all_memberships]
        return records

    @classmethod
    def create(cls, group_id: int, user_id: int, **kwargs) -> "PermissionMembership":
        response = cls.connection().post(
            cls.ENDPOINT,
            json={
                "group_id": group_id,
                "user_id": user_id,
                **kwargs
            }
        )
        return cls.from_dict(response.json())
