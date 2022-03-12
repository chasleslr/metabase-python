from unittest import TestCase

from metabase.exceptions import AuthenticationError
from metabase.metabase import Metabase
from tests.helpers import IntegrationTestCase


class MetabaseTests(TestCase):
    def test_host(self):
        """Ensure Metabase.host adds https:// and trims trailing /."""
        metabase = Metabase(host="example.com/", user="", password="")
        self.assertEqual(metabase.host, "https://example.com")

        del metabase

        metabase = Metabase(host="http://example.com/", user="", password="")
        self.assertEqual(metabase.host, "http://example.com")

    def test_token(self):
        """Ensure Metabase.token returns Metabase._token if not None, else gets a new token."""
        metabase = Metabase(host="example.com", user="", password="", token="123")
        self.assertEqual(metabase.token, "123")

        # TODO: add test case when token is None

    def test_token_invalid_auth(self):
        """Ensure Metabase.token raises AuthenticationException is the user or password is invalid."""
        metabase = Metabase(host="http://0.0.0.0:3000", user="", password="")

        with self.assertRaises(AuthenticationError):
            _ = metabase.token

    def test_headers(self):
        """Ensure Metabase.headers returns a dictionary with the token."""
        metabase = Metabase(host="example.com", user="", password="", token="123")
        self.assertDictEqual(metabase.headers, {"X-Metabase-Session": "123"})

    def test_get(self):
        # TODO
        pass

    def test_post(self):
        # TODO
        pass

    def test_put(self):
        # TODO
        pass

    def test_delete(self):
        # TODO
        pass


class MetabaseIntegrationTests(IntegrationTestCase):
    def test_can_connect(self):
        """Ensure Metabase test instance is setup and can be connected to."""
        response = self.metabase.get("/api/user/current")
        self.assertEqual(200, response.status_code)
        self.assertEqual(self.EMAIL, response.json().get("email"))
