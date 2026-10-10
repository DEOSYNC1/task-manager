"""Модель данных задачи."""

from __future__ import annotations

import datetime as dt
from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class Priority(Enum):
    """Приоритет задачи."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Status(Enum):
    """Статус выполнения задачи."""

    PENDING = "pending"
    DONE = "done"


@dataclass
class Task:
    """Задача с идентификатором, текстом, приоритетом и статусом."""

    title: str
    priority: Priority = Priority.MEDIUM
    status: Status = Status.PENDING
    created_at: str = field(
        default_factory=lambda: dt.datetime.now().isoformat(timespec="seconds")
    )
    id: int | None = None

    def to_dict(self) -> dict[str, Any]:
        """Сериализация задачи в словарь для JSON-хранилища."""
        return {
            "id": self.id,
            "title": self.title,
            "priority": self.priority.value,
            "status": self.status.value,
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Task":
        """Создание задачи из словаря JSON-хранилища."""
        return cls(
            id=data.get("id"),
            title=data["title"],
            priority=Priority(data.get("priority", Priority.MEDIUM.value)),
            status=Status(data.get("status", Status.PENDING.value)),
            created_at=data.get("created_at", ""),
        )