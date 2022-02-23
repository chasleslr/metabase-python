from unittest import TestCase

from metabase.mbql.groupby import BinOption, GroupBy, TemporalOption


class GroupbyTests(TestCase):
    def test_groupby_compile(self):
        """Ensure GroupBy.compile() returns ["field", self.id, self.option]"""
        groupby = GroupBy(id=4)
        self.assertEqual(["field", 4, None], groupby.compile())

        groupby = GroupBy(id=4, option=TemporalOption.DAY)
        self.assertEqual(["field", 4, {"temporal-unit": "day"}], groupby.compile())

        groupby = GroupBy(id=4, option=BinOption.BINS_10)
        self.assertEqual(
            ["field", 4, {"binning": {"strategy": "num-bins", "num-bins": 10}}],
            groupby.compile(),
        )
