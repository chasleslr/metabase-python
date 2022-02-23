from typing import List

from metabase.mbql.base import Mbql


class Aggregation(Mbql):
    function: str

    def compile(self) -> List:
        return [self.function, super(Aggregation, self).compile()]


class Count(Aggregation):
    function = "count"

    def __init__(self, id: int = None):
        self.id = id

    def compile(self) -> List:
        return [self.function]


class Sum(Aggregation):
    function = "sum"


class Average(Aggregation):
    function = "avg"


class Distinct(Aggregation):
    function = "distinct"


class CumulativeSum(Aggregation):
    function = "cum-sum"


class CumulativeCount(Aggregation):
    function = "cum-count"


class StandardDeviation(Aggregation):
    function = "stddev"


class Min(Aggregation):
    function = "min"


class Max(Aggregation):
    function = "max"
