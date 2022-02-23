from unittest import TestCase

from metabase.mbql.filter import (
    Between,
    CaseOption,
    TimeGrainOption,
    TimeInterval,
    ValueFilter,
)


class FilterTests(TestCase):
    def test_value_filter_compile(self):
        """
        Ensure ValueFilter.compile() returns
        [self.function, ['field', self.id, None], self.value, self.filter_option].
        """

        class Mock(ValueFilter):
            function = "mock"

        filter = Mock(id=5, value="gmail", option=CaseOption.CASE_SENSITIVE)
        self.assertEqual(
            ["mock", ["field", 5, None], "gmail", {"case-sensitive": True}],
            filter.compile(),
        )

    def test_between_compile(self):
        """
        Ensure Between.compile() returns
        ['between', ['field', self.id', None], self.lower_bound, self.upper_bound].
        """
        between = Between(id=2, lower_bound=2.5, upper_bound=6.7)
        self.assertEqual(["between", ["field", 2, None], 2.5, 6.7], between.compile())

    def test_time_interval(self):
        interval = TimeInterval(id=4, value=30, time_grain=TimeGrainOption.YEAR)
        self.assertEqual(
            [
                "time-interval",
                ["field", 4, None],
                30,
                "year",
                {"include-current": True},
            ],
            interval.compile(),
        )

        interval = TimeInterval(
            id=4, value=30, time_grain=TimeGrainOption.YEAR, include_current=False
        )
        self.assertEqual(
            ["time-interval", ["field", 4, None], 30, "year"], interval.compile()
        )
