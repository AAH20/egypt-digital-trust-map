"""Offline, human-reviewable changes to the public EG-CERT snapshot."""

from __future__ import annotations

from datetime import date

from .sovereignty import validate_provider_register


def freshness(snapshot: dict, today: date, max_age_days: int = 30) -> dict:
    if max_age_days < 0:
        raise ValueError("max_age_days must be non-negative")
    verified = date.fromisoformat(snapshot["last_verified"])
    age = (today - verified).days
    return {
        "source_url": snapshot["source_url"],
        "last_verified": verified.isoformat(),
        "checked_on": today.isoformat(),
        "age_days": age,
        "max_age_days": max_age_days,
        "status": "future-dated" if age < 0 else "stale" if age > max_age_days else "current",
        "scope": "snapshot recency only; accreditation scope requires live-source review",
    }


def review_candidate(current: dict, candidate: dict) -> dict:
    errors = validate_provider_register(current) + validate_provider_register(candidate)
    if candidate.get("source_url") != current.get("source_url"):
        errors.append("candidate source_url differs from the tracked authority")
    try:
        current_date = date.fromisoformat(current["last_verified"])
        candidate_date = date.fromisoformat(candidate["last_verified"])
        if candidate_date < current_date:
            errors.append("candidate last_verified is older than the tracked snapshot")
    except (KeyError, TypeError, ValueError):
        errors.append("both snapshots require ISO last_verified dates")
    if errors:
        return {"valid": False, "errors": errors}
    before = {entry["id"]: entry for entry in current["providers"]}
    after = {entry["id"]: entry for entry in candidate["providers"]}
    shared = before.keys() & after.keys()
    changes = {
        "added": [after[key] for key in sorted(after.keys() - before.keys())],
        "removed": [before[key] for key in sorted(before.keys() - after.keys())],
        "renamed": [
            {"id": key, "before": before[key]["name"], "after": after[key]["name"]}
            for key in sorted(shared)
            if before[key]["name"] != after[key]["name"]
        ],
        "renumbered": [
            {"id": key, "before": before[key]["registry_number"], "after": after[key]["registry_number"]}
            for key in sorted(shared)
            if before[key]["registry_number"] != after[key]["registry_number"]
        ],
    }
    return {
        "valid": True,
        "source_url": current["source_url"],
        "previous_verified": current["last_verified"],
        "candidate_verified": candidate["last_verified"],
        "previous_count": len(before),
        "candidate_count": len(after),
        "changes": changes,
        "requires_human_review": any(changes.values()),
        "scope": "identity and ordering only; authorized services are not inferred",
    }
