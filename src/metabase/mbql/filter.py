from typing import Any, List

from metabase.mbql.base import Mbql, Option


class CaseOption(Option):
    CASE_SENSITIVE = {"case-sensitive": True}
    CASE_INSENSITIVE = {"case-sensitive": False}


class TimeGrainOption(Option):
    MINUTE = "minute"
    HOUR = "hour"
    DAY = "day"
    WEEK = "week"
    MONTH = "month"
    QUARTER = "quarter"
    YEAR = "year"


class Filter(Mbql):
    function: str

    def __init__(self, id: int, option: Option = None):
        self.id = id
        self.option = None
        self.filter_option = option

    def compile(self) -> List:
        compiled = [self.function, super(Filter, self).compile()]

        if self.filter_option is not None:
            compiled = compiled + [self.filter_option]

        return compiled


class ValueFilter(Filter):
    def __init__(self, id: int, value: Any, option: Option = None):
        self.id = id
        self.value = value
        self.option = None
        self.filter_option = option

    def compile(self) -> List:
        compiled = [self.function, super(Filter, self).compile(), self.value]

        if self.filter_option is not None:
            compiled = compiled + [self.filter_option]

        return compiled


class Equal(ValueFilter):
    function = "="


class NotEqual(ValueFilter):
    function = "!="


class Greater(ValueFilter):
    function = ">"


class Less(ValueFilter):
    function = "<"


class Between(Filter):
    function = "between"

    def __init__(
        self, id: int, lower_bound: float, upper_bound: float, option: Option = None
    ):
        self.id = id
        self.option = None
        self.filter_option = option
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound

    def compile(self) -> List:
        return super(Between, self).compile() + [self.lower_bound, self.upper_bound]


class GreaterEqual(ValueFilter):
    function = ">="


class LessEqual(ValueFilter):
    function = "<="


class IsNull(Filter):
    function = "is-null"


class IsNotNull(Filter):
    function = "not-null"


class Contains(ValueFilter):
    function = "contains"


class StartsWith(ValueFilter):
    function = "starts-with"


class EndsWith(ValueFilter):
    function = "ends-with"


class TimeInterval(Filter):
    function = "time-interval"

    def __init__(
        self,
        id: int,
        value: Any,
        time_grain: TimeGrainOption,
        include_current: bool = True,
    ):
        self.id = id
        self.value = value
        self.option = None
        self.time_grain = time_grain
        self.include_current = include_current

    def compile(self) -> List:
        compiled = [
            self.function,
            super(Filter, self).compile(),
            self.value,
            self.time_grain,
        ]

        if self.include_current:
            compiled = compiled + [{"include-current": True}]

        return compiled
