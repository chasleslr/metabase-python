from unittest import TestCase

import requests

from metabase.metabase import Metabase


class IntegrationTestCase(TestCase):
    HOST = "http://0.0.0.0:3000"
    FIRST_NAME = "test"
    LAST_NAME = "test"
    EMAIL = "test@example.com"
    PASSWORD = "example123"
    SITE_NAME = "metabase-python"

    @classmethod
    def setUpClass(cls) -> None:
        cls.setup_metabase()

    def setUp(self) -> None:
        self.metabase = Metabase(
            host=self.HOST, user=self.EMAIL, password=self.PASSWORD
        )

    @classmethod
    def setup_metabase(cls):
        response = requests.get(cls.HOST + "/api/session/properties")
        token = response.json()["setup-token"]

        if token is not None:
            response = requests.post(
                cls.HOST + "/api/setup",
                json={
                    "prefs": {"site_name": cls.SITE_NAME},
                    "user": {
                        "email": cls.EMAIL,
                        "password": cls.PASSWORD,
                        "first_name": cls.FIRST_NAME,
                        "last_name": cls.LAST_NAME,
                        "site_name": cls.SITE_NAME,
                    },
                    "token": token,
                },
            )
