"""Kill switch simple basado en la existencia de un archivo."""

from __future__ import annotations

from pathlib import Path


class KillSwitch:
    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)

    @property
    def active(self) -> bool:
        return self.path.exists()

    def activate(self, reason: str = "") -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(reason or "activated", encoding="utf-8")

    def deactivate(self) -> None:
        self.path.unlink(missing_ok=True)
