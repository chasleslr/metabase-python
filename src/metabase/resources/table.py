from __future__ import annotations

from enum import Enum
from typing import Any, Dict, List

from metabase import Metabase
from metabase.missing import MISSING
from metabase.resource import GetResource, ListResource, Resource, UpdateResource
from metabase.resources.field import Field
from metabase.resources.metric import Metric
from metabase.resources.segment import Segment


class Dimension(Resource):
    ENDPOINT = None

    id: str
    name: str
    mbql: List[Any]
    type: str


class Table(ListResource, GetResource, UpdateResource):
    ENDPOINT = "/api/table"

    id: int
    name: str
    schema: str
    db_id: int
    db: dict

    display_name: str
    description: str

    entity_name: str
    entity_type: str

    pk_field: int
    visibility_type: Table.VisibilityType
    field_order: Table.FieldOrder
    points_of_interest: str

    active: bool
    show_in_getting_started: bool

    created_at: str
    updated_at: str

    _metrics = None
    _fields = None

    class VisibilityType(str, Enum):
        cruft = "cruft"
        hidden = "hidden"
        technical = "technical"

    class FieldOrder(str, Enum):
        alphabetical = "alphabetical"
        custom = "custom"
        database = "database"
        smart = "smart"

    @classmethod
    def list(cls, using: Metabase) -> List[Table]:
        """Get all Tables."""
        return super(Table, cls).list(using=using)

    @classmethod
    def get(cls, id: int, using: Metabase) -> Table:
        """Get Table with ID."""
        return super(Table, cls).get(id, using=using)

    def update(
        self,
        display_name: str = MISSING,
        description: str = MISSING,
        field_order: Table.FieldOrder = MISSING,
        visibility_type: Table.VisibilityType = MISSING,
        entity_type: str = MISSING,
        points_of_interest: str = MISSING,
        caveats: str = MISSING,
        show_in_getting_started: bool = MISSING,
        **kwargs,
    ) -> None:
        """Update Table with ID."""
        return super(Table, self).update(
            display_name=display_name,
            description=description,
            field_order=field_order,
            visibility_type=visibility_type,
            entity_type=entity_type,
            points_of_interest=points_of_interest,
            caveats=caveats,
            show_in_getting_started=show_in_getting_started,
        )

    def fks(self) -> List[dict]:
        """Get all foreign keys whose destination is a Field that belongs to this Table."""
        return self._using.get(
            self.ENDPOINT + f"/{getattr(self, self.PRIMARY_KEY)}" + "/fks"
        ).json()

    def query_metadata(self) -> Dict[str, Any]:
        """
        Get metadata about a Table useful for running queries. Returns DB, fields,
        field FKs, and field values.

        Passing include_hidden_fields=true will include any hidden Fields in the response.
        Defaults to false Passing include_sensitive_fields=true will include any sensitive
        Fields in the response. Defaults to false.

        These options are provided for use in the Admin Edit Metadata page.
        """
        return self._using.get(
            self.ENDPOINT + f"/{getattr(self, self.PRIMARY_KEY)}" + "/query_metadata"
        ).json()

    def related(self) -> Dict[str, Any]:
        """Return related entities."""
        return self._using.get(
            self.ENDPOINT + f"/{getattr(self, self.PRIMARY_KEY)}" + "/related"
        ).json()

    def discard_values(self):
        """
        Discard the FieldValues belonging to the Fields in this Table. Only applies to
        fields that have FieldValues. If this Table’s Database is set up to automatically
        sync FieldValues, they will be recreated during the next cycle.

        You must be a superuser to do this.
        """
        self._using.post(
            self.ENDPOINT + f"/{getattr(self, self.PRIMARY_KEY)}" + "/discard_values"
        )

    def rescan_values(self):
        """
        Manually trigger an update for the FieldValues for the Fields belonging to this Table.
        Only applies to Fields that are eligible for FieldValues.

        You must be a superuser to do this.
        """
        self._using.post(
            self.ENDPOINT + f"/{getattr(self, self.PRIMARY_KEY)}" + "/rescan_values"
        )

    def fields(self) -> List[Field]:
        """Get all Fields associated with this Table.."""
        return [
            Field(_using=self._using, **field)
            for field in self.query_metadata().get("fields")
        ]

    def dimensions(self) -> List[Dimension]:
        """Get all Dimensions associated with this Table."""
        return [
            Dimension(id=id, _using=self._using, **dimension)
            for id, dimension in self.query_metadata()
            .get("dimension_options", {})
            .items()
        ]

    def metrics(self) -> List[Metric]:
        """Get all Metrics associated with this Table."""
        return [
            Metric(_using=self._using, **metric)
            for metric in self.related().get("metrics")
        ]

    def segments(self) -> List[Segment]:
        """Get all Segments associated with this Table."""
        return [
            Segment(_using=self._using, **segment)
            for segment in self.related().get("segments")
        ]
