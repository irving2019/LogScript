from datetime import date
from pathlib import Path


from log_reporter.parser import read_logs


FIXTURE = Path(__file__).parent / 'fixtures' / 'sample.log'


def test_read_logs_all():
    records = list(read_logs([str(FIXTURE)]))
    assert len(records) == 3
    assert records[0].url == '/api/test'


def test_read_logs_filter_date():
    records = list(read_logs([str(FIXTURE)], date(2023, 1, 2)))
    assert len(records) == 1
    assert records[0].url == '/api/other'


def test_read_logs_invalid_lines(capfd):
    list(read_logs([str(FIXTURE)]))
    err = capfd.readouterr().err
    assert 'Invalid timestamp' in err
    assert 'Invalid response_time' in err
