from random import randint

from exceptions import NotFoundError

from metabase.resources.user import User
from tests.helpers import IntegrationTestCase


class UserTests(IntegrationTestCase):
    def tearDown(self) -> None:
        users = User.list()
        for user in users:
            if user.id != 1:
                user.delete()

    def test_import(self):
        """Ensure User can be imported from Metabase."""
        from metabase import User

        self.assertIsNotNone(User())

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
        )
        self.assertIsInstance(user, User)

        u = User.get(user.id)
        self.assertIsInstance(u, User)
        self.assertEqual(user.id, u.id)

        with self.assertRaises(NotFoundError):
            _ = User.get(12345)

    def test_create(self):
        """Ensure User.create() creates a User in Metabase and returns a User instance."""
        email = f"{randint(2, 10000)}@example.com"
        user = User.create(
            first_name="Test", last_name="Test", email=email, password="example123"
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
        )

        self.assertIsInstance(user, User)
        self.assertEqual("Test", user.first_name)

        user.update(first_name="Test1")
        # assert local instance is mutated
        self.assertEqual("Test1", user.first_name)

        # assert metabase object is mutated
        u = User.get(user.id)
        self.assertEqual("Test1", u.first_name)

    def test_delete(self):
        """Ensure User.delete() updates archived=True."""
        # fixture
        user = User.create(
            first_name="Test",
            last_name="Test",
            email=f"{randint(2, 10000)}@example.com",
            password="example123",
        )
        self.assertIsInstance(user, User)

        user.delete()

        # assert metabase object is mutated
        with self.assertRaises(NotFoundError):
            _ = User.get(user.id)
