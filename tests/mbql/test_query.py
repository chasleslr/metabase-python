from unittest import TestCase

from metabase import Metric
from metabase.mbql.aggregations import Count, Max
from metabase.mbql.filter import Equal
from metabase.mbql.groupby import GroupBy
from metabase.mbql.query import Query
from metabase.resources.metric import Metric


class QueryTests(TestCase):
    def test_compile(self):
        """Ensure Query.compile() returns valid MBQL."""
        query = Query(
            table_id=14,
            aggregations=[Count(), Max(5)],
            group_by=[GroupBy(14)],
            filters=[Equal(2, 5), Equal(5, "foo")],
        )

        self.assertEqual(
            {
                "source-table": 14,
                "aggregation": [["count"], ["max", ["field", 5, None]]],
                "breakout": [["field", 14, None]],
                "filter": [
                    "and",
                    ["=", ["field", 2, None], 5],
                    ["=", ["field", 5, None], "foo"],
                ],
            },
            query.compile(),
        )

    def test__aggregations(self):
        """Ensure Query._aggregations returns a list of compiled Aggregation."""
        query = Query(table_id=12, aggregations=[])
        self.assertEqual([], query._aggregations)

        query = Query(
            table_id=12,
            aggregations=[Count(), Max(5)],
        )
        self.assertEqual([["count"], ["max", ["field", 5, None]]], query._aggregations)

        query = Query(
            table_id=12,
            aggregations=[Count(), Metric(id=4, _using=None)],
        )
        self.assertEqual([["count"], ["metric", 4]], query._aggregations)

    def test__group_by(self):
        """Ensure Query._group_by returns a list of compiled GroupBy."""
        query = Query(table_id=12, aggregations=[Count()], group_by=[])
        self.assertEqual([], query._group_by)

        query = Query(
            table_id=12,
            aggregations=[Count()],
            group_by=[GroupBy(5)],
        )
        self.assertEqual([["field", 5, None]], query._group_by)

    def test__filters(self):
        """Ensure Query._filters returns a list of compiled Filter."""
        query = Query(table_id=12, aggregations=[Count()], filters=[])
        self.assertEqual([], query._filters)

        query = Query(
            table_id=12,
            aggregations=[Count()],
            filters=[Equal(5, 2)],
        )
        self.assertListEqual(["=", ["field", 5, None], 2], query._filters)

        query = Query(
            table_id=12,
            aggregations=[Count()],
            filters=[Equal(5, 2), Equal(6, 1)],
        )
        self.assertEqual(
            ["and", ["=", ["field", 5, None], 2], ["=", ["field", 6, None], 1]],
            query._filters,
        )
