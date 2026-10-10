"""Бизнес-логика управления задачами."""

from __future__ import annotations

from .models import Priority, Status, Task
from .storage import Storage


class TaskService:
    """Операции над задачами: добавление, просмотр, изменение, удаление."""

    def __init__(self, path: str = "tasks.json") -> None:
        self._storage = Storage(path)
        self._tasks: list[Task] = [Task.from_dict(row) for row in self._storage.load()]

    def _next_id(self) -> int:
        return max((task.id or 0 for task in self._tasks), default=0) + 1

    def _persist(self) -> None:
        self._storage.save([task.to_dict() for task in self._tasks])

    def add(self, title: str, priority: Priority = Priority.MEDIUM) -> Task:
        """Создаёт новую задачу и сохраняет её."""
        task = Task(title=title, priority=priority, id=self._next_id())
        self._tasks.append(task)
        self._persist()
        return task

    def list(
        self,
        status: Status | None = None,
        priority: Priority | None = None,
    ) -> list[Task]:
        """Возвращает задачи с опциональной фильтрацией по статусу и приоритету."""
        tasks = self._tasks
        if status is not None:
            tasks = [task for task in tasks if task.status is status]
        if priority is not None:
            tasks = [task for task in tasks if task.priority is priority]
        return tasks

    def mark_done(self, task_id: int) -> Task | None:
        """Помечает задачу выполненной; возвращает её или None, если не найдена."""
        for task in self._tasks:
            if task.id == task_id:
                task.status = Status.DONE
                self._persist()
                return task
        return None

    def remove(self, task_id: int) -> bool:
        """Удаляет задачу; возвращает True, если задача существовала."""
        before = len(self._tasks)
        self._tasks = [task for task in self._tasks if task.id != task_id]
        if len(self._tasks) != before:
            self._persist()
            return True
        return False