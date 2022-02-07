from dataclasses import dataclass, field
from typing import List, Union

from metabase.mbql.aggregations import Aggregation
from metabase.mbql.groupby import GroupBy


@dataclass
class Query:
    table_id: int
    aggregations: List[Union[Aggregation, Metric]]
    group_by: List[GroupBy] = field(default_factory=list)
    filters: List[Filter] = field(default_factory=list)

    def compile(self):
        return {
            "source-table": self.table_id,
            "aggregation": [agg.compile() for agg in self.aggregations],
            "breakout": [],
            "filter": [],
        }
