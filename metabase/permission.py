from dataclasses import dataclass
from typing import List

from metabase.resource import Resource


@dataclass
class PermissionGroup(Resource):
    ENDPOINT = "/api/permissions/group"

    id: int
    name: str
    member_count: int

    @classmethod
    def all(cls) -> List["PermissionGroup"]:
        response = cls.connection().get(cls.ENDPOINT)
        records = [cls.from_dict(record) for record in response.json()]
        return records

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

    def delete(self) -> None:
        self.connection().delete(self.ENDPOINT + f"/{self.id}")


@dataclass
class PermissionMembership(Resource):
    ENDPOINT = "/api/permissions/membership"

    membership_id: int
    user_id: int
    group_id: int

    @classmethod
    def all(cls) -> List["PermissionGroup"]:
        response = cls.connection().get(cls.ENDPOINT)
        all_memberships = [item for sublist in response.json().values() for item in sublist]
        records = [cls.from_dict(record) for record in all_memberships]
        return records

    @classmethod
    def create(cls, group_id: int, user_id: int, **kwargs) -> "PermissionGroup":
        response = cls.connection().post(
            cls.ENDPOINT,
            json={
                "group_id": group_id,
                "user_id": user_id
                **kwargs
            }
        )
        return cls.from_dict(response.json())

    def delete(self) -> None:
        self.connection().delete(self.ENDPOINT + f"/{self.membership_id}")
