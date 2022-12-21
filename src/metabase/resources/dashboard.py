from __future__ import annotations

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

class Dashboard(CreateResource, DeleteResource, GetResource, ListResource, UpdateResource):
    ENDPOINT = "/api/dashboard"

    id: int
    name: str
    description: str

    parameters: List[dict]
    cache_ttl: int
    collection_id: int
    collection_position: int
    is_app_page: bool

    @classmethod
    def list(cls, using: Metabase) -> List[Dashboard]:
        response = using.get(cls.ENDPOINT)
        records = [cls(_using=using, **dashboard) for dashboard in response.json()]
        return records

    @classmethod
    def get(cls, id: int, using: Metabase) -> Dashboard:
        return super(Dashboard, cls).get(id, using=using)

    @classmethod
    def create(
        cls,
        using: Metabase,
        name: str,
        description: str,
        parameters: Optional[List[dict]] = None,
        cache_ttl: Optional[int] = None,
        collection_id: Optional[int] = None,
        collection_position: Optional[int] = None,
        is_app_page: Optional[bool] = None,
        **kwargs,
    ) -> Dashboard:
        """Add a new Dashboard."""
        return super(Dashboard, cls).create(
            using=using,
            name=name,
            description=description,
            parameters=parameters,
            cache_ttl=cache_ttl,
            collection_id=collection_id,
            collection_position=collection_position,
            is_app_page=is_app_page,
            **kwargs,
        )

    def update(
        self,
        name: str = MISSING,
        description: str = MISSING,
        parameters: Optional[List[dict]] = MISSING,
        cache_ttl: Optional[int] = MISSING,
        collection_id: Optional[int] = MISSING,
        collection_position: Optional[int] = MISSING,
        is_app_page: Optional[bool] = MISSING,
        **kwargs,
    ) -> None:
        """Update a Dashboard."""
        return super(Dashboard, self).update(
            name=name,
            description=description,
            parameters=parameters,
            cache_ttl=cache_ttl,
            collection_id=collection_id,
            collection_position=collection_position,
            is_app_page=is_app_page,
        )

    def delete(self) -> None:
        """Delete a Dashboard."""
        return super(Dashboard, self).delete()

