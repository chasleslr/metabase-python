from unittest import TestCase

from metabase.mbql.aggregations import Aggregation, Count


class AggregationTests(TestCase):
    def test_aggregation(self):
        """Ensure Aggregation.compile() returns [self.function, ['field', self.id, self.option']]."""

        class Mock(Aggregation):
            function = "mock"

        aggregation = Mock(id=2)
        self.assertEqual(["mock", ["field", 2, None]], aggregation.compile())

        aggregation = Mock(id=2, option={"foo": "bar"})
        self.assertEqual(["mock", ["field", 2, {"foo": "bar"}]], aggregation.compile())

    def test_count(self):
        """Ensure Count optionally accepts an id attribute."""
        count = Count()
        self.assertEqual(["count"], count.compile())

        count = Count(id=5)
        self.assertEqual(["count"], count.compile())
