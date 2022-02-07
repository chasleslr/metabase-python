from enum import Enum

from metabase.mbql.base import Field


class TemporalOption(Enum):
    MINUTE = {"temporal-unit": "minute"}
    HOUR = {"temporal-unit": "hour"}
    DAY = {"temporal-unit": "day"}
    WEEK = {"temporal-unit": "week"}
    MONTH = {"temporal-unit": "month"}
    QUARTER = {"temporal-unit": "quarter"}
    YEAR = {"temporal-unit": "year"}
    MINUTE_OF_HOUR = {"temporal-unit": "minute-of-hour"}
    HOUR_OF_DAY = {"temporal-unit": "hour-of-day"}
    DAY_OF_WEEK = {"temporal-unit": "day-of-week"}
    DAY_OF_MONTH = {"temporal-unit": "day-of-month"}
    DAY_OF_YEAR = {"temporal-unit": "day-of-year"}
    WEEK_OF_YEAR = {"temporal-unit": "week-of-year"}
    MONTH_OF_YEAR = {"temporal-unit": "month-of-year"}
    QUARTER_OF_YEAR = {"temporal-unit": "quarter-of-year"}


class BinOption(Enum):
    AUTO = {"binning": {"strategy": "default"}}
    BINS_10 = {"binning": {"strategy": "num-bins", "num-bins": 10}}
    BINS_50 = {"binning": {"strategy": "num-bins", "num-bins": 50}}
    BINS_100 = {"binning": {"strategy": "num-bins", "num-bins": 100}}
    NONE = None


class GroupBy(Field):
    def __init__(self, field_id: int, option=None):
        super(GroupBy, self).__init__(id=field_id, option=option)


class TemporalGroupBy(GroupBy):
    def __init__(self, field_id: int, option: TemporalOption):
        super(TemporalGroupBy, self).__init__(field_id=field_id, option=option.value)


class BinnedGroupBy(GroupBy):
    def __init__(self, field_id: int, option: BinOption):
        super(BinnedGroupBy, self).__init__(field_id=field_id, option=option.value)
