from weakref import WeakValueDictionary

import requests


class Singleton(type):
    _instances = WeakValueDictionary()

    def __call__(cls, *args, **kw):
        if cls not in cls._instances:
            instance = super(Singleton, cls).__call__(*args, **kw)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Metabase(metaclass=Singleton):
    def __init__(self, host: str, user: str, password: str, token: str = None):
        self._host = host
        self.user = user
        self.password = password
        self._token = token

    @property
    def host(self):
        host = self._host

        if not host.startswith("http"):
            host = "https://" + self._host

        return host.rstrip("/")

    @host.setter
    def host(self, value):
        self._host = value

    @property
    def token(self):
        if self._token is None:
            response = requests.post(
                self.host + "/api/session",
                json={"username": self.user, "password": self.password},
            )
            self._token = response.json()["id"]

        return self._token

    @token.setter
    def token(self, value):
        self._token = value

    @property
    def headers(self):
        return {"X-Metabase-Session": self.token}

    def get(self, endpoint: str, **kwargs):
        return requests.get(self.host + endpoint, headers=self.headers, **kwargs)

    def post(self, endpoint: str, **kwargs):
        return requests.post(self.host + endpoint, headers=self.headers, **kwargs)

    def put(self, endpoint: str, **kwargs):
        return requests.put(self.host + endpoint, headers=self.headers, **kwargs)

    def delete(self, endpoint: str, **kwargs):
        return requests.delete(self.host + endpoint, headers=self.headers, **kwargs)
