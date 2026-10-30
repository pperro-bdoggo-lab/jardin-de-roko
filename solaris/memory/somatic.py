"""Memoria somática: similitud semántica simple + resonancia afectiva."""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from solaris.schemas import AffectState, MemoryItem, MemoryKind

_WORD_RE = re.compile(r"[^\W\d_]+", re.UNICODE)


def _tokens(text: str) -> set[str]:
    return {word.lower() for word in _WORD_RE.findall(text)}


@dataclass
class SomaticMemory:
    items: list[MemoryItem] = field(default_factory=list)

    def write(self, text: str, affect: float = 0.0) -> MemoryItem:
        item = MemoryItem(text=text, kind=MemoryKind.SOMATIC, affect=affect)
        self.items.append(item)
        return item

    def retrieve(
        self, query: str, affect: AffectState, limit: int = 5
    ) -> list[MemoryItem]:
        query_tokens = _tokens(query)
        scored: list[MemoryItem] = []
        for item in self.items:
            item_tokens = _tokens(item.text)
            union = query_tokens | item_tokens
            semantic = len(query_tokens & item_tokens) / len(union) if union else 0.0
            resonance = 1.0 - min(1.0, abs(item.affect - affect.valence))
            score = round(0.7 * semantic + 0.3 * resonance, 4)
            scored.append(
                MemoryItem(
                    text=item.text,
                    kind=item.kind,
                    affect=item.affect,
                    score=score,
                    item_id=item.item_id,
                    created_at=item.created_at,
                )
            )
        scored.sort(key=lambda candidate: candidate.score, reverse=True)
        return [item for item in scored[:limit] if item.score > 0.0]
