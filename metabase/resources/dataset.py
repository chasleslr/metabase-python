from __future__ import annotations

from dataclasses import dataclass
from typing import Any, List

import pandas as pd

from metabase.resource import CreateResource, Resource


class Data(Resource):
    ENDPOINT = None
    PRIMARY_KEY = None

    rows: List[List[Any]]
    cols: dict
    native_form: dict

    def to_pandas(self):
        """Returns the query results as a Pandas DataFrame."""
        columns = [col["display_name"] for col in self.cols]
        return pd.DataFrame(data=self.rows, columns=columns)


class Dataset(CreateResource):
    ENDPOINT = "/api/dataset"
    PRIMARY_KEY = None

    context: str
    status: str
    database_id: int
    data: Data
    row_count: int

    started_at: str
    running_time: int
    json_query: str
    average_execution_time: int = None

    @classmethod
    def create(cls, database: int, type: str, query: dict, **kwargs) -> Dataset:
        dataset = super(Dataset, cls).create(database=database, type=type, query=query)
        dataset.data = Data(**dataset.data)
        return dataset

    def to_pandas(self) -> pd.DataFrame:
        """Returns the query results as a Pandas DataFrame."""
        return self.data.to_pandas()
