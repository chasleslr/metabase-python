from __future__ import annotations

from requests import HTTPError

from metabase.exceptions import NotFoundError
from metabase.metabase import Metabase
from metabase.missing import MISSING


class Resource:
    ENDPOINT: str
    PRIMARY_KEY: str = "id"

    def __init__(self, _using: Metabase, **kwargs):
        self._attributes = []
        self._using = _using

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


class ListResource(Resource):
    @classmethod
    def list(cls, using: Metabase):
        """List all instances."""
        response = using.get(cls.ENDPOINT)
        records = [cls(_using=using, **record) for record in response.json()]
        return records


class GetResource(Resource):
    @classmethod
    def get(cls, id: int, using: Metabase):
        """Get a single instance by ID."""
        response = using.get(cls.ENDPOINT + f"/{id}")

        if response.status_code == 404 or response.status_code == 204:
            raise NotFoundError(f"{cls.__name__}(id={id}) was not found.")

        return cls(_using=using, **response.json())


class CreateResource(Resource):
    @classmethod
    def create(cls, using: Metabase, **kwargs):
        """Create an instance and save it."""
        response = using.post(cls.ENDPOINT, json=kwargs)

        if response.status_code not in (200, 202):
            raise HTTPError(response.content.decode())

        return cls(_using=using, **response.json())


class UpdateResource(Resource):
    def update(self, **kwargs) -> None:
        """
        Update an instance by providing function arguments.
        Providing any argument with metabase.MISSING will result in this argument being
        ignored from the request.
        """
        params = {k: v for k, v in kwargs.items() if v != MISSING}
        response = self._using.put(
            self.ENDPOINT + f"/{getattr(self, self.PRIMARY_KEY)}", json=params
        )

        if response.status_code not in (200, 202):
            raise HTTPError(response.json())

        for k, v in kwargs.items():
            setattr(self, k, v)


class DeleteResource(Resource):
    def delete(self) -> None:
        """Delete an instance."""
        response = self._using.delete(
            self.ENDPOINT + f"/{getattr(self, self.PRIMARY_KEY)}"
        )

        if response.status_code not in (200, 204):
            raise HTTPError(response.content.decode())
