from __future__ import annotations

import json
import os
from functools import lru_cache
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_KB_DIR = PROJECT_ROOT / "knowledge_base"


class KnowledgeBaseError(RuntimeError):
    """Raised when the local knowledge base cannot be read."""


def resolve_kb_dir(kb_dir: str | Path | None = None) -> Path:
    """Resolve the knowledge base directory.

    Resolution order:
    1. Explicit ``kb_dir`` argument.
    2. ``XINGCE_KB_DIR`` environment variable.
    3. ``knowledge_base`` under the current working directory.
    4. ``knowledge_base`` under this repository root.
    """

    candidates: list[Path] = []
    if kb_dir is not None:
        candidates.append(Path(kb_dir))
    env_kb_dir = os.getenv("XINGCE_KB_DIR")
    if env_kb_dir:
        candidates.append(Path(env_kb_dir))
    candidates.extend([Path.cwd() / "knowledge_base", DEFAULT_KB_DIR])

    for candidate in candidates:
        resolved = candidate.expanduser().resolve()
        if resolved.exists():
            return resolved

    raise KnowledgeBaseError(
        "Knowledge base directory not found. Expected knowledge_base/ or XINGCE_KB_DIR."
    )


def _stringify(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, dict):
        return " ".join(f"{_stringify(k)} {_stringify(v)}" for k, v in value.items())
    if isinstance(value, list):
        return " ".join(_stringify(item) for item in value)
    return str(value)


def _weighted_text(card: dict[str, Any]) -> tuple[str, str]:
    high_weight_fields = [
        "id",
        "module",
        "question_type",
        "sub_type",
        "method_name",
        "aliases",
        "tags",
        "trigger_conditions",
    ]
    broad_fields = [
        "anti_conditions",
        "required_inputs",
        "steps",
        "formulas",
        "examples",
        "pitfalls",
        "forbidden",
        "output_constraints",
    ]
    high = " ".join(_stringify(card.get(field)) for field in high_weight_fields)
    broad = " ".join(_stringify(card.get(field)) for field in broad_fields)
    return high.lower(), f"{high} {broad}".lower()


def _query_terms(query: str) -> list[str]:
    terms = [term.strip().lower() for term in query.split() if term.strip()]
    return terms or [query.strip().lower()]


def _solver_rank(card: dict[str, Any]) -> int:
    priority = card.get("solver_priority")
    if isinstance(priority, dict):
        rank = priority.get("rank", 999)
        if isinstance(rank, int):
            return rank
    return 999


class KnowledgeBase:
    def __init__(self, kb_dir: str | Path | None = None) -> None:
        self.kb_dir = resolve_kb_dir(kb_dir)
        self.cards_path = self.kb_dir / "all_cards.jsonl"
        if not self.cards_path.exists():
            raise KnowledgeBaseError(f"Missing cards file: {self.cards_path}")
        self._cards: list[dict[str, Any]] | None = None
        self._card_index: dict[str, dict[str, Any]] | None = None

    @property
    def cards(self) -> list[dict[str, Any]]:
        if self._cards is None:
            self._cards = self._read_cards()
        return self._cards

    @property
    def card_index(self) -> dict[str, dict[str, Any]]:
        if self._card_index is None:
            self._card_index = {card["id"]: card for card in self.cards if "id" in card}
        return self._card_index

    def _read_cards(self) -> list[dict[str, Any]]:
        cards: list[dict[str, Any]] = []
        with self.cards_path.open("r", encoding="utf-8") as file:
            for line_number, line in enumerate(file, start=1):
                stripped = line.strip()
                if not stripped:
                    continue
                try:
                    card = json.loads(stripped)
                except json.JSONDecodeError as exc:
                    raise KnowledgeBaseError(
                        f"Invalid JSON in {self.cards_path} line {line_number}: {exc}"
                    ) from exc
                cards.append(card)
        return cards

    def get_method_card(self, method_id: str) -> dict[str, Any] | None:
        return self.card_index.get(method_id)

    def search_methods(
        self, query: str, module: str | None = None, top_k: int = 5
    ) -> list[dict[str, Any]]:
        return [match["card"] for match in self.search_method_matches(query, module, top_k)]

    def search_method_matches(
        self, query: str, module: str | None = None, top_k: int = 5
    ) -> list[dict[str, Any]]:
        if top_k <= 0:
            return []

        terms = _query_terms(query)
        scored: list[tuple[int, dict[str, Any]]] = []
        for card in self.cards:
            if module and card.get("module") != module:
                continue
            high_text, broad_text = _weighted_text(card)
            score = 0
            for term in terms:
                if not term:
                    continue
                score += high_text.count(term) * 5
                score += broad_text.count(term)
            if score > 0:
                scored.append((score, card))

        scored.sort(
            key=lambda item: (
                -item[0],
                item[1].get("module", ""),
                _solver_rank(item[1]),
                item[1].get("id", ""),
            )
        )
        return [{"score": score, "card": card} for score, card in scored[:top_k]]

    def get_source_reference(self, method_id: str) -> dict[str, Any] | None:
        card = self.get_method_card(method_id)
        if card is None:
            return None
        return {
            "id": card.get("id"),
            "method_name": card.get("method_name"),
            "module": card.get("module"),
            "question_type": card.get("question_type"),
            "sub_type": card.get("sub_type"),
            "source_file": card.get("source_file", []),
            "source_page": card.get("source_page", []),
            "source_zip": card.get("source_zip"),
            "confidence": card.get("confidence"),
            "need_review": card.get("need_review", False),
        }


@lru_cache(maxsize=4)
def _cached_kb(kb_dir: str | None = None) -> KnowledgeBase:
    return KnowledgeBase(kb_dir)


def load_cards(kb_dir: str | Path | None = None) -> list[dict[str, Any]]:
    return _cached_kb(str(kb_dir) if kb_dir else None).cards


def get_method_card(
    method_id: str, kb_dir: str | Path | None = None
) -> dict[str, Any] | None:
    return _cached_kb(str(kb_dir) if kb_dir else None).get_method_card(method_id)


def search_methods(
    query: str,
    module: str | None = None,
    top_k: int = 5,
    kb_dir: str | Path | None = None,
) -> list[dict[str, Any]]:
    return _cached_kb(str(kb_dir) if kb_dir else None).search_methods(query, module, top_k)


def search_method_matches(
    query: str,
    module: str | None = None,
    top_k: int = 5,
    kb_dir: str | Path | None = None,
) -> list[dict[str, Any]]:
    return _cached_kb(str(kb_dir) if kb_dir else None).search_method_matches(
        query, module, top_k
    )


def get_source_reference(
    method_id: str, kb_dir: str | Path | None = None
) -> dict[str, Any] | None:
    return _cached_kb(str(kb_dir) if kb_dir else None).get_source_reference(method_id)
