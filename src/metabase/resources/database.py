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
from metabase.resources.field import Field
from metabase.resources.table import Table


class Database(
    ListResource, CreateResource, GetResource, UpdateResource, DeleteResource
):
    ENDPOINT = "/api/database"

    id: int
    name: str
    description: str
    engine: str

    features: List[Any]
    details: Dict[str, str]
    options: str
    native_permissions: str

    timezone: str
    metadata_sync_schedule: str
    cache_field_values_schedule: str
    cache_ttl: int

    caveats: str
    refingerprint: str
    points_of_interest: str

    auto_run_queries: bool
    is_full_sync: bool
    is_on_demand: bool
    is_sample: bool

    updated_at: str
    created_at: str

    @classmethod
    def list(cls, using: Metabase) -> List[Database]:
        response = using.get(cls.ENDPOINT)
        records = [cls(_using=using, **db) for db in response.json().get("data", [])]
        return records

    @classmethod
    def get(cls, id: int, using: Metabase) -> Database:
        return super(Database, cls).get(id, using=using)

    @classmethod
    def create(
        cls,
        using: Metabase,
        name: str,
        engine: str,
        details: dict,
        is_full_sync: bool = None,
        is_on_demand: bool = None,
        schedules: dict = None,
        auto_run_queries: bool = None,
        cache_ttl: int = None,
        **kwargs,
    ) -> Database:
        """
        Add a new Database.

        You must be a superuser to do this.
        """
        return super(Database, cls).create(
            using=using,
            name=name,
            engine=engine,
            details=details,
            is_full_sync=is_full_sync,
            is_on_demand=is_on_demand,
            schedules=schedules,
            auto_run_queries=auto_run_queries,
            cache_ttl=cache_ttl,
            **kwargs,
        )

    def update(
        self,
        name: str = MISSING,
        description: str = MISSING,
        engine: str = MISSING,
        schedules: dict = MISSING,
        refingerprint: bool = MISSING,
        points_of_interest: str = MISSING,
        auto_run_queries: bool = MISSING,
        caveats: str = MISSING,
        is_full_sync: bool = MISSING,
        cache_ttl: int = MISSING,
        details: dict = MISSING,
        is_on_demand: bool = MISSING,
        **kwargs,
    ) -> None:
        """
        Update a Database.

        You must be a superuser to do this.
        """
        return super(Database, self).update(
            name=name,
            description=description,
            engine=engine,
            schedules=schedules,
            refingerprint=refingerprint,
            points_of_interest=points_of_interest,
            auto_run_queries=auto_run_queries,
            caveats=caveats,
            is_full_sync=is_full_sync,
            cache_ttl=cache_ttl,
            details=details,
            is_on_demand=is_on_demand,
        )

    def delete(self) -> None:
        """Delete a Database."""
        return super(Database, self).delete()

    def fields(self) -> List[Field]:
        """Get a list of all Fields in Database."""
        fields = self._using.get(
            self.ENDPOINT + f"/{getattr(self, self.PRIMARY_KEY)}" + "/fields"
        ).json()
        return [Field(_using=self._using, **payload) for payload in fields]

    def idfields(self) -> List[Field]:
        """Get a list of all primary key Fields for Database."""
        fields = self._using.get(
            self.ENDPOINT + f"/{getattr(self, self.PRIMARY_KEY)}" + "/idfields"
        ).json()
        return [Field(_using=self._using, **payload) for payload in fields]

    def schemas(self) -> List[str]:
        """Returns a list of all the schemas found for the database id."""
        return self._using.get(
            self.ENDPOINT + f"/{getattr(self, self.PRIMARY_KEY)}" + "/schemas"
        ).json()

    def tables(self, schema: str) -> List[Table]:
        """Returns a list of Tables for the given Database id and schema."""
        tables = self._using.get(
            self.ENDPOINT
            + f"/{getattr(self, self.PRIMARY_KEY)}"
            + "/schema"
            + f"/{schema}"
        ).json()
        return [Table(_using=self._using, **payload) for payload in tables]

    def discard_values(self):
        """
        Discards all saved field values for this Database.

        You must be a superuser to do this.
        """
        return self._using.post(
            self.ENDPOINT + f"/{getattr(self, self.PRIMARY_KEY)}" + "/discard_values"
        )

    def rescan_values(self):
        """
        Trigger a manual scan of the field values for this Database.

        You must be a superuser to do this.
        """
        return self._using.post(
            self.ENDPOINT + f"/{getattr(self, self.PRIMARY_KEY)}" + "/rescan_values"
        )

    def sync(self):
        """Update the metadata for this Database. This happens asynchronously."""
        return self._using.post(
            self.ENDPOINT + f"/{getattr(self, self.PRIMARY_KEY)}" + "/sync"
        )

    def sync_schema(self):
        """
        Trigger a manual update of the schema metadata for this Database.

        You must be a superuser to do this.
        """
        return self._using.post(
            self.ENDPOINT + f"/{getattr(self, self.PRIMARY_KEY)}" + "/sync_schema"
        )
