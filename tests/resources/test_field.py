from metabase.resources.field import Field
from tests.helpers import IntegrationTestCase


class FieldTests(IntegrationTestCase):
    def setUp(self) -> None:
        super(FieldTests, self).setUp()

    def test_import(self):
        """Ensure Field can be imported from Metabase."""
        from metabase import Field

        self.assertIsNotNone(Field(_using=None))

    def test_get(self):
        """Ensure Field.get() returns a Field instance for a given ID."""
        field = Field.get(1, using=self.metabase)

        self.assertIsInstance(field, Field)
        self.assertEqual(1, field.id)

    def test_update(self):
        """Ensure Field.update() updates an existing Field in Metabase."""
        field = Field.get(1, using=self.metabase)

        display_name = field.display_name
        semantic_type = field.semantic_type
        field.update(display_name="New Name", semantic_type=Field.SemanticType.zip_code)

        # assert local instance is mutated
        self.assertEqual("New Name", field.display_name)
        self.assertEqual(Field.SemanticType.zip_code, field.semantic_type)

        # assert metabase object is mutated
        f = Field.get(field.id, using=self.metabase)
        self.assertEqual("New Name", f.display_name)
        self.assertEqual(Field.SemanticType.zip_code, f.semantic_type)

        # teardown
        f.update(display_name=display_name, semantic_type=semantic_type)

    def test_related(self):
        """Ensure Field.related() returns a dict."""
        field = Field.get(1, using=self.metabase)
        related = field.related()

        self.assertIsInstance(related, dict)

    def test_discard_values(self):
        # TODO
        pass

    def test_rescan_values(self):
        # TODO
        pass
