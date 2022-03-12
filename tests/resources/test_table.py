from metabase.resources.field import Field
from metabase.resources.metric import Metric
from metabase.resources.segment import Segment
from metabase.resources.table import Dimension, Table
from tests.helpers import IntegrationTestCase


class TableTests(IntegrationTestCase):
    def setUp(self) -> None:
        super(TableTests, self).setUp()

    def test_import(self):
        """Ensure Table can be imported from Metabase."""
        from metabase import Table

        self.assertIsNotNone(Table(_using=None))

    def test_list(self):
        """Ensure Table.list() returns a list of Table instances."""
        tables = Table.list(using=self.metabase)

        self.assertIsInstance(tables, list)
        self.assertTrue(len(tables) > 0)
        self.assertTrue(all(isinstance(t, Table) for t in tables))

    def test_get(self):
        """Ensure Table.get() returns a Table instance for a given ID."""
        table = Table.get(1, using=self.metabase)

        self.assertIsInstance(table, Table)
        self.assertEqual(1, table.id)

    def test_update(self):
        """Ensure Table.update() updates an existing Table in Metabase."""
        table = Table.get(1, using=self.metabase)

        display_name = table.display_name
        table.update(display_name="New Name")

        # assert local instance is mutated
        self.assertEqual("New Name", table.display_name)

        # assert metabase object is mutated
        t = Table.get(table.id, using=self.metabase)
        self.assertEqual("New Name", t.display_name)

        # teardown
        t.update(display_name=display_name)

    def test_foreign_keys(self):
        """Ensure Table.fks() returns a list of foreign keys as dict."""
        table = Table.get(1, using=self.metabase)
        fks = table.fks()

        self.assertIsInstance(fks, list)
        self.assertTrue(len(fks) > 0)
        self.assertTrue(all(isinstance(fk, dict) for fk in fks))

    def test_query_metadata(self):
        """Ensure Table.query_metadata() returns a dict."""
        table = Table.get(1, using=self.metabase)
        query_metadata = table.query_metadata()

        self.assertIsInstance(query_metadata, dict)

    def test_related(self):
        """Ensure Table.related() returns a dict."""
        table = Table.get(1, using=self.metabase)
        related = table.related()

        self.assertIsInstance(related, dict)

    def test_discard_values(self):
        # TODO
        pass

    def test_rescan_values(self):
        # TODO
        pass

    def test_fields(self):
        """Ensure Table.fields() returns a list of Field instances."""
        table = Table.get(1, using=self.metabase)
        fields = table.fields()

        self.assertIsInstance(fields, list)
        self.assertTrue(len(fields) > 0)
        self.assertTrue(all(isinstance(field, Field) for field in fields))

    def test_dimensions(self):
        """Ensure Table.dimensions() returns a list of Dimension instances."""
        table = Table.get(1, using=self.metabase)
        dimensions = table.dimensions()

        self.assertIsInstance(dimensions, list)
        self.assertTrue(len(dimensions) > 0)
        self.assertTrue(all(isinstance(field, Dimension) for field in dimensions))

    def test_metrics(self):
        """Ensure Table.metrics() returns a list of Metric instances."""
        table = Table.get(1, using=self.metabase)
        metrics = table.metrics()

        self.assertIsInstance(metrics, list)
        self.assertEqual(0, len(metrics))

        # fixture
        metric = Metric.create(
            name="Products",
            table_id=1,
            definition={
                "aggregation": [["count"]],
            },
            using=self.metabase,
        )

        metrics = table.metrics()
        self.assertIsInstance(metrics, list)
        self.assertEqual(1, len(metrics))
        self.assertEqual(metric.id, metrics[0].id)

        # teardown
        metric.archive()

    def test_segments(self):
        """Ensure Table.segments() returns a list of Segment instances."""
        table = Table.get(1, using=self.metabase)
        segments = table.segments()

        self.assertIsInstance(segments, list)
        self.assertEqual(0, len(segments))

        # fixture
        segment = Segment.create(
            name="Free",
            table_id=1,
            definition={
                "filter": ["=", ["field", 1, None], 0],
            },
            using=self.metabase,
        )

        segments = table.segments()
        self.assertIsInstance(segments, list)
        self.assertEqual(1, len(segments))
        self.assertEqual(segment.id, segments[0].id)

        # teardown
        segment.archive()
