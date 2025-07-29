from dataclasses import dataclass
from datetime import datetime


@dataclass
class LogRecord:
    timestamp: datetime
    url: str
    response_time: float
