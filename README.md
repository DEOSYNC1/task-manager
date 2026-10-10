# Менеджер задач

Консольное приложение на Python для ведения личного списка задач: добавление,
просмотр с фильтрацией, отметка выполнения и удаление. Проект контейнеризован
с помощью Docker и сопровождается автоматическими тестами и инструментами
качества кода (black, isort, ruff, pre-commit).

## Цель проекта

Закрепить практику разработки на Python: модульная структура, юнит-тесты,
контейнеризация и настройка качества кода.

## Архитектура

```
task-manager/
├── src/
│   ├── __init__.py
│   ├── main.py        # точка входа
│   ├── cli.py         # разбор аргументов и вывод
│   ├── models.py      # модель данных (Task, Priority, Status)
│   ├── service.py     # бизнес-логика
│   └── storage.py     # чтение/запись JSON
├── tests/
│   └── test_service.py
├── Dockerfile
├── requirements.txt        # зависимости приложения
├── requirements-dev.txt    # dev-инструменты
├── .pre-commit-config.yaml
├── .gitignore
└── .dockerignore
```

Код разбит на слои: CLI (`cli.py`) → бизнес-логика (`service.py`) →
хранилище (`storage.py`) → модель (`models.py`). `main.py` — точка входа.

## Запуск локально

```bash
python -m src.main --file my_tasks.json add "Купить молоко" --priority high
python -m src.main list
python -m src.main list --status pending
python -m src.main done 1
python -m src.main remove 1
```

Данные сохраняются в `tasks.json` (путь можно задать флагом `--file`).
Требуется Python 3.10+; внешних runtime-зависимостей нет.

## Запуск в Docker

Сборка образа:

```bash
docker build -t task-manager .
```

Запуск контейнера (хранилище монтируется в `data/`):

```bash
docker run --rm -v "$(pwd)/data:/app/data" task-manager add "Купить молоко" --priority high
docker run --rm -v "$(pwd)/data:/app/data" task-manager list
```

Чтобы закрепить порт и использовать переменные окружения (демонстрация,
реальный CLI хранилище не держит в сети):

```bash
docker run --rm -p 8000:8000 --env-file .env task-manager list
```

## Конфигурация

Никаких обязательных переменных окружения нет. Опционально задаётся путь к
хранилищу:

| Переменная      | Назначение                      | По умолчанию |
|-----------------|---------------------------------|--------------|
| `TASKS_FILE`    | путь к файлу JSON-хранилища     | `tasks.json` |

> Примечание: флаг `--file` имеет приоритет над переменной окружения.

## Примеры использования

```bash
# Создать хранилище и добавить задачи
python -m src.main --file tasks.json add "Написать отчёт" --priority high
python -m src.main --file tasks.json add "Сходить в зал" --priority low

# Показать все задачи
python -m src.main --file tasks.json list

# Показать только невыполненные высокой важности
python -m src.main --file tasks.json list --status pending --priority high

# Отметить выполненной задачу #1 и удалить задачу #2
python -m src.main --file tasks.json done 1
python -m src.main --file tasks.json remove 2
```

Пример вывода:

```
  1 [x] (  high) Написать отчёт
  2 [ ] (   low) Сходить в зал
```

## Качество кода

```bash
pip install -r requirements-dev.txt
black --check src tests
isort --check-only src tests
ruff check src tests
pytest -q
```

Git-хуки настроены через pre-commit:

```bash
pre-commit install
pre-commit run --all-files
```

## Зависимости

- **Приложение:** только стандартная библиотека Python 3.10+.
- **Разработка:** black 24.8.0, isort 5.13.2, ruff 0.6.9, pytest 8.3.2
  (см. `requirements-dev.txt`).

## Коммиты и история

Проект ведётся как публичный репозиторий Git.
