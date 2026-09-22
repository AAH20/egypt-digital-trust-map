from __future__ import annotations

import json
from collections import Counter
from datetime import date
from pathlib import Path
from urllib.parse import urlparse


ALLOWED_SOURCE_STATUS = {
    "authoritative",
    "authoritative-listing",
    "authoritative-listing-and-first-party-claim",
    "first-party-claim",
    "independently-tested",
}


def load_registry(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_registry(document: dict) -> list[str]:
    errors: list[str] = []
    players = document.get("players")
    if not isinstance(players, list) or not players:
        return ["players must be a non-empty array"]

    ids = [player.get("id") for player in players]
    duplicates = sorted(key for key, count in Counter(ids).items() if count > 1)
    if duplicates:
        errors.append(f"duplicate player ids: {', '.join(duplicates)}")

    required = {"id", "name", "player_types", "capabilities", "source_status", "sources", "last_verified"}
    for index, player in enumerate(players):
        prefix = f"players[{index}]"
        missing = sorted(required - set(player))
        if missing:
            errors.append(f"{prefix} missing: {', '.join(missing)}")
            continue
        if player["source_status"] not in ALLOWED_SOURCE_STATUS:
            errors.append(f"{prefix}.source_status is invalid")
        for field in ("player_types", "capabilities", "sources"):
            value = player[field]
            if not isinstance(value, list) or not value or len(value) != len(set(value)):
                errors.append(f"{prefix}.{field} must be a non-empty unique array")
        for source in player["sources"]:
            parsed = urlparse(source)
            if parsed.scheme != "https" or not parsed.netloc:
                errors.append(f"{prefix}.sources contains a non-HTTPS URL")
        try:
            verified = date.fromisoformat(player["last_verified"])
            if verified > date.today():
                errors.append(f"{prefix}.last_verified is in the future")
        except (TypeError, ValueError):
            errors.append(f"{prefix}.last_verified is not ISO-8601")
    return errors


def summarize(document: dict) -> dict:
    players = document["players"]
    type_counts = Counter(kind for player in players for kind in player["player_types"])
    capability_counts = Counter(capability for player in players for capability in player["capabilities"])
    return {
        "coverage_status": document.get("coverage_status", "unknown"),
        "players": len(players),
        "player_types": dict(sorted(type_counts.items())),
        "capabilities": dict(sorted(capability_counts.items())),
    }
