from metabase.resources.dataset import Data, Dataset

from tests.helpers import IntegrationTestCase

import pandas as pd


class DatasetTests(IntegrationTestCase):
    def test_import(self):
        """Ensure Metric can be imported from Metabase."""
        from metabase import Dataset
        self.assertIsNotNone(Dataset())

    def test_create(self):
        """Ensure Dataset.create() executes a query and returns a Dataset instance with the query results."""
        dataset = Dataset.create(
            database=1,
            type="query",
            query={
                "source-table": 1,
                "breakout": [["field", 7, {"temporal-unit": "year"}]],
                "aggregation": [["count"]]
            }
        )
        self.assertIsInstance(dataset, Dataset)
        self.assertIsInstance(dataset.data, Data)

    def test_to_pandas(self):
        """Ensure Dataset.to_pandas() returns a Pandas DataFrame."""
        dataset = Dataset.create(
            database=1,
            type="query",
            query={
                "source-table": 1,
                "breakout": [["field", 7, {"temporal-unit": "year"}]],
                "aggregation": [["count"]]
            }
        )
        df = dataset.to_pandas()
        self.assertIsInstance(df, pd.DataFrame)
        self.assertListEqual(["Created At", "Count"], df.columns.tolist())