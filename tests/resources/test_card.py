from metabase import Card
from tests.helpers import IntegrationTestCase


class CardTests(IntegrationTestCase):
    def setUp(self) -> None:
        super(CardTests, self).setUp()

    def test_import(self):
        """Ensure Card can be imported from Metabase."""
        from metabase import Card

        self.assertIsNotNone(Card())

    def test_list(self):
        """Ensure Card.list() returns a list of Card instances."""
        cards = Card.list()

        self.assertIsInstance(cards, list)
        self.assertTrue(len(cards) > 0)
        self.assertTrue(all(isinstance(t, Card) for t in cards))

    def test_get(self):
        """Ensure Card.get() returns a Card instance for a given ID."""
        card = Card.get(1)

        self.assertIsInstance(card, Card)
        self.assertEqual(1, card.id)

    def test_create(self):
        """Ensure Card.create() creates a Card in Metabase and returns a Card instance."""
        card = Card.create(
            name="My Card",
            dataset_query={
                "type": "query",
                "query": {
                    "source-table": 2,
                    "aggregation": [["count"]],
                    "breakout": [["field", 12, {"temporal-unit": "month"}]],
                },
                "database": 1,
            },
            visualization_settings={
                "graph.dimensions": ["CREATED_AT"],
                "graph.metrics": ["count"],
            },
            display="line",
        )

        self.assertIsInstance(card, Card)
        self.assertEqual("My Card", card.name)
        self.assertEqual("line", card.display)
        self.assertIsInstance(Card.get(card.id), Card)  # instance exists in Metabase

        # teardown
        card.archive()

    def test_update(self):
        """Ensure Card.update() updates an existing Card in Metabase."""
        # fixture
        card = Card.create(
            name="My Card",
            dataset_query={
                "type": "query",
                "query": {
                    "source-table": 2,
                    "aggregation": [["count"]],
                    "breakout": [["field", 12, {"temporal-unit": "month"}]],
                },
                "database": 1,
            },
            visualization_settings={
                "graph.dimensions": ["CREATED_AT"],
                "graph.metrics": ["count"],
            },
            display="line",
        )

        card = Card.get(1)

        name = card.name
        card.update(name="New Name")

        # assert local instance is mutated
        self.assertEqual("New Name", card.name)

        # assert metabase object is mutated
        t = Card.get(card.id)
        self.assertEqual("New Name", t.name)

        # teardown
        t.archive()

    def test_archive(self):
        """Ensure Card.archive() deletes a Card in Metabase."""
        # fixture
        card = Card.create(
            name="My Card",
            dataset_query={
                "type": "query",
                "query": {
                    "source-table": 2,
                    "aggregation": [["count"]],
                    "breakout": [["field", 12, {"temporal-unit": "month"}]],
                },
                "database": 1,
            },
            visualization_settings={
                "graph.dimensions": ["CREATED_AT"],
                "graph.metrics": ["count"],
            },
            display="line",
        )
        self.assertIsInstance(card, Card)

        card.archive()
        self.assertEqual(True, card.archived)

        c = Card.get(card.id)
        self.assertEqual(True, c.archived)