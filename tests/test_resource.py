from unittest.mock import patch

from requests import HTTPError

from metabase.exceptions import NotFoundError
from metabase.metabase import Metabase
from metabase.missing import MISSING
from metabase.resource import (
    CreateResource,
    DeleteResource,
    GetResource,
    ListResource,
    Resource,
    UpdateResource,
)
from tests.helpers import IntegrationTestCase


class ResourceTests(IntegrationTestCase):
    def test_resource_initializes_all_attributes(self):
        """Ensure Resource accepts arbitrary attributes when initializing an instance."""
        resource = Resource(a="a", b="b", _using=None)

        self.assertEqual("a", resource.a)
        self.assertEqual("b", resource.b)
        self.assertListEqual(["a", "b"], resource._attributes)

        # default class attributes
        self.assertEqual(None, getattr(resource, "ENDPOINT", None))
        self.assertEqual("id", resource.PRIMARY_KEY)

    def test_repr(self):
        """Ensure Resource repr prints all class attributes with the PRIMARY_KEY first, if any."""
        resource = Resource(a="a", b="b", id=1, _using=None)
        self.assertEqual("Resource(id=1, a=a, b=b)", resource.__repr__())

        resource.PRIMARY_KEY = None
        self.assertEqual("Resource(a=a, b=b, id=1)", resource.__repr__())


class ListResourceTests(IntegrationTestCase):
    def test_list(self):
        """Ensure ListResource.list() returns a list of objects from Metabase, if any."""

        class Setting(ListResource):
            ENDPOINT = "/api/setting"
            PRIMARY_KEY = None

        settings = Setting.list(using=self.metabase)
        self.assertIsInstance(settings, list)
        self.assertTrue(all([isinstance(s, Setting) for s in settings]))


class GetResourceTests(IntegrationTestCase):
    def test_get(self):
        """Ensure GetResource.get() returns an instance of an object, by ID, if any."""

        class User(GetResource):
            ENDPOINT = "/api/user"

        user = User.get(1, using=self.metabase)
        self.assertIsInstance(user, User)

    def test_get_404(self):
        """Ensure GetResource.get() raises NotFoundError if the object does not exist."""

        class User(GetResource):
            ENDPOINT = "/api/user"

        with self.assertRaises(NotFoundError):
            user = User.get(1234, using=self.metabase)


class CreateResourceTests(IntegrationTestCase):
    def test_create(self):
        """Ensure CreateResource.create() creates an object in Metabase and returns an instance."""

        class Collection(CreateResource, GetResource):
            ENDPOINT = "/api/collection"

        collection = Collection.create(
            name="My Collection", color="#123456", using=self.metabase
        )
        self.assertIsInstance(collection, Collection)
        self.assertIsNotNone(
            Collection.get(collection.id, using=self.metabase)
        )  # metabase was updated


class UpdateResourceTests(IntegrationTestCase):
    def test_update(self):
        """Ensure UpdateResource.update() updates an existing object in Metabase."""

        class Collection(CreateResource, GetResource, UpdateResource):
            ENDPOINT = "/api/collection"

        # fixture
        collection = Collection.create(
            name="My Collection", color="#123456", using=self.metabase
        )
        self.assertIsInstance(collection, Collection)
        self.assertIsNotNone(Collection.get(collection.id, using=self.metabase))

        collection.update(name="My New Collection")
        self.assertEqual("My New Collection", collection.name)

        # metabase was updated
        self.assertEqual(
            "My New Collection", Collection.get(collection.id, using=self.metabase).name
        )

    def test_update_missing(self):
        """Ensure UpdateResource.update() ignores arguments equal to MISSING."""

        class Collection(UpdateResource):
            ENDPOINT = "/api/collection"

        test_matrix = [
            ({"a": "A", "b": "B"}, {"a": "A", "b": "B"}),
            ({"a": "A", "b": MISSING}, {"a": "A"}),
            ({"a": MISSING, "b": MISSING}, {}),
        ]

        for kwargs, expected in test_matrix:
            with patch("metabase.resource.Metabase.put") as mock:
                try:
                    Collection(id=1, _using=self.metabase).update(**kwargs)
                except HTTPError:
                    pass

                self.assertTrue(mock.called)
                self.assertIsNone(
                    mock.assert_called_with("/api/collection/1", json=expected)
                )


class DeleteResourceTests(IntegrationTestCase):
    def test_delete(self):
        """Ensure DeleteResource.delete() deletes an existing object in Metabase."""

        class Group(CreateResource, GetResource, DeleteResource):
            ENDPOINT = "/api/permissions/group"
            PRIMARY_KEY = "id"

        group = Group.create(name="My Group 4", using=self.metabase)

        self.assertIsNotNone(group)
        self.assertIsNotNone(Group.get(group.id, using=self.metabase))

        group.delete()

        with self.assertRaises(NotFoundError):
            Group.get(group.id, using=self.metabase)
