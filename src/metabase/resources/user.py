from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List

from metabase import Metabase
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
    def list(
        cls,
        using: Metabase,
        status: str = None,
        query: str = None,
        group_id: int = None,
        include_deactivated: bool = None,
        limit: int = None,
        offset: int = None,
    ) -> List[User]:
        """
        Fetch a list of Users. By default returns every active user but only active users.

        If status is deactivated, include deactivated users only. If status is all, include all users (active and
        inactive). Also supports include_deactivated, which if true, is equivalent to status=all. status and
        included_deactivated requires superuser permissions.

        For users with segmented permissions, return only themselves.

        Takes limit, offset for pagination. Takes query for filtering on first name, last name, email. Also takes
        group_id, which filters on group id.
        """
        response = using.get(
            cls.ENDPOINT,
            params={
                "status": status,
                "query": query,
                "group_id": group_id,
                "include_deactivated": include_deactivated,
                "limit": limit,
                "offset": offset,
            },
        )
        records = [
            cls(_using=using, **user) for user in response.json().get("data", [])
        ]
        return records

    @classmethod
    def create(
        cls,
        using: Metabase,
        first_name: str,
        last_name: str,
        email: str,
        password: str,
        group_ids: List[int] = None,
        login_attributes: Dict[str, Any] = None,
        **kwargs,
    ) -> User:
        """
        Create a new User, return a 400 if the email address is already taken.

        You must be a superuser to do this.
        """
        return super(User, cls).create(
            using=using,
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
        group_ids: List[int] = MISSING,
        is_superuser: bool = MISSING,
        locale: str = MISSING,
        **kwargs,
    ) -> None:
        """Update an existing, active User."""
        return super(User, self).update(
            first_name=first_name,
            last_name=last_name,
            email=email,
            group_ids=group_ids,
            locale=locale,
            **kwargs,
        )

    def delete(self) -> None:
        """
        Disable a User. This does not remove the User from the DB, but instead disables their account.

        You must be a superuser to do this.
        """
        return super(User, self).delete()

    def password(self, password: str, old_password: str):
        """Update a user’s password."""
        return self._using.put(
            self.ENDPOINT + f"/{getattr(self, self.PRIMARY_KEY)}" + "/password",
            json={"password": password, "old_password": old_password},
        )

    def send_invite(self):
        """
        Resend the user invite email for a given user.

        You must be a superuser to do this.
        """
        return self._using.put(
            self.ENDPOINT + f"/{getattr(self, self.PRIMARY_KEY)}" + "/send_invite"
        )

    def reactivate(self):
        """
        Reactivate user at :id.

        You must be a superuser to do this.
        """
        return self._using.put(
            self.ENDPOINT + f"/{getattr(self, self.PRIMARY_KEY)}" + "/reactivate"
        )
