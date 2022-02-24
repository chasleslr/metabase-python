from typing import List

from metabase.mbql.base import Mbql, Option


class Aggregation(Mbql):
    function: str

    def __init__(self, id: int, name: str = None, option: Option = None):
        self.name = name
        super(Aggregation, self).__init__(id=id, option=option)

    def compile(self) -> List:
        compiled = [self.function, super(Aggregation, self).compile()]

        if self.name is not None:
            compiled = self.compile_name(compiled, self.name)

        return compiled

    @staticmethod
    def compile_name(compiled, name: str) -> str:
        return (
            ["aggregation-options"]
            + [compiled]
            + [{"name": name, "display-name": name}]
        )


class Count(Aggregation):
    function = "count"

    def __init__(self, id: int = None, name: str = None, option: Option = None):
        self.id = id
        self.name = name

    def compile(self) -> List:
        compiled = [self.function]

        if self.name is not None:
            compiled = self.compile_name(compiled, self.name)

        return compiled


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
