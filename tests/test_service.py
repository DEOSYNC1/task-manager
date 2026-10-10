"""Тесты бизнес-логики приложения на pytest."""

from __future__ import annotations

from src.models import Priority, Status
from src.service import TaskService


def test_add_creates_task(tmp_path) -> None:
    service = TaskService(path=tmp_path / "tasks.json")
    task = service.add("Купить молоко", Priority.HIGH)
    assert task.id == 1
    assert task.priority is Priority.HIGH
    assert service.list() == [task]


def test_list_filters_by_status_and_priority(tmp_path) -> None:
    service = TaskService(path=tmp_path / "tasks.json")
    service.add("Задача A", Priority.LOW)
    service.add("Задача B", Priority.HIGH)
    service.add("Задача C", Priority.HIGH)

    high = service.list(priority=Priority.HIGH)
    assert [t.title for t in high] == ["Задача B", "Задача C"]

    service.mark_done(2)
    pending = service.list(status=Status.PENDING)
    assert [t.title for t in pending] == ["Задача A", "Задача C"]


def test_mark_done_changes_status(tmp_path) -> None:
    service = TaskService(path=tmp_path / "tasks.json")
    task = service.add("Прочитать книгу")
    service.mark_done(task.id)
    assert service.list()[0].status is Status.DONE


def test_mark_done_missing_returns_none(tmp_path) -> None:
    service = TaskService(path=tmp_path / "tasks.json")
    assert service.mark_done(999) is None


def test_remove_deletes_task(tmp_path) -> None:
    service = TaskService(path=tmp_path / "tasks.json")
    task = service.add("Убраться")
    assert service.remove(task.id) is True
    assert service.list() == []


def test_remove_missing_returns_false(tmp_path) -> None:
    service = TaskService(path=tmp_path / "tasks.json")
    assert service.remove(123) is False


def test_storage_persists_across_instances(tmp_path) -> None:
    path = tmp_path / "tasks.json"
    first = TaskService(path=path)
    first.add("Долгоживущая задача", Priority.HIGH)

    second = TaskService(path=path)
    assert [t.title for t in second.list()] == ["Долгоживущая задача"]