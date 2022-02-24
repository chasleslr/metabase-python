from metabase.exceptions import NotFoundError
from metabase.resources.segment import Segment
from tests.helpers import IntegrationTestCase


class SegmentTests(IntegrationTestCase):
    def tearDown(self) -> None:
        segments = Segment.list(using=self.metabase)
        for segment in segments:
            segment.archive()

    def test_import(self):
        """Ensure Segment can be imported from Metabase."""
        from metabase import Segment

        self.assertIsNotNone(Segment(_using=None))

    def test_list(self):
        """Ensure Segment.list returns a list of Segment instances."""
        # fixture
        _ = Segment.create(
            name="My Segment",
            table_id=1,
            definition={
                "filter": ["=", ["field", 1, None], 0],
            },
            using=self.metabase,
        )
        _ = Segment.create(
            name="My Segment",
            table_id=1,
            definition={
                "filter": ["=", ["field", 1, None], 0],
            },
            using=self.metabase,
        )

        segments = Segment.list(using=self.metabase)

        self.assertIsInstance(segments, list)
        self.assertEqual(2, len(segments))
        self.assertTrue(all([isinstance(m, Segment) for m in segments]))

    def test_get(self):
        """
        Ensure Segment.get returns a Segment instance for a given ID, or
        raises a NotFoundError when it does not exist.
        """
        # fixture
        segment = Segment.create(
            name="My Segment",
            table_id=1,
            definition={
                "filter": ["=", ["field", 1, None], 0],
            },
            using=self.metabase,
        )
        self.assertIsInstance(segment, Segment)

        m = Segment.get(segment.id, using=self.metabase)
        self.assertIsInstance(m, Segment)
        self.assertEqual(segment.id, m.id)

        with self.assertRaises(NotFoundError):
            _ = Segment.get(12345, using=self.metabase)

    def test_create(self):
        """Ensure Segment.create creates a Segment in Metabase and returns a Segment instance."""
        segment = Segment.create(
            name="My Segment",
            table_id=1,
            definition={
                "filter": ["=", ["field", 1, None], 0],
            },
            using=self.metabase,
        )

        self.assertIsInstance(segment, Segment)
        self.assertEqual("My Segment", segment.name)
        self.assertEqual(1, segment.table_id)
        self.assertEqual({"filter": ["=", ["field", 1, None], 0]}, segment.definition)

    def test_update(self):
        """Ensure Segment.update updates an existing Segment in Metabase."""
        # fixture
        segment = Segment.create(
            name="My Segment",
            table_id=1,
            definition={
                "filter": ["=", ["field", 1, None], 0],
            },
            using=self.metabase,
        )

        self.assertIsInstance(segment, Segment)
        self.assertEqual("My Segment", segment.name)

        segment.update(name="New Name")
        # assert local instance is mutated
        self.assertEqual("New Name", segment.name)

        # assert metabase object is mutated
        m = Segment.get(segment.id, using=self.metabase)
        self.assertEqual("New Name", m.name)

    def test_archive(self):
        """Ensure Segment.archive updates archived=True."""
        # fixture
        segment = Segment.create(
            name="My Segment",
            table_id=1,
            definition={
                "filter": ["=", ["field", 1, None], 0],
            },
            using=self.metabase,
        )

        self.assertIsInstance(segment, Segment)
        self.assertEqual(False, segment.archived)

        segment.archive()
        # assert local instance is mutated
        self.assertEqual(True, segment.archived)

        # assert metabase object is mutated
        m = Segment.get(segment.id, using=self.metabase)
        self.assertEqual(True, m.archived)
