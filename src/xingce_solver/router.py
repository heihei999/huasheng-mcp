from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any

from .kb import KnowledgeBaseError, resolve_kb_dir


ROUTE_LIST_FIELDS = {
    "stem_triggers",
    "option_features",
    "negative_triggers",
    "backup_method_ids",
}

ROUTE_SCALAR_FIELDS = {
    "route_id",
    "module",
    "question_type",
    "sub_type",
    "priority_method_id",
}


def _strip_yaml_scalar(value: str) -> str:
    value = value.strip()
    if not value:
        return ""
    if value[0:1] in {"'", '"'} and value[-1:] == value[0]:
        return value[1:-1]
    if " #" in value:
        return value.split(" #", 1)[0].strip()
    return value


def _parse_routes_yaml(path: Path) -> list[dict[str, Any]]:
    """Parse the subset of YAML needed for first-phase route matching.

    The project intentionally avoids a runtime dependency here. The knowledge
    base's router file is generated with a regular structure, and phase 1 only
    needs route ids, module names, trigger lists, and priority method ids.
    """

    routes: list[dict[str, Any]] = []
    current: dict[str, Any] | None = None
    current_list: str | None = None

    with path.open("r", encoding="utf-8") as file:
        for raw_line in file:
            if not raw_line.strip() or raw_line.lstrip().startswith("#"):
                continue

            stripped = raw_line.strip()
            if stripped.startswith("- route_id:"):
                if current:
                    routes.append(current)
                current = {
                    "route_id": _strip_yaml_scalar(stripped.split(":", 1)[1]),
                    "stem_triggers": [],
                    "option_features": [],
                    "negative_triggers": [],
                    "backup_method_ids": [],
                }
                current_list = None
                continue

            if current is None:
                continue

            indent = len(raw_line) - len(raw_line.lstrip(" "))
            if indent == 2 and ":" in stripped and not stripped.startswith("- "):
                key, value = stripped.split(":", 1)
                if key in ROUTE_LIST_FIELDS:
                    current.setdefault(key, [])
                    current_list = key
                elif key in ROUTE_SCALAR_FIELDS:
                    current[key] = _strip_yaml_scalar(value)
                    current_list = None
                else:
                    current_list = None
                continue

            if current_list and indent == 2 and stripped.startswith("- "):
                current[current_list].append(_strip_yaml_scalar(stripped[2:]))

    if current:
        routes.append(current)
    return routes


@lru_cache(maxsize=4)
def load_routes(kb_dir: str | Path | None = None) -> list[dict[str, Any]]:
    resolved = resolve_kb_dir(kb_dir)
    routes_path = resolved / "global_router_rules.yaml"
    if not routes_path.exists():
        raise KnowledgeBaseError(f"Missing router rules file: {routes_path}")
    return _parse_routes_yaml(routes_path)


def _route_score(route: dict[str, Any], question_text: str) -> tuple[int, list[str]]:
    negative_hits = [
        trigger
        for trigger in route.get("negative_triggers", [])
        if trigger and trigger in question_text
    ]
    if negative_hits:
        return 0, []

    triggers = list(route.get("stem_triggers", [])) + list(route.get("option_features", []))
    matched = [trigger for trigger in triggers if trigger and trigger in question_text]
    if not matched:
        return 0, []

    max_trigger_length = max(len(trigger) for trigger in matched)
    score = max_trigger_length * 20 + sum(len(trigger) for trigger in matched) + len(matched)
    return score, matched


def classify_question(
    question_text: str,
    kb_dir: str | Path | None = None,
    top_k: int = 5,
) -> list[dict[str, Any]]:
    """Return preliminary route matches for a question.

    This is a lightweight keyword router, not a full solver. Results are sorted
    by trigger-match strength and include the target module and method id.
    """

    matches: list[dict[str, Any]] = []
    for route in load_routes(kb_dir):
        score, matched_triggers = _route_score(route, question_text)
        if score <= 0:
            continue
        matches.append(
            {
                "module": route.get("module"),
                "question_type": route.get("question_type"),
                "sub_type": route.get("sub_type"),
                "route_id": route.get("route_id"),
                "priority_method_id": route.get("priority_method_id"),
                "backup_method_ids": route.get("backup_method_ids", []),
                "matched_triggers": matched_triggers,
                "score": score,
            }
        )

    matches.sort(
        key=lambda item: (
            -item["score"],
            item.get("module") or "",
            item.get("question_type") or "",
            item.get("route_id") or "",
        )
    )
    return matches[:top_k]
