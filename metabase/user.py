from dataclasses import dataclass
from typing import List

from metabase.resource import ListResource, CreateResource, GetResource, UpdateResource, DeleteResource


@dataclass
class User(ListResource, CreateResource, GetResource, UpdateResource, DeleteResource):
    ENDPOINT = "/api/user"

    id: int
    first_name: str
    last_name: str
    email: str
    password: str = None
    groups_ids: List[int] = None
    login_attributes: dict = None

    is_superuser: bool = None
    locale: str = None

    @classmethod
    def list(cls) -> List["User"]:
        response = cls.connection().get(cls.ENDPOINT)
        records = [cls.from_dict(db) for db in response.json().get("data", [])]
        return records

    @classmethod
    def create(cls, first_name: str, last_name: str, email: str, **kwargs) -> "User":
        response = cls.connection().post(
            cls.ENDPOINT,
            json={
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                **kwargs
            }
        )
        return cls.from_dict(response.json())

    def send_invite(self):
        self.connection().put(self.ENDPOINT + f"/{self.id}" + "/send_invite")

    def reactivate(self):
        self.connection().put(self.ENDPOINT + f"/{self.id}" + "/reactivate")
