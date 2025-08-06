# Техническое задание: Скрипт для обработки JSON-логов

## 1. Цель

Разработать консольный Python-скрипт `main.py`, который:

- Читает один или несколько файлов логов в формате JSON (по одному объекту JSON на строку)
- Аггрегирует данные по эндпоинтам: считает общее число запросов и среднее время ответа
- Поддерживает фильтрацию по дате
- Выводит результат в виде красиво отформатированной таблицы в консоль

## 2. Функциональные требования

### 2.1. CLI и параметры

Использовать стандартную библиотеку `argparse`.

Скрипт вызывается как:

```bash
python main.py --file file1.log [--file file2.log …] --report average [--date YYYY-MM-DD]
```

Параметры:

- `--file` (или `-f`): путь к лог-файлу. Можно указывать несколько раз.
- `--report` (или `-r`): тип отчёта. Обязательный. Поддерживать минимум "average".
- `--date` (или `-d`): фильтр по дате: брать только записи, у которых поле `@timestamp` соответствует указанной дате (формат ISO 8601). Опционально.

### 2.2. Парсинг логов

- Для каждого файла читать построчно, не загружая весь файл в память
- Парсить JSON каждой строки; при ошибке парсинга — логировать предупреждение в stderr и пропускать строку
- Из каждого объекта извлекать поля:
  - `@timestamp` (строка ISO 8601)
  - `url` (строка — эндпоинт)
  - `response_time` (число — время ответа в секундах)

### 2.3. Агрегация

По каждому уникальному `url` хранить:
- `count` — общее число попаданий
- `total_time` — сумма всех `response_time`

После чтения всех файлов для каждой записи вычислить:
```
average_time = total_time / count
```

### 2.4. Вывод отчёта

Использовать библиотеку `tabulate` (можно добавить в `requirements.txt`).

Формат таблицы:

```
handler             total    avg_response_time
/api/homeworks/...  55312    0.093
/api/context/...    43928    0.019
```

- Заголовки: `handler`, `total`, `avg_response_time`
- Результаты сортировать по убыванию `total`

## 3. Нефункциональные требования

- Язык: Python 3.8+
- Код должен соответствовать PEP 8
- Использовать typing (например, `TypedDict` или `@dataclass`) для описания структуры записи лога
- Обработка ошибок: скрипт никогда не должен падать на невалидных строках; в таких случаях выводить предупреждение
- Проект должен содержать `README.md` с кратким описанием, инструкцией по запуску и примерами

## 4. Архитектура и структура проекта

```
log_reporter/
├── main.py              # точка входа, парсинг аргументов и запуск
├── parser.py            # функции чтения и валидации логов
├── models.py            # @dataclass LogRecord или TypedDict
├── reports/
│   ├── base.py          # абстрактный класс Report
│   └── average.py       # класс AverageReport(Report)
├── formatter.py         # обёртка над tabulate для вывода
├── utils.py             # вспомогательные функции (парсинг даты и т.п.)
├── requirements.txt     # зависимость: tabulate
├── README.md            # инструкция
└── tests/
    ├── conftest.py
    ├── test_parser.py
    ├── test_average_report.py
    ├── test_cli.py
    └── fixtures/
        └── sample.log   # небольшой пример логов
```

## 5. Детали реализации

### 5.1. main.py

- Определить `ArgumentParser` с описанными выше опциями
- В зависимости от `--report` динамически импортировать нужный класс из `reports/`
- Передать в объект отчёта результаты `parser.read_logs(files, date)` и вывести `report.render()`

### 5.2. parser.py

Функция `read_logs(files: List[str], date: Optional[date]) -> Iterator[LogRecord]`.

Чтение файлов, фильтрация по дате, валидация полей.

### 5.3. models.py

```python
from dataclasses import dataclass
from datetime import datetime

@dataclass
class LogRecord:
    timestamp: datetime
    url: str
    response_time: float
```

### 5.4. reports/base.py

```python
from abc import ABC, abstractmethod
from typing import Iterable
from models import LogRecord

class Report(ABC):
    @abstractmethod
    def __init__(self, records: Iterable[LogRecord]) -> None: ...
    
    @abstractmethod
    def render(self) -> str:  # возвращает строку-таблицу
        ...
```

### 5.5. reports/average.py

- Наследует `Report`
- В `__init__` собирает статистику (`count`, `total_time`) по `record.url`
- В `render()` формирует и возвращает таблицу `tabulate`

### 5.6. formatter.py

```python
from tabulate import tabulate
from typing import List, Any

def format_table(headers: List[str], rows: List[List[Any]]) -> str:
    return tabulate(rows, headers, tablefmt="github", floatfmt=".3f")
```

## 6. Тестирование

Использовать `pytest`.

Покрытие:
- `parser.read_logs`: и корректные, и некорректные строки, фильтрация по дате
- `AverageReport`: на небольшом наборе `LogRecord`
- CLI (модульный тест): проверить, что при передаче фиктивных файлов и опций создаётся нужный объект и что `render()` вызывается
- Для интеграционных тестов можно создавать временный файл `tmp_path` и сравнивать stdout

## 7. Критерии приёмки

- Все команды `pytest` проходят без ошибок
- Скрипт корректно обрабатывает хотя бы 10 000 строк за ~1 секунду (стриминг)
- При ошибочной строке в логе — выводится предупреждение в stderr, exit code = 0
- `README.md` содержит:
  - Описание проекта
  - Инструкцию по установке зависимостей
  - Примеры команд и ожидаемый вывод
