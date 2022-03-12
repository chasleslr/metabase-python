from unittest import TestCase

from metabase.mbql.base import Mbql


class MbqlTests(TestCase):
    def test_compile(self):
        """Ensure Mbql.compile() returns a list formatted as ["field", self.id, self.option]."""
        mbql = Mbql(id=5, option={"foo": "bar"})
        self.assertEqual(["field", 5, {"foo": "bar"}], mbql.compile())

        mbql = Mbql(id=10, option=None)
        self.assertEqual(["field", 10, None], mbql.compile())

    def test_repr(self):
        """Ensure Mbql.__repr__() returns the compiled Mbql as a string."""
        mbql = Mbql(id=5, option={"foo": "bar"})
        self.assertEqual("['field', 5, {'foo': 'bar'}]", mbql.__repr__())

        mbql = Mbql(id=10, option=None)
        self.assertEqual("['field', 10, None]", mbql.__repr__())
