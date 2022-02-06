from __future__ import annotations

from typing import List

from metabase import Metabase
from metabase.missing import MISSING
from metabase.resource import CreateResource, GetResource, ListResource, UpdateResource


class Segment(ListResource, CreateResource, GetResource, UpdateResource):
    ENDPOINT = "/api/segment"

    id: int
    table_id: int
    creator_id: int

    name: str
    description: str
    definition: dict
    points_of_interest: str
    caveats: str

    show_in_getting_started: bool
    archived: bool

    updated_at: str
    created_at: str

    @classmethod
    def list(cls, using: Metabase) -> List[Segment]:
        return super(Segment, cls).list(using=using)

    @classmethod
    def get(cls, id: int, using: Metabase) -> Segment:
        return super(Segment, cls).get(id, using=using)

    @classmethod
    def create(
        cls,
        using: Metabase,
        name: str,
        table_id: int,
        definition: dict,
        description: str = "Created by metabase-python.",
        **kwargs
    ) -> Segment:
        return super(Segment, cls).create(
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
        show_in_getting_started: str = MISSING,
        points_of_interest: str = MISSING,
        caveats: str = MISSING,
        archived: bool = MISSING,
        **kwargs
    ) -> None:
        return super(Segment, self).update(
            revision_message=revision_message,
            name=name,
            description=description,
            definition=definition,
            points_of_interest=points_of_interest,
            caveats=caveats,
            archived=archived,
            show_in_getting_started=show_in_getting_started,
            **kwargs
        )

    def archive(self):
        """Archive a Segment."""
        return self.update(
            archived=True, revision_message="Archived by metabase-python."
        )
