from metabase.exceptions import NotFoundError
from metabase.resources.metric import Metric
from tests.helpers import IntegrationTestCase


class MetricTests(IntegrationTestCase):
    def tearDown(self) -> None:
        metrics = Metric.list(using=self.metabase)
        for metric in metrics:
            metric.archive()

    def test_import(self):
        """Ensure Metric can be imported from Metabase."""
        from metabase import Metric

        self.assertIsNotNone(Metric(_using=None))

    def test_list(self):
        """Ensure Metric.list returns a list of Metric instances."""
        # fixture
        _ = Metric.create(
            name="My Metric",
            table_id=1,
            definition={
                "aggregation": [["count"]],
            },
            using=self.metabase,
        )
        _ = Metric.create(
            name="My Metric",
            table_id=1,
            definition={
                "aggregation": [["count"]],
            },
            using=self.metabase,
        )

        metrics = Metric.list(using=self.metabase)

        self.assertIsInstance(metrics, list)
        self.assertEqual(2, len(metrics))
        self.assertTrue(all([isinstance(m, Metric) for m in metrics]))

    def test_get(self):
        """
        Ensure Metric.get returns a Metric instance for a given ID, or
        raises a NotFoundError when it does not exist.
        """
        # fixture
        metric = Metric.create(
            name="My Metric",
            table_id=1,
            definition={
                "aggregation": [["count"]],
            },
            using=self.metabase,
        )
        self.assertIsInstance(metric, Metric)

        m = Metric.get(metric.id, using=self.metabase)
        self.assertIsInstance(m, Metric)
        self.assertEqual(metric.id, m.id)

        with self.assertRaises(NotFoundError):
            _ = Metric.get(12345, using=self.metabase)

    def test_create(self):
        """Ensure Metric.create creates a Metric in Metabase and returns a Metric instance."""
        metric = Metric.create(
            name="My Metric",
            table_id=1,
            definition={
                "aggregation": [["count"]],
            },
            using=self.metabase,
        )

        self.assertIsInstance(metric, Metric)
        self.assertEqual("My Metric", metric.name)
        self.assertEqual(1, metric.table_id)
        self.assertEqual({"aggregation": [["count"]]}, metric.definition)

    def test_update(self):
        """Ensure Metric.update updates an existing Metric in Metabase."""
        # fixture
        metric = Metric.create(
            name="My Metric",
            table_id=1,
            definition={
                "aggregation": [["count"]],
            },
            using=self.metabase,
        )

        self.assertIsInstance(metric, Metric)
        self.assertEqual("My Metric", metric.name)

        metric.update(name="New Name")
        # assert local instance is mutated
        self.assertEqual("New Name", metric.name)

        # assert metabase object is mutated
        m = Metric.get(metric.id, using=self.metabase)
        self.assertEqual("New Name", m.name)

    def test_archive(self):
        """Ensure Metric.archive updates archived=True."""
        # fixture
        metric = Metric.create(
            name="My Metric",
            table_id=1,
            definition={
                "aggregation": [["count"]],
            },
            using=self.metabase,
        )

        self.assertIsInstance(metric, Metric)
        self.assertEqual(False, metric.archived)

        metric.archive()
        # assert local instance is mutated
        self.assertEqual(True, metric.archived)

        # assert metabase object is mutated
        m = Metric.get(metric.id, using=self.metabase)
        self.assertEqual(True, m.archived)
