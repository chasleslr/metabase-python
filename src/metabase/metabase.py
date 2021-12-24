from weakref import WeakValueDictionary

import requests

from metabase.exceptions import AuthenticationError


class Connection:
    instances = WeakValueDictionary()

    def __init__(self, name, host: str, user: str, password: str, token: str = None):
        self.name = name
        self._host = host
        self.user = user
        self.password = password
        self._token = token

        # register instance
        Connection.instances[name] = self

    @property
    def headers(self) -> dict:
        """Returns headers to include with requests sent to Metabase API."""
        return {"X-Metabase-Session": self.token}

    @property
    def token(self) -> str:
        """Returns a token used to authenticate with Metabase API."""
        if self._token is None:
            self._token = self.get_token(self.user, self.password)

        return self._token

    @property
    def host(self) -> str:
        """Return a sanitized host."""
        host = self._host

        # defaults to https if hot does not include scheme
        if not host.startswith("http"):
            host = "https://" + self._host

        return host.rstrip("/")

    def get_token(self, user: str, password: str) -> str:
        """Get a Session Token used for authentication in API requests."""
        response = requests.post(
            self.host + "/api/session",
            json={"username": user, "password": password},
        )

        if response.status_code != 200:
            raise AuthenticationError(response.content.decode())

        return response.json()["id"]

    def get(self, endpoint: str, **kwargs):
        """Execute a GET request on a given endpoint."""
        return requests.get(self.host + endpoint, headers=self.headers, **kwargs)

    def post(self, endpoint: str, **kwargs):
        """Execute a POST request on a given endpoint."""
        return requests.post(self.host + endpoint, headers=self.headers, **kwargs)

    def put(self, endpoint: str, **kwargs):
        """Execute a PUT request on a given endpoint."""
        return requests.put(self.host + endpoint, headers=self.headers, **kwargs)

    def delete(self, endpoint: str, **kwargs):
        """Execute a DELETE request on a given endpoint."""
        return requests.delete(self.host + endpoint, headers=self.headers, **kwargs)


class Metabase:
    def __init__(
        self,
        host: str,
        user: str,
        password: str,
        token: str = None,
        name: str = "default",
    ):
        self.host = host
        self.user = user
        self.password = password
        self.token = token

        self.connection = Connection(
            name=name, host=host, user=user, password=password, token=token
        )
