from dataclasses import dataclass, field
from typing import List

from metabase.mbql.aggregations import Aggregation
from metabase.mbql.filter import Filter
from metabase.mbql.groupby import GroupBy


@dataclass
class Query:
    table_id: int
    aggregations: List[Aggregation]
    group_by: List[GroupBy] = field(default_factory=list)
    filters: List[Filter] = field(default_factory=list)

    def compile(self):
        return {
            "source-table": self.table_id,
            "aggregation": self._aggregations,
            "breakout": self._group_by,
            "filter": self._filters,
        }

    @property
    def _aggregations(self):
        return [aggregation.compile() for aggregation in self.aggregations]

    @property
    def _group_by(self):
        return [group.compile() for group in self.group_by]

    @property
    def _filters(self):
        if len(self.filters) == 0:
            return self.filters

        if len(self.filters) == 1:
            return self.filters[0].compile()

        return ["and"] + [filt.compile() for filt in self.filters]
