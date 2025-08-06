# LogScript - Анализатор JSON-логов

## Описание

LogScript - это консольная утилита для анализа файлов логов в формате JSON. Скрипт агрегирует данные по эндпоинтам, считает общее количество запросов и среднее время ответа, а также поддерживает фильтрацию по дате.

## Возможности

- 📖 Чтение множественных файлов логов в формате JSON
- 📊 Агрегация данных по эндпоинтам (URL)
- ⏱️ Расчёт среднего времени ответа
- 📅 Фильтрация по дате
- 📋 Красивый табличный вывод результатов
- 🚫 Устойчивость к некорректным строкам в логах

## Требования

- Python 3.8+
- Зависимости из `requirements.txt`

## Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/irving2019/LogScript.git
cd LogScript
```

2. Установите зависимости:
```bash
pip install -r requirements.txt
```

## Использование

### Основной синтаксис

```bash
python log_reporter/main.py --file file1.log [--file file2.log ...] --report average [--date YYYY-MM-DD]
```

### Параметры

- `--file` / `-f` - путь к файлу лога (можно указать несколько раз)
- `--report` / `-r` - тип отчёта (в данный момент поддерживается только "average")
- `--date` / `-d` - фильтр по дате в формате ISO 8601 (YYYY-MM-DD)

### Примеры использования

#### Анализ одного файла

```bash
python log_reporter/main.py --file logs/app.log --report average
```

#### Анализ нескольких файлов

```bash
python log_reporter/main.py --file logs/app1.log --file logs/app2.log --report average
```

#### Анализ с фильтрацией по дате

```bash
python log_reporter/main.py --file logs/app.log --report average --date 2025-01-15
```

## Формат входных данных

Скрипт ожидает файлы логов в формате JSON, где каждая строка содержит отдельный JSON-объект:

```json
{"@timestamp": "2025-01-15T10:30:00Z", "url": "/api/users", "response_time": 0.045}
{"@timestamp": "2025-01-15T10:31:00Z", "url": "/api/orders", "response_time": 0.123}
{"@timestamp": "2025-01-15T10:32:00Z", "url": "/api/users", "response_time": 0.067}
```

### Обязательные поля

- `@timestamp` - временная метка в формате ISO 8601
- `url` - эндпоинт/URL запроса
- `response_time` - время ответа в секундах (число)

## Формат вывода

Результат выводится в виде таблицы, отсортированной по убыванию общего количества запросов:

```
| handler             | total | avg_response_time |
|---------------------|-------|-------------------|
| /api/users          | 1523  | 0.056            |
| /api/orders         | 892   | 0.123            |
| /api/products       | 445   | 0.089            |
```

## Архитектура проекта

```
log_reporter/
├── main.py              # Точка входа и CLI
├── parser.py            # Парсинг и валидация логов
├── models.py            # Модели данных
├── formatter.py         # Форматирование вывода
├── utils.py             # Вспомогательные функции
└── reports/
    ├── __init__.py
    ├── base.py          # Абстрактный класс отчёта
    └── average.py       # Отчёт по среднему времени ответа
```

## Тестирование

Для запуска тестов используйте pytest:

```bash
# Запуск всех тестов
pytest

# Запуск тестов с покрытием
pytest --cov=log_reporter

# Запуск конкретного теста
pytest tests/test_parser.py
```

## Производительность

- Скрипт обрабатывает файлы построчно, не загружая их полностью в память
- Способен обрабатывать 10,000+ строк за ~1 секунду
- Устойчив к некорректным строкам JSON

## Обработка ошибок

- При встрече некорректной JSON-строки выводится предупреждение в stderr
- Скрипт продолжает работу и не завершается с ошибкой
- Exit code всегда равен 0 при нормальном завершении

## Разработка

### Добавление нового типа отчёта

1. Создайте новый класс в `log_reporter/reports/`, наследующий от `Report`
2. Реализуйте методы `__init__` и `render`
3. Добавьте импорт в `main.py`

### Структура отчёта

```python
from log_reporter.reports.base import Report
from log_reporter.models import LogRecord

class MyReport(Report):
    def __init__(self, records: Iterable[LogRecord]) -> None:
        # Инициализация и обработка данных
        pass
    
    def render(self) -> str:
        # Возврат отформатированной таблицы
        return formatted_table
```

## Контакты

- Автор: [irving2019](https://github.com/irving2019)
- Репозиторий: [LogScript](https://github.com/irving2019/LogScript)