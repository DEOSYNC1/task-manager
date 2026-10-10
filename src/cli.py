"""Командный интерфейс приложения «Менеджер задач»."""

from __future__ import annotations

import argparse
import sys

from .models import Priority, Status, Task
from .service import TaskService


def _build_parser() -> argparse.ArgumentParser:
    """Создаёт парсер аргументов командной строки."""
    parser = argparse.ArgumentParser(
        prog="task-manager",
        description="Консольный менеджер личных задач.",
    )
    parser.add_argument("--file", default="tasks.json", help="путь к файлу хранилища")
    sub = parser.add_subparsers(dest="command", required=True)

    p_add = sub.add_parser("add", help="добавить задачу")
    p_add.add_argument("title", help="текст задачи")
    p_add.add_argument(
        "-p",
        "--priority",
        choices=[item.value for item in Priority],
        default=Priority.MEDIUM.value,
        help="приоритет задачи",
    )

    p_list = sub.add_parser("list", help="показать задачи")
    p_list.add_argument(
        "--status",
        choices=[item.value for item in Status],
        help="фильтр по статусу",
    )
    p_list.add_argument(
        "--priority",
        choices=[item.value for item in Priority],
        help="фильтр по приоритету",
    )

    p_done = sub.add_parser("done", help="отметить задачу выполненной")
    p_done.add_argument("id", type=int, help="идентификатор задачи")

    p_rm = sub.add_parser("remove", help="удалить задачу")
    p_rm.add_argument("id", type=int, help="идентификатор задачи")

    return parser


def _format_task(task: Task) -> str:
    """Форматирует задачу в строку для вывода."""
    mark = "[x]" if task.status is Status.DONE else "[ ]"
    return f"{task.id:>3} {mark} ({task.priority.value:6}) {task.title}"


def run(argv: list[str] | None = None) -> int:
    """Запускает CLI и возвращает код возврата."""
    args = _build_parser().parse_args(argv)
    service = TaskService(args.file)

    if args.command == "add":
        task = service.add(args.title, Priority(args.priority))
        print(f"Задача добавлена: #{task.id} «{task.title}»")
        return 0

    if args.command == "list":
        status = Status(args.status) if args.status else None
        priority = Priority(args.priority) if args.priority else None
        tasks = service.list(status=status, priority=priority)
        if not tasks:
            print("Задач нет.")
            return 0
        for task in tasks:
            print(_format_task(task))
        return 0

    if args.command == "done":
        task = service.mark_done(args.id)
        if task is None:
            print(f"Задача #{args.id} не найдена.")
            return 1
        print(f"Задача #{args.id} отмечена выполненной.")
        return 0

    if args.command == "remove":
        if service.remove(args.id):
            print(f"Задача #{args.id} удалена.")
            return 0
        print(f"Задача #{args.id} не найдена.")
        return 1

    parser = _build_parser()
    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(run())