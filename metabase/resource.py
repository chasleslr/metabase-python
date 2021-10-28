from dataclasses import dataclass, field, fields
from typing import List

from exceptions import NotFoundError
from metabase.metabase import Metabase


class Resource:
    ENDPOINT: str
    PRIMARY_KEY: str = "id"

    @staticmethod
    def connection() -> Metabase:
        return Metabase()

    @classmethod
    def from_dict(cls, payload: dict) -> "Resource":
        f = [field.name for field in fields(cls)]
        p = {k: payload[k] for k in payload.keys() if k in f}
        return cls(**p)


class ListResource(Resource):
    @classmethod
    def list(cls) -> List["Resource"]:
        """List all instances."""
        response = cls.connection().get(cls.ENDPOINT)
        records = [cls.from_dict(record) for record in response.json()]
        return records


class GetResource(Resource):
    @classmethod
    def get(cls, id: int) -> "Resource":
        """Get a single instance by ID."""
        response = cls.connection().get(cls.ENDPOINT + f"/{id}")

        if response.status_code == 404:
            raise NotFoundError(f"{cls.__name__}(id={id}) was not found.")

        return cls.from_dict(response.json())


class CreateResource(Resource):
    @classmethod
    def create(cls, **kwargs) -> "Resource":
        """Create an instance and save it."""
        raise NotImplementedError()


class UpdateResource(Resource):
    def update(self) -> None:
        """Update an instance."""
        raise NotImplementedError()


class DeleteResource(Resource):
    def delete(self) -> None:
        """Delete an instance."""
        self.connection().delete(self.ENDPOINT + f"/{getattr(self, self.PRIMARY_KEY)}")
