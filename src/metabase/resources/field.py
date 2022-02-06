from __future__ import annotations

from enum import Enum
from typing import Any, Dict, List, Optional

from metabase import Metabase
from metabase.missing import MISSING
from metabase.resource import GetResource, UpdateResource


class Field(GetResource, UpdateResource):
    ENDPOINT = "/api/field"

    id: int
    table_id: int
    fk_target_id: Optional[int]
    parent_id: Optional[int]

    name: str
    display_name: str
    description: str

    database_type: str
    semantic_type: Field.SemanticType
    effective_type: str
    base_type: str

    dimensions: List[str]
    dimension_options: List[str]
    default_dimension_option: Optional[int]

    database_position: int
    custom_position: int
    visibility_type: str
    points_of_interest: str
    has_field_values: Field.FieldValue

    active: bool
    preview_display: bool

    target: Optional[Field]

    settings: dict
    caveats: str
    coercion_strategy: str

    updated_at: str
    created_at: str

    class FieldValue(str, Enum):
        none = "none"
        auto_list = "auto-list"
        list = "list"
        search = "search"

    class SemanticType(str, Enum):
        primary_key = "Type/PK"
        foreign_key = "Type/FK"

        avatar_url = "type/AvatarURL"
        birthdate = "type/Birthdate"
        cancelation_date = "type/CancelationDate"
        cancelation_time = "type/CancelationTime"
        cancelation_timestamp = "type/CancelationTimestamp"
        category = "type/Category"
        city = "type/City"
        comment = "type/Comment"
        company = "type/Company"
        cost = "type/Cost"
        country = "type/Country"
        creation_date = "type/CreationDate"
        creation_time = "type/CreationTime"
        creation_timestamp = "type/CreationTimestamp"
        currency = "type/Currency"
        deletion_date = "type/DeletionDate"
        deletion_time = "type/DeletionTime"
        deletion_timestamp = "type/DeletionTimestamp"
        description = "type/Description"
        discount = "type/Discount"
        email = "type/Email"
        enum = "type/Enum"
        gross_margin = "type/GrossMargin"
        image_url = "type/ImageURL"
        income = "type/Income"
        join_date = "type/JoinDate"
        join_time = "type/JoinTime"
        join_timestamp = "type/JoinTimestamp"
        latitude = "type/Latitude"
        longitude = "type/Longitude"
        name = "type/Name"
        number = "type/Number"
        owner = "type/Owner"
        price = "type/Price"
        product = "type/Product"
        quantity = "type/Quantity"
        score = "type/Score"
        serialized_json = "type/SerializedJSON"
        share = "type/Share"
        source = "type/Source"
        state = "type/State"
        subscription = "type/Subscription"
        title = "type/Title"
        url = "type/URL"
        user = "type/User"
        zip_code = "type/ZipCode"

    class VisibilityType(str, Enum):
        details_only = "details-only"
        hidden = "hidden"
        normal = "normal"
        retired = "retired"
        sensitive = "sensitive"

    @classmethod
    def get(cls, id: int, using: Metabase) -> Field:
        """Get Field with ID."""
        return super(Field, cls).get(id, using=using)

    def update(
        self,
        display_name: str = MISSING,
        description: str = MISSING,
        semantic_type: Field.SemanticType = MISSING,
        visibility_type: Field.VisibilityType = MISSING,
        fk_target_field_id: int = MISSING,
        has_field_values: Field.FieldValue = MISSING,
        points_of_interest: str = MISSING,
        settings: str = MISSING,
        caveats: str = MISSING,
        coercion_strategy: str = MISSING,
        **kwargs,
    ) -> None:
        """Update Field with ID."""
        return super(Field, self).update(
            display_name=display_name,
            description=description,
            semantic_type=semantic_type,
            visibility_type=visibility_type,
            fk_target_field_id=fk_target_field_id,
            has_field_values=has_field_values,
            points_of_interest=points_of_interest,
            settings=settings,
            caveats=caveats,
            coercion_strategy=coercion_strategy,
        )

    def related(self) -> Dict[str, Any]:
        """Return related entities."""
        return self._using.get(
            self.ENDPOINT + f"/{getattr(self, self.PRIMARY_KEY)}" + "/related"
        ).json()

    def discard_values(self):
        """
        Discard the FieldValues belonging to this Field. Only applies to fields
        that have FieldValues. If this Field’s Database is set up to automatically
        sync FieldValues, they will be recreated during the next cycle.

        You must be a superuser to do this.
        """
        return self._using.post(
            self.ENDPOINT + f"/{getattr(self, self.PRIMARY_KEY)}" + "/discard_values"
        )

    def rescan_values(self):
        """
        Manually trigger an update for the FieldValues for this Field. Only applies
        to Fields that are eligible for FieldValues.

        You must be a superuser to do this.
        """
        return self._using.post(
            self.ENDPOINT + f"/{getattr(self, self.PRIMARY_KEY)}" + "/rescan_values"
        )
