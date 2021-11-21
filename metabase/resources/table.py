from __future__ import annotations

from enum import Enum
from typing import Any, Dict, List

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
    def list(cls) -> List[Table]:
        return super(Table, cls).list()

    @classmethod
    def get(cls, id: int) -> Table:
        return super(Table, cls).get(id)

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

    def foreign_keys(self) -> List[dict]:
        return (
            self.connection()
            .get(self.ENDPOINT + f"/{getattr(self, self.PRIMARY_KEY)}" + "/fks")
            .json()
        )

    def query_metadata(self) -> Dict[str, Any]:
        return (
            self.connection()
            .get(
                self.ENDPOINT
                + f"/{getattr(self, self.PRIMARY_KEY)}"
                + "/query_metadata"
            )
            .json()
        )

    def related(self) -> Dict[str, Any]:
        return (
            self.connection()
            .get(self.ENDPOINT + f"/{getattr(self, self.PRIMARY_KEY)}" + "/related")
            .json()
        )

    def discard_values(self):
        self.connection().post(
            self.ENDPOINT + f"/{getattr(self, self.PRIMARY_KEY)}" + "/discard_values"
        )

    def rescan_values(self):
        self.connection().post(
            self.ENDPOINT + f"/{getattr(self, self.PRIMARY_KEY)}" + "/rescan_values"
        )

    def fields(self) -> List[Field]:
        return [Field(**field) for field in self.query_metadata().get("fields")]

    def dimensions(self) -> List[Dimension]:
        return [
            Dimension(id=id, **dimension)
            for id, dimension in self.query_metadata()
            .get("dimension_options", {})
            .items()
        ]

    def metrics(self) -> List[Metric]:
        return [Metric(**metric) for metric in self.related().get("metrics")]

    def segments(self) -> List[Segment]:
        return [Segment(**segment) for segment in self.related().get("segments")]

    def get_field(self, id: int) -> Field:
        return next(filter(lambda field: field.id == id, self.fields()))

    def get_dimension(self, id: str) -> Dimension:
        return next(filter(lambda dimension: dimension.id == id, self.dimensions()))

    def get_metric(self, id: int) -> Metric:
        return next(filter(lambda metric: metric.id == id, self.metrics()))

    def get_segment(self, id: int) -> Segment:
        return next(filter(lambda segment: segment.id == id, self.segments()))
