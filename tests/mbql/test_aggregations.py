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

        aggregation = Mock(id=2, name="My Aggregation", option={"foo": "bar"})
        self.assertEqual(
            [
                "aggregation-options",
                ["mock", ["field", 2, {"foo": "bar"}]],
                {"name": "My Aggregation", "display-name": "My Aggregation"},
            ],
            aggregation.compile(),
        )

    def test_count(self):
        """Ensure Count optionally accepts an id attribute."""
        count = Count()
        self.assertEqual(["count"], count.compile())

        count = Count(id=5)
        self.assertEqual(["count"], count.compile())

        count = Count(id=5, name="My Count")
        self.assertEqual(
            [
                "aggregation-options",
                ["count"],
                {"name": "My Count", "display-name": "My Count"},
            ],
            count.compile(),
        )
