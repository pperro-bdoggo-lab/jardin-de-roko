"""Audit log JSONL con cadena de hashes para detectar manipulación."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from solaris.schemas import AuditEvent, to_dict

GENESIS = "GENESIS"


class AuditLog:
    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)

    def _last_hash(self) -> str:
        if not self.path.exists():
            return GENESIS
        last = GENESIS
        with self.path.open("r", encoding="utf-8") as handle:
            for line in handle:
                line = line.strip()
                if line:
                    last = json.loads(line).get("hash", GENESIS)
        return last

    @staticmethod
    def _compute_hash(event: AuditEvent) -> str:
        payload = {
            "event_id": event.event_id,
            "timestamp": event.timestamp,
            "kind": event.kind,
            "payload": to_dict(event.payload),
            "prev_hash": event.prev_hash,
        }
        canonical = json.dumps(
            payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")
        )
        return hashlib.sha256(canonical.encode("utf-8")).hexdigest()

    def append(self, kind: str, payload: dict[str, Any]) -> AuditEvent:
        event = AuditEvent(kind=kind, payload=payload, prev_hash=self._last_hash())
        event.hash = self._compute_hash(event)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(event.to_json(indent=None).replace("\n", "") + "\n")
        return event

    def read_all(self) -> list[dict[str, Any]]:
        if not self.path.exists():
            return []
        events: list[dict[str, Any]] = []
        with self.path.open("r", encoding="utf-8") as handle:
            for line in handle:
                line = line.strip()
                if line:
                    events.append(json.loads(line))
        return events

    def verify(self) -> bool:
        prev = GENESIS
        for raw in self.read_all():
            try:
                event = AuditEvent(
                    kind=raw["kind"],
                    payload=raw["payload"],
                    event_id=raw["event_id"],
                    timestamp=raw["timestamp"],
                    prev_hash=raw.get("prev_hash", GENESIS),
                    hash=raw.get("hash", ""),
                )
            except (KeyError, TypeError):
                return False
            if event.prev_hash != prev:
                return False
            if event.hash != self._compute_hash(event):
                return False
            prev = event.hash
        return True
