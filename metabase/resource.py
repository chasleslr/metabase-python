from dataclasses import dataclass, field, fields
from typing import List

from exceptions import NotFoundError
from metabase.metabase import Metabase


@dataclass
class Resource:
    ENDPOINT: str = field(init=False, repr=False)

    @staticmethod
    def connection() -> Metabase:
        return Metabase()

    @classmethod
    def all(cls) -> List["Resource"]:
        raise NotImplementedError()

    @classmethod
    def get(cls, id: int) -> "Resource":
        response = cls.connection().get(cls.ENDPOINT + f"/{id}")

        if response.status_code == 404:
            raise NotFoundError(f"{cls.__name__}(id={id}) was not found.")

        return cls.from_dict(response.json())

    @classmethod
    def create(cls, **kwargs) -> "Resource":
        raise NotImplementedError()

    def update(self) -> None:
        raise NotImplementedError()

    def delete(self) -> None:
        self.connection().delete(self.ENDPOINT + f"/{self.id}")

    @classmethod
    def from_dict(cls, payload: dict) -> "Resource":
        f = [field.name for field in fields(cls)]
        p = {k: payload[k] for k in payload.keys() if k in f}
        return cls(**p)
