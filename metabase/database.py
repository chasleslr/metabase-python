from dataclasses import dataclass
from enum import Enum
from typing import List

from metabase.resource import Resource


@dataclass
class Database(Resource):
    ENDPOINT = "/api/database"

    class Engine(str, Enum):
        H2 = "h2"
        POSTGRES = "postgres"
        SNOWFLAKE = "snowflake"

    id: int
    name: str
    engine: Engine
    details: dict

    description: str = None
    is_full_sync: bool = None
    is_on_demand: bool = None
    schedules: dict = None
    auto_run_queries: bool = None
    cache_ttl: int = None

    @classmethod
    def all(cls) -> List["Database"]:
        response = cls.connection().get(cls.ENDPOINT)
        records = [cls.from_dict(db) for db in response.json().get("data", [])]
        return records

    @classmethod
    def create(cls, name: str, engine: Engine, details: dict, **kwargs) -> "Database":
        response = cls.connection().post(
            cls.ENDPOINT,
            json={
                "name": name,
                "engine": engine,
                "details": details,
                **kwargs
            }
        )
        return cls.from_dict(response.json())

    def delete(self) -> None:
        self.connection().delete(self.ENDPOINT + f"/{self.id}")

    def discard_values(self):
        self.connection().post(self.ENDPOINT + f"/{self.id}" + "/discard_values")

    def rescan_values(self):
        self.connection().post(self.ENDPOINT + f"/{self.id}" + "/rescan_values")

    def sync(self):
        self.connection().post(self.ENDPOINT + f"/{self.id}" + "/sync")

    def sync_schema(self):
        self.connection().post(self.ENDPOINT + f"/{self.id}" + "/sync_schema")
