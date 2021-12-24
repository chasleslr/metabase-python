from __future__ import annotations

from requests import HTTPError

from metabase.exceptions import NotFoundError
from metabase.metabase import Connection
from metabase.missing import MISSING


class Resource:
    ENDPOINT: str
    PRIMARY_KEY: str = "id"

    def __init__(self, **kwargs):
        self._attributes = []

        for k, v in kwargs.items():
            self._attributes.append(k)
            setattr(self, k, v)

    def __repr__(self):
        # move primary key to beginning of the list
        attributes = self._attributes.copy()
        if self.PRIMARY_KEY is not None:
            attributes.insert(0, attributes.pop(attributes.index(self.PRIMARY_KEY)))

        return (
            self.__class__.__qualname__
            + "("
            + ", ".join([f"{attr}={getattr(self, attr)}" for attr in attributes])
            + ")"
        )

    @staticmethod
    def connection(using) -> Connection:
        return Connection.instances[using]


class ListResource(Resource):
    @classmethod
    def list(cls, using: str = "default"):
        """List all instances."""
        response = cls.connection(using).get(cls.ENDPOINT)
        records = [cls(**record) for record in response.json()]
        return records


class GetResource(Resource):
    @classmethod
    def get(cls, id: int, using: str = "default"):
        """Get a single instance by ID."""
        response = cls.connection(using).get(cls.ENDPOINT + f"/{id}")

        if response.status_code == 404 or response.status_code == 204:
            raise NotFoundError(f"{cls.__name__}(id={id}) was not found.")

        return cls(**response.json())


class CreateResource(Resource):
    @classmethod
    def create(cls, using: str = "default", **kwargs):
        """Create an instance and save it."""
        response = cls.connection(using).post(cls.ENDPOINT, json=kwargs)

        if response.status_code not in (200, 202):
            raise HTTPError(response.content.decode())

        return cls(**response.json())


class UpdateResource(Resource):
    def update(self, using: str = "default", **kwargs) -> None:
        """
        Update an instance by providing function arguments.
        Providing any argument with metabase.MISSING will result in this argument being
        ignored from the request.
        """
        params = {k: v for k, v in kwargs.items() if v != MISSING}
        response = self.connection(using).put(
            self.ENDPOINT + f"/{getattr(self, self.PRIMARY_KEY)}", json=params
        )

        if response.status_code not in (200, 202):
            raise HTTPError(response.json())

        for k, v in kwargs.items():
            setattr(self, k, v)


class DeleteResource(Resource):
    def delete(self, using: str = "default") -> None:
        """Delete an instance."""
        response = self.connection(using).delete(
            self.ENDPOINT + f"/{getattr(self, self.PRIMARY_KEY)}"
        )

        if response.status_code not in (200, 204):
            raise HTTPError(response.content.decode())
