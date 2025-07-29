from abc import ABC, abstractmethod
from typing import Iterable

from ..models import LogRecord


class Report(ABC):
    @abstractmethod
    def __init__(self, records: Iterable[LogRecord]) -> None:
        ...

    @abstractmethod
    def render(self) -> str:
        ...
