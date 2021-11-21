from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List

from metabase.missing import MISSING
from metabase.resource import (
    CreateResource,
    DeleteResource,
    GetResource,
    ListResource,
    UpdateResource,
)


class User(ListResource, CreateResource, GetResource, UpdateResource, DeleteResource):
    ENDPOINT = "/api/user"

    id: int
    email: str
    first_name: str
    last_name: str
    common_name: str
    locale: str

    is_superuser: bool
    is_active: bool
    is_qbnewb: bool
    ldap_auth: bool
    google_auth: bool

    login_attributes: Dict[str, Any]
    group_ids: List[int]

    last_login: datetime
    date_joined: datetime
    updated_at: datetime

    @classmethod
    def list(cls) -> List[User]:
        response = cls.connection().get(cls.ENDPOINT)
        records = [cls(**user) for user in response.json().get("data", [])]
        return records

    @classmethod
    def create(
        cls,
        first_name: str,
        last_name: str,
        email: str,
        password: str,
        group_ids: List[int] = None,
        login_attributes: Dict[str, Any] = None,
        **kwargs,
    ) -> User:
        return super(User, cls).create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            group_ids=group_ids,
            login_attributes=login_attributes,
            **kwargs,
        )

    def update(
        self,
        first_name: str = MISSING,
        last_name: str = MISSING,
        email: str = MISSING,
        password: str = MISSING,
        group_ids: List[int] = MISSING,
        is_superuser: bool = MISSING,
        locale: str = MISSING,
        **kwargs,
    ) -> None:
        return super(User, self).update(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            group_ids=group_ids,
            locale=locale,
            **kwargs,
        )

    def send_invite(self):
        self.connection().put(
            self.ENDPOINT + f"/{getattr(self, self.PRIMARY_KEY)}" + "/send_invite"
        )

    def reactivate(self):
        self.connection().put(
            self.ENDPOINT + f"/{getattr(self, self.PRIMARY_KEY)}" + "/reactivate"
        )
