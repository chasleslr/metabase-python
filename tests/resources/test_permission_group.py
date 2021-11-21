from exceptions import NotFoundError

from metabase import PermissionGroup, PermissionMembership
from tests.helpers import IntegrationTestCase


class PermissionMembershipTests(IntegrationTestCase):
    def tearDown(self) -> None:
        groups = PermissionGroup.list()
        for group in groups:
            if group.id not in (1, 2):
                # can't delete default groups
                group.delete()

    def test_import(self):
        """Ensure PermissionGroup can be imported from Metabase."""
        from metabase import PermissionGroup

        self.assertIsNotNone(PermissionGroup())

    def test_list(self):
        """Ensure PermissionGroup.list returns a list of PermissionGroup instances."""
        groups = PermissionGroup.list()

        self.assertIsInstance(groups, list)
        self.assertEqual(2, len(groups))  # there are 2 default groups in Metabase
        self.assertTrue(all([isinstance(g, PermissionGroup) for g in groups]))

    def test_get(self):
        """
        Ensure PermissionGroup.get returns a PermissionGroup instance for a given ID, or
        raises a NotFoundError when it does not exist.
        """
        # fixture
        group = PermissionGroup.create(name="My Group")
        self.assertIsInstance(group, PermissionGroup)

        g = PermissionGroup.get(group.id)
        self.assertIsInstance(g, PermissionGroup)
        self.assertEqual(group.id, g.id)

        with self.assertRaises(NotFoundError):
            _ = PermissionGroup.get(12345)

    def test_create(self):
        """Ensure PermissionGroup.create creates a Metric in Metabase and returns a PermissionGroup instance."""
        group = PermissionGroup.create(
            name="My Group",
        )

        self.assertIsInstance(group, PermissionGroup)
        self.assertEqual("My Group", group.name)

    def test_update(self):
        """Ensure PermissionGroup.update updates an existing PermissionGroup in Metabase."""
        # fixture
        group = PermissionGroup.create(
            name="My Group",
        )

        self.assertIsInstance(group, PermissionGroup)
        self.assertEqual("My Group", group.name)

        group.update(name="New Name")
        # assert local instance is mutated
        self.assertEqual("New Name", group.name)

        # assert metabase object is mutated
        m = PermissionGroup.get(group.id)
        self.assertEqual("New Name", m.name)

    def test_delete(self):
        """Ensure PermissionGroup.delete deletes a PermissionGroup in Metabase."""
        # fixture
        group = PermissionGroup.create(
            name="My Metric",
        )

        self.assertIsInstance(group, PermissionGroup)

        group.delete()

        # assert metabase object is mutated
        with self.assertRaises(NotFoundError):
            _ = PermissionGroup.get(group.id)
