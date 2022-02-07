from __future__ import annotations

from typing import Any, List

import pandas as pd

from metabase import Metabase
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
    def create(
        cls, using: Metabase, database: int, type: str, query: dict, **kwargs
    ) -> Dataset:
        """Execute a query and retrieve the results in the usual format."""
        dataset = super(Dataset, cls).create(
            using=using, database=database, type=type, query=query
        )
        dataset.data = Data(_using=using, **dataset.data)
        return dataset

    def to_pandas(self) -> pd.DataFrame:
        """Returns the query results as a Pandas DataFrame."""
        return self.data.to_pandas()
