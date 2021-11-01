from __future__ import annotations

from exceptions import NotFoundError
from metabase import Metabase
from requests import HTTPError


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

        return self.__class__.__qualname__ + "(" + ', '.join([f"{attr}={getattr(self, attr)}" for attr in attributes]) + ")"

    @staticmethod
    def connection() -> Metabase:
        return Metabase()


class ListResource(Resource):
    @classmethod
    def list(cls):
        """List all instances."""
        response = cls.connection().get(cls.ENDPOINT)
        records = [cls(**record) for record in response.json()]
        return records


class GetResource(Resource):
    @classmethod
    def get(cls, id: int):
        """Get a single instance by ID."""
        response = cls.connection().get(cls.ENDPOINT + f"/{id}")

        if response.status_code == 404 or response.status_code == 204:
            raise NotFoundError(f"{cls.__name__}(id={id}) was not found.")

        return cls(**response.json())


class CreateResource(Resource):
    @classmethod
    def create(cls, **kwargs):
        """Create an instance and save it."""
        response = cls.connection().post(cls.ENDPOINT, json=kwargs)

        if response.status_code != 200:
            raise HTTPError(response.content.decode())

        return cls(**response.json())


class UpdateResource(Resource):
    def update(self, **kwargs) -> None:
        """Update an instance."""
        response = self.connection().put(self.ENDPOINT + f"/{getattr(self, self.PRIMARY_KEY)}", json=kwargs)

        if response.status_code != 200:
            raise HTTPError(response.json())

        for k, v in kwargs.items():
            setattr(self, k, v)


class DeleteResource(Resource):
    def delete(self) -> None:
        """Delete an instance."""
        response = self.connection().delete(self.ENDPOINT + f"/{getattr(self, self.PRIMARY_KEY)}")

        if response.status_code != 204:
            raise HTTPError(response.content.decode())
