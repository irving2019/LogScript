import sys
import json
from datetime import datetime, date
from pathlib import Path
from typing import Iterator, Iterable, Optional

from .models import LogRecord


def parse_timestamp(value: str) -> Optional[datetime]:
    try:
        return datetime.fromisoformat(value.replace('Z', '+00:00'))
    except ValueError:
        return None


def read_logs(files: Iterable[str], target_date: Optional[date] = None) -> Iterator[LogRecord]:
    for file_path in files:
        path = Path(file_path)
        if not path.is_file():
            continue
        with path.open() as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                except json.JSONDecodeError:
                    print(f"Invalid JSON line: {line}", file=sys.stderr)
                    continue
                ts_str = obj.get('@timestamp')
                url = obj.get('url')
                rt = obj.get('response_time')
                if ts_str is None or url is None or rt is None:
                    print(f"Missing fields in line: {line}", file=sys.stderr)
                    continue
                ts = parse_timestamp(ts_str)
                if ts is None:
                    print(f"Invalid timestamp: {ts_str}", file=sys.stderr)
                    continue
                if target_date and ts.date() != target_date:
                    continue
                try:
                    rt = float(rt)
                except (TypeError, ValueError):
                    print(f"Invalid response_time: {rt}", file=sys.stderr)
                    continue
                yield LogRecord(timestamp=ts, url=str(url), response_time=rt)
