"""Memoria episódica en memoria con persistencia JSONL opcional."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

from solaris.schemas import MemoryItem, MemoryKind


@dataclass
class EpisodicMemory:
    path: Path | None = None
    items: list[MemoryItem] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.path and self.path.exists():
            self._load()

    def _load(self) -> None:
        assert self.path is not None
        with self.path.open("r", encoding="utf-8") as handle:
            for line in handle:
                raw = line.strip()
                if raw:
                    data = json.loads(raw)
                    self.items.append(
                        MemoryItem(
                            text=data["text"],
                            kind=MemoryKind(data.get("kind", "episodic")),
                            affect=float(data.get("affect", 0.0)),
                            score=float(data.get("score", 0.0)),
                            item_id=data["item_id"],
                            created_at=data["created_at"],
                        )
                    )

    def write(self, text: str, affect: float = 0.0) -> MemoryItem:
        item = MemoryItem(text=text, kind=MemoryKind.EPISODIC, affect=affect)
        self.items.append(item)
        if self.path:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            with self.path.open("a", encoding="utf-8") as handle:
                handle.write(item.to_json(indent=None).replace("\n", "") + "\n")
        return item

    def retrieve(self, query: str, limit: int = 5) -> list[MemoryItem]:
        lowered = query.lower()
        return [item for item in self.items if lowered in item.text.lower()][:limit]
