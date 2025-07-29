from typing import Any, List

from tabulate import tabulate


def format_table(headers: List[str], rows: List[List[Any]]) -> str:
    return tabulate(rows, headers, tablefmt="github", floatfmt=".3f")
