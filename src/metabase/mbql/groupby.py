from metabase.mbql.base import Mbql, Option


class TemporalOption(Option):
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


class BinOption(Option):
    AUTO = {"binning": {"strategy": "default"}}
    BINS_10 = {"binning": {"strategy": "num-bins", "num-bins": 10}}
    BINS_50 = {"binning": {"strategy": "num-bins", "num-bins": 50}}
    BINS_100 = {"binning": {"strategy": "num-bins", "num-bins": 100}}
    NONE = None


class GroupBy(Mbql):
    pass
