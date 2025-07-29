from types import SimpleNamespace
from unittest import mock

from log_reporter.main import main


def test_cli_invokes_report(monkeypatch, tmp_path):
    dummy_module = SimpleNamespace(FakeReport=mock.Mock())
    import importlib
    monkeypatch.setattr(importlib, 'import_module', lambda name, package=None: dummy_module)
    log_file = tmp_path / 'log.log'
    log_file.write_text('{"@timestamp":"2023-01-01T00:00:00Z","url":"/a","response_time":0.1}\n')
    result = main(['--file', str(log_file), '--report', 'fake'])
    assert result == 0
    assert dummy_module.FakeReport.called
