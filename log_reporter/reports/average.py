from collections import defaultdict
from typing import Iterable, List

from ..formatter import format_table
from ..models import LogRecord
from .base import Report


class AverageReport(Report):
    def __init__(self, records: Iterable[LogRecord]) -> None:
        stats = defaultdict(lambda: {'count': 0, 'total_time': 0.0})
        for r in records:
            stat = stats[r.url]
            stat['count'] += 1
            stat['total_time'] += r.response_time
        self.rows: List[List] = []
        for url, s in stats.items():
            avg = s['total_time'] / s['count']
            self.rows.append([url, s['count'], avg])
        self.rows.sort(key=lambda x: x[1], reverse=True)

    def render(self) -> str:
        headers = ['handler', 'total', 'avg_response_time']
        return format_table(headers, self.rows)
