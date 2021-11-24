from exceptions import NotFoundError

from metabase import Database
from metabase.resources.field import Field
from metabase.resources.table import Table
from tests.helpers import IntegrationTestCase


class DatabaseTests(IntegrationTestCase):
    def setUp(self) -> None:
        super(DatabaseTests, self).setUp()

    def test_import(self):
        """Ensure Database can be imported from Metabase."""
        from metabase import Database

        self.assertIsNotNone(Database())

    def test_list(self):
        """Ensure Database.list() returns a list of Database instances."""
        databases = Database.list()

        self.assertIsInstance(databases, list)
        self.assertTrue(len(databases) > 0)
        self.assertTrue(all(isinstance(t, Database) for t in databases))

    def test_get(self):
        """Ensure Database.get() returns a Database instance for a given ID."""
        database = Database.get(1)

        self.assertIsInstance(database, Database)
        self.assertEqual(1, database.id)

    def test_create(self):
        """Ensure Database.create() creates a Database in Metabase and returns a Database instance."""
        database = Database.create(
            name="Test",
            engine="h2",
            details={
                "db": "zip:/app/metabase.jar!/sample-dataset.db;USER=GUEST;PASSWORD=guest"
            },
        )

        self.assertIsInstance(database, Database)
        self.assertEqual("Test", database.name)
        self.assertEqual("h2", database.engine)
        self.assertIsInstance(
            Database.get(database.id), Database
        )  # instance exists in Metabase

        # teardown
        database.delete()

    def test_update(self):
        """Ensure Database.update() updates an existing Database in Metabase."""
        database = Database.get(1)

        name = database.name
        database.update(name="New Name")

        # assert local instance is mutated
        self.assertEqual("New Name", database.name)

        # assert metabase object is mutated
        t = Database.get(database.id)
        self.assertEqual("New Name", t.name)

        # teardown
        t.update(name=name)

    def test_delete(self):
        """Ensure Database.delete() deletes a Database in Metabase."""
        # fixture
        database = Database.create(
            name="Test",
            engine="h2",
            details={
                "db": "zip:/app/metabase.jar!/sample-dataset.db;USER=GUEST;PASSWORD=guest"
            },
        )
        self.assertIsInstance(database, Database)

        database.delete()

        # assert metabase object is mutated
        with self.assertRaises(NotFoundError):
            _ = Database.get(database.id)

    def test_fields(self):
        """Ensure Database.fields() returns a list of Field instances."""
        database = Database.get(1)
        fields = database.fields()

        self.assertIsInstance(fields, list)
        self.assertTrue(len(fields) > 0)
        self.assertTrue(all(isinstance(t, Field) for t in fields))

    def test_idfields(self):
        """Ensure Database.idfields() returns a list of Field instances."""
        database = Database.get(1)
        fields = database.idfields()

        self.assertIsInstance(fields, list)
        self.assertTrue(len(fields) > 0)
        self.assertTrue(all(isinstance(t, Field) for t in fields))

    def test_schemas(self):
        """Ensure Database.schemas() returns a list of strings."""
        database = Database.get(1)
        schemas = database.schemas()

        self.assertIsInstance(schemas, list)
        self.assertTrue(len(schemas) > 0)
        self.assertTrue(all(isinstance(t, str) for t in schemas))

    def test_tables(self):
        """Ensure Database.tables() returns a list of Table instances."""
        database = Database.get(1)
        schema = database.schemas()[0]
        tables = database.tables(schema)

        self.assertIsInstance(tables, list)
        self.assertTrue(len(tables) > 0)
        self.assertTrue(all(isinstance(t, Table) for t in tables))

    def test_discard_values(self):
        """Ensure Database.discard_values() does not raise an error."""
        database = Database.get(1)
        response = database.discard_values()

        self.assertEqual(200, response.status_code)

    def test_rescan_values(self):
        """Ensure Database.rescan_values() does not raise an error."""
        database = Database.get(1)
        response = database.rescan_values()

        self.assertEqual(200, response.status_code)

    def test_sync(self):
        """Ensure Database.sync() does not raise an error."""
        database = Database.get(1)
        response = database.sync()

        self.assertEqual(200, response.status_code)

    def test_sync_schema(self):
        """Ensure Database.sync_schema() does not raise an error."""
        database = Database.get(1)
        response = database.sync_schema()

        self.assertEqual(200, response.status_code)
