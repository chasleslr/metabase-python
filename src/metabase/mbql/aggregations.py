from metabase.mbql.base import Mbql


class Aggregation(Mbql):
    mbql: str

    def compile(self):
        return [self.mbql]


class ColumnAggregation(Aggregation):
    def __init__(self, field_id: int):
        self.field_id = field_id

    def compile(self):
        return [self.mbql, ["field", self.field_id, None]]


class Count(Aggregation):
    mbql = "count"


class Sum(ColumnAggregation):
    mbql = "sum"


class Max(ColumnAggregation):
    mbql = "max"


class Min(ColumnAggregation):
    mbql = "min"
