from exceptions import NotFoundError

from metabase import PermissionGroup, PermissionMembership
from tests.helpers import IntegrationTestCase


class PermissionMembershipTests(IntegrationTestCase):
    def tearDown(self) -> None:
        memberships = PermissionMembership.list()
        for membership in memberships:
            if membership.group_id not in (1, 2):
                # can't delete memberships in the default groups
                membership.delete()

        groups = PermissionGroup.list()
        for group in groups:
            if group.id not in (1, 2):
                # can't delete default groups
                group.delete()

    def test_import(self):
        """Ensure PermissionMembership can be imported from Metabase."""
        from metabase import PermissionMembership

        self.assertIsNotNone(PermissionMembership())

    def test_list(self):
        """Ensure PermissionMembership.list returns a list of PermissionMembership instances."""
        memberships = PermissionMembership.list()
        self.assertIsInstance(memberships, list)
        self.assertTrue(len(memberships) > 0)
        self.assertTrue(all([isinstance(m, PermissionMembership) for m in memberships]))

    def test_create(self):
        """Ensure PermissionMembership.create creates a Metric in Metabase and returns a PermissionMembership instance."""
        group = PermissionGroup.create(name="My Group")
        membership = PermissionMembership.create(group_id=group.id, user_id=1)

        self.assertIsInstance(membership, PermissionMembership)
        self.assertEqual(1, membership.user_id)

    def test_delete(self):
        """Ensure PermissionMembership.delete deletes a PermissionMembership in Metabase."""
        # fixture
        group = PermissionGroup.create(name="My Group")
        membership = PermissionMembership.create(group_id=group.id, user_id=1)
        self.assertIsInstance(membership, PermissionMembership)
        self.assertTrue(
            membership.membership_id
            in [m.membership_id for m in PermissionMembership.list()]
        )

        membership.delete()

        self.assertFalse(
            membership.membership_id
            in [m.membership_id for m in PermissionMembership.list()]
        )
