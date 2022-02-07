from __future__ import annotations

from typing import List

from metabase import Metabase
from metabase.missing import MISSING
from metabase.resource import CreateResource, GetResource, ListResource, UpdateResource


class Card(ListResource, CreateResource, GetResource, UpdateResource):
    ENDPOINT = "/api/card"

    id: int
    table_id: int
    database_id: int
    collection_id: int
    creator_id: int
    made_public_by_id: int
    public_uuid: str

    name: str
    description: str

    collection: dict  # TODO: Collection
    collection_position: int

    query_type: str
    dataset_query: dict  # TODO: DatasetQuery
    display: str
    visualization_settings: dict  # TODO: VisualizationSettings
    result_metadata: List[dict]

    embedding_params: dict
    cache_ttl: str
    creator: "User"

    favorite: bool
    archived: bool
    enable_embedding: bool

    updated_at: str
    created_at: str

    @classmethod
    def list(cls, using: Metabase) -> List[Card]:
        """
        Get all the Cards. Option filter param f can be used to change the set
        of Cards that are returned; default is all, but other options include
        mine, fav, database, table, recent, popular, and archived.

        See corresponding implementation functions above for the specific behavior
        of each filter option. :card_index:.
        """
        # TODO: add support for endpoint parameters: f, model_id.
        return super(Card, cls).list(using)

    @classmethod
    def get(cls, id: int, using: Metabase) -> Card:
        """
        Get Card with ID.
        """
        return super(Card, cls).get(id, using)

    @classmethod
    def create(
        cls,
        using: Metabase,
        name: str,
        dataset_query: dict,  # TODO: DatasetQuery
        visualization_settings: dict,  # TODO: VisualizationSettings
        display: str,
        description: str = None,
        collection_id: str = None,
        collection_position: int = None,
        result_metadata: List[dict] = None,
        metadata_checksum: str = None,
        cache_ttl: int = None,
        **kwargs,
    ) -> Card:
        """
        Create a new Card.
        """
        return super(Card, cls).create(
            using=using,
            name=name,
            dataset_query=dataset_query,
            visualization_settings=visualization_settings,
            display=display,
            description=description,
            collection_id=collection_id,
            collection_position=collection_position,
            result_metadata=result_metadata,
            metadata_checksum=metadata_checksum,
            cache_ttl=cache_ttl,
            **kwargs,
        )

    def update(
        self,
        name: str = MISSING,
        dataset_query: dict = MISSING,  # TODO: DatasetQuery
        visualization_settings: dict = MISSING,  # TODO: VisualizationSettings
        display: str = MISSING,
        description: str = MISSING,
        collection_id: str = MISSING,
        collection_position: int = MISSING,
        result_metadata: List[dict] = MISSING,
        metadata_checksum: str = MISSING,
        archived: bool = MISSING,
        enable_embedding: bool = MISSING,
        embedding_params: dict = MISSING,
        cache_ttl: int = None,
        **kwargs,
    ) -> None:
        """
        Update a Card.
        """
        return super(Card, self).update(
            name=name,
            dataset_query=dataset_query,
            visualization_settings=visualization_settings,
            display=display,
            description=description,
            collection_id=collection_id,
            collection_position=collection_position,
            result_metadata=result_metadata,
            metadata_checksum=metadata_checksum,
            archived=archived,
            enable_embedding=enable_embedding,
            embedding_params=embedding_params,
            cache_ttl=cache_ttl,
        )

    def archive(self):
        """Archive a Card."""
        return self.update(
            archived=True, revision_message="Archived by metabase-python."
        )
