"""Слой хранения задач в JSON-файле."""

from __future__ import annotations

import json
from pathlib import Path


class Storage:
    """Чтение и запись списка задач в JSON-файле."""

    def __init__(self, path: str | Path = "tasks.json") -> None:
        self.path = Path(path)

    def load(self) -> list[dict]:
        """Загрузка задач из файла; отсутствующий файл даёт пустой список."""
        if not self.path.exists():
            return []
        with self.path.open("r", encoding="utf-8") as fh:
            return json.load(fh)

    def save(self, data: list[dict]) -> None:
        """Сохранение задач в файл (создаёт каталоги при необходимости)."""
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("w", encoding="utf-8") as fh:
            json.dump(data, fh, ensure_ascii=False, indent=2)