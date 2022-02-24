from __future__ import annotations

from datetime import datetime
from typing import List

from metabase.metabase import Metabase
from metabase.missing import MISSING
from metabase.resource import CreateResource, GetResource, ListResource, UpdateResource


class Metric(ListResource, CreateResource, GetResource, UpdateResource):
    ENDPOINT = "/api/metric"

    id: int
    database_id: int
    table_id: int
    creator_id: dict

    name: str
    description: str
    definition: dict
    how_is_this_calculated: str
    points_of_interest: str
    caveats: str

    archived: bool
    show_in_getting_started: bool

    created_at: datetime
    updated_at: datetime

    creator: dict

    @classmethod
    def list(cls, using: Metabase) -> List[Metric]:
        return super(Metric, cls).list(using=using)

    @classmethod
    def get(cls, id: int, using: Metabase) -> Metric:
        return super(Metric, cls).get(id, using=using)

    @classmethod
    def create(
        cls,
        using: Metabase,
        name: str,
        table_id: int,
        definition: dict,
        description: str = "Created by metabase-python.",
        **kwargs
    ) -> Metric:
        return super(Metric, cls).create(
            using=using,
            name=name,
            table_id=table_id,
            definition=definition,
            description=description,
            **kwargs
        )

    def update(
        self,
        revision_message: str = "Updated by metabase-python.",
        name: str = MISSING,
        description: str = MISSING,
        definition: dict = MISSING,
        how_is_this_calculated: str = MISSING,
        points_of_interest: str = MISSING,
        caveats: str = MISSING,
        archived: bool = MISSING,
        show_in_getting_started: bool = MISSING,
        **kwargs
    ) -> None:
        return super(Metric, self).update(
            revision_message=revision_message,
            name=name,
            description=description,
            definition=definition,
            how_is_this_calculated=how_is_this_calculated,
            points_of_interest=points_of_interest,
            caveats=caveats,
            archived=archived,
            show_in_getting_started=show_in_getting_started,
            **kwargs
        )

    def archive(self):
        """Archive a Metric."""
        return self.update(
            archived=True, revision_message="Archived by metabase-python."
        )
