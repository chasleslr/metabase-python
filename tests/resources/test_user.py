from random import randint

from metabase import PermissionGroup
from metabase.exceptions import NotFoundError
from metabase.resources.user import User
from tests.helpers import IntegrationTestCase


class UserTests(IntegrationTestCase):
    def tearDown(self) -> None:
        users = User.list(using=self.metabase)
        for user in users:
            if user.id != 1:
                user.delete()

        groups = PermissionGroup.list(using=self.metabase)
        for group in groups:
            if group.id > 2:
                group.delete()

    def test_import(self):
        """Ensure User can be imported from Metabase."""
        from metabase import User

        self.assertIsNotNone(User(_using=None))

    def test_list(self):
        """Ensure User.list() returns a list of Users, and supports filter parameters."""
        users = User.list(using=self.metabase)
        self.assertIsInstance(users, list)
        self.assertEqual(1, len(users))

        user1 = User.create(
            first_name="Test",
            last_name="Test",
            email=f"{randint(2, 10000)}@example.com",
            password="example123",
            using=self.metabase,
        )
        group = PermissionGroup.create(using=self.metabase, name="foo")
        user2 = User.create(
            first_name="Test",
            last_name="Test",
            email=f"{randint(2, 10000)}@example.com",
            password="example123",
            group_ids=[1, group.id],
            using=self.metabase,
        )

        users = User.list(using=self.metabase)
        self.assertEqual(3, len(users))

        users = User.list(using=self.metabase, query=user1.email)
        self.assertEqual(1, len(users))
        self.assertEqual(users[0].id, user1.id)

        users = User.list(using=self.metabase, group_id=group.id)
        self.assertEqual(1, len(users))
        self.assertEqual(users[0].id, user2.id)

        user1.delete()
        users = User.list(using=self.metabase, include_deactivated=True)
        self.assertTrue(user1.id in map(lambda u: u.id, users))

        users = User.list(using=self.metabase, limit=1)
        self.assertEqual(1, len(users))

        users = User.list(using=self.metabase, limit=2)
        self.assertEqual(2, len(users))

    def test_get(self):
        """
        Ensure User.get() returns a User instance for a given ID, or
        raises a NotFoundError when it does not exist.
        """
        # fixture
        user = User.create(
            first_name="Test",
            last_name="Test",
            email=f"{randint(2, 10000)}@example.com",
            password="example123",
            using=self.metabase,
        )
        self.assertIsInstance(user, User)

        u = User.get(user.id, using=self.metabase)
        self.assertIsInstance(u, User)
        self.assertEqual(user.id, u.id)

        with self.assertRaises(NotFoundError):
            _ = User.get(12345, using=self.metabase)

    def test_create(self):
        """Ensure User.create() creates a User in Metabase and returns a User instance."""
        email = f"{randint(2, 10000)}@example.com"
        user = User.create(
            first_name="Test",
            last_name="Test",
            email=email,
            password="example123",
            using=self.metabase,
        )

        self.assertIsInstance(user, User)
        self.assertEqual("Test", user.first_name)
        self.assertEqual("Test", user.last_name)
        self.assertEqual(email, user.email)

    def test_update(self):
        """Ensure User.update() updates an existing User in Metabase."""
        # fixture
        user = User.create(
            first_name="Test",
            last_name="Test",
            email=f"{randint(2, 10000)}@example.com",
            password="example123",
            using=self.metabase,
        )

        self.assertIsInstance(user, User)
        self.assertEqual("Test", user.first_name)

        user.update(first_name="Test1")
        # assert local instance is mutated
        self.assertEqual("Test1", user.first_name)

        # assert metabase object is mutated
        u = User.get(user.id, using=self.metabase)
        self.assertEqual("Test1", u.first_name)

    def test_delete(self):
        """Ensure User.delete() updates archived=True."""
        # fixture
        user = User.create(
            first_name="Test",
            last_name="Test",
            email=f"{randint(2, 10000)}@example.com",
            password="example123",
            using=self.metabase,
        )
        self.assertIsInstance(user, User)

        user.delete()

        # assert metabase object is mutated
        with self.assertRaises(NotFoundError):
            _ = User.get(user.id, using=self.metabase)
