from log_reporter.models import LogRecord
from log_reporter.reports.average import AverageReport
from datetime import datetime


def make_record(url: str, rt: float) -> LogRecord:
    return LogRecord(timestamp=datetime.utcnow(), url=url, response_time=rt)


def test_average_report():
    records = [
        make_record('/a', 0.1),
        make_record('/a', 0.3),
        make_record('/b', 0.2),
    ]
    report = AverageReport(records)
    table = report.render()
    assert '| handler   |   total |   avg_response_time |' in table.splitlines()[0]
    assert '/a' in table
    assert '/b' in table
