import sys
import argparse
import importlib
from datetime import date
from typing import List, Optional

from .parser import read_logs
from .utils import parse_date


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', action='append', required=True, help='log file path')
    parser.add_argument('-r', '--report', required=True, help='report type')
    parser.add_argument('-d', '--date', help='filter by date YYYY-MM-DD')
    return parser


def main(argv: Optional[List[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    report_type = args.report
    module = importlib.import_module(f'.reports.{report_type}', __package__)
    report_cls = getattr(module, f'{report_type.capitalize()}Report')
    filter_date: Optional[date] = None
    if args.date:
        filter_date = parse_date(args.date)
        if filter_date is None:
            print('Invalid date format. Use YYYY-MM-DD.', file=sys.stderr)
            return 1
    records = list(read_logs(args.file, filter_date))
    report = report_cls(records)
    print(report.render())
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
