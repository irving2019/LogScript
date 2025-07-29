# Log Reporter

This project provides a small CLI for processing JSON log files. It aggregates statistics about URL handlers and prints a table report.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python -m log_reporter.main --file path/to/file.log --report average [--date YYYY-MM-DD]
```

Several `--file` arguments can be provided. The report will display total requests and average response time per handler.
