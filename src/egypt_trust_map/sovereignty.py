from __future__ import annotations

import json
from pathlib import Path


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_profile(profile: dict) -> list[str]:
    errors: list[str] = []
    dimensions = profile.get("dimensions", [])
    hard_gates = profile.get("hard_gates", [])
    dimension_ids = [item.get("id") for item in dimensions]
    if not profile.get("profile_id"):
        errors.append("profile_id is required")
    if not dimensions or len(dimension_ids) != len(set(dimension_ids)):
        errors.append("dimensions must be non-empty with unique ids")
    if sum(item.get("weight", 0) for item in dimensions) != 100:
        errors.append("dimension weights must total 100")
    if not hard_gates or len(hard_gates) != len(set(hard_gates)):
        errors.append("hard_gates must be non-empty and unique")
    threshold = profile.get("score_threshold")
    if not isinstance(threshold, int) or not 0 <= threshold <= 100:
        errors.append("score_threshold must be an integer from 0 to 100")
    return errors


def assess(profile: dict, submission: dict) -> dict:
    profile_errors = validate_profile(profile)
    if profile_errors:
        raise ValueError("; ".join(profile_errors))

    dimensions = {item["id"]: item["weight"] for item in profile["dimensions"]}
    submitted_scores = submission.get("scores", {})
    submitted_gates = submission.get("gates", {})
    errors: list[str] = []

    missing_dimensions = sorted(set(dimensions) - set(submitted_scores))
    extra_dimensions = sorted(set(submitted_scores) - set(dimensions))
    if missing_dimensions:
        errors.append(f"missing dimensions: {', '.join(missing_dimensions)}")
    if extra_dimensions:
        errors.append(f"unknown dimensions: {', '.join(extra_dimensions)}")

    for dimension_id, maximum in dimensions.items():
        value = submitted_scores.get(dimension_id)
        if not isinstance(value, (int, float)) or isinstance(value, bool) or not 0 <= value <= maximum:
            errors.append(f"{dimension_id} must be between 0 and {maximum}")

    missing_gates = sorted(set(profile["hard_gates"]) - set(submitted_gates))
    extra_gates = sorted(set(submitted_gates) - set(profile["hard_gates"]))
    if missing_gates:
        errors.append(f"missing gates: {', '.join(missing_gates)}")
    if extra_gates:
        errors.append(f"unknown gates: {', '.join(extra_gates)}")
    for gate in profile["hard_gates"]:
        if gate in submitted_gates and not isinstance(submitted_gates[gate], bool):
            errors.append(f"{gate} must be boolean")

    if errors:
        return {"valid": False, "qualified": False, "score": None, "errors": errors}

    score = round(float(sum(submitted_scores.values())), 2)
    failed_gates = sorted(gate for gate in profile["hard_gates"] if not submitted_gates[gate])
    qualified = not failed_gates and score >= profile["score_threshold"]
    return {
        "valid": True,
        "assessment_id": submission.get("assessment_id"),
        "profile_id": profile["profile_id"],
        "score": score,
        "threshold": profile["score_threshold"],
        "failed_gates": failed_gates,
        "qualified": qualified,
        "decision": "QUALIFIED" if qualified else "NOT_QUALIFIED",
    }


def validate_provider_register(document: dict) -> list[str]:
    errors: list[str] = []
    providers = document.get("providers")
    if not isinstance(providers, list) or not providers:
        return ["providers must be a non-empty array"]
    numbers = [provider.get("registry_number") for provider in providers]
    ids = [provider.get("id") for provider in providers]
    if len(numbers) != len(set(numbers)):
        errors.append("registry numbers must be unique")
    if len(ids) != len(set(ids)):
        errors.append("provider ids must be unique")
    if numbers != list(range(1, len(providers) + 1)):
        errors.append("registry numbers must be contiguous from 1")
    if document.get("snapshot_count") != len(providers):
        errors.append("snapshot_count must match provider count")
    for index, provider in enumerate(providers):
        if not provider.get("id") or not provider.get("name"):
            errors.append(f"providers[{index}] requires id and name")
    return errors
