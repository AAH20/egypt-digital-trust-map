from __future__ import annotations

from collections import Counter
from datetime import date
from urllib.parse import urlparse


def _is_iso_date(value: object) -> bool:
    try:
        date.fromisoformat(str(value))
        return True
    except ValueError:
        return False


def validate_catalog(catalog: dict) -> list[str]:
    errors: list[str] = []
    scenarios = catalog.get("scenarios")
    if not catalog.get("catalog_id"):
        errors.append("catalog_id is required")
    threshold = catalog.get("score_threshold")
    if not isinstance(threshold, (int, float)) or isinstance(threshold, bool) or not 0 <= threshold <= 100:
        errors.append("score_threshold must be between 0 and 100")
    if not isinstance(scenarios, list) or not scenarios:
        return errors + ["scenarios must be a non-empty array"]
    ids = [scenario.get("id") for scenario in scenarios]
    duplicates = sorted(key for key, count in Counter(ids).items() if count > 1)
    if duplicates:
        errors.append(f"duplicate scenario ids: {', '.join(duplicates)}")
    optional_weight = 0
    for index, scenario in enumerate(scenarios):
        prefix = f"scenarios[{index}]"
        required = {"id", "family", "mandatory", "expected", "weight", "test", "evidence"}
        missing = sorted(required - set(scenario))
        if missing:
            errors.append(f"{prefix} missing: {', '.join(missing)}")
            continue
        if scenario["mandatory"] and scenario["weight"] != 0:
            errors.append(f"{prefix} mandatory gate weight must be zero")
        if not scenario["mandatory"]:
            if not isinstance(scenario["weight"], (int, float)) or isinstance(scenario["weight"], bool) or scenario["weight"] <= 0:
                errors.append(f"{prefix} optional metric weight must be positive")
                continue
            optional_weight += scenario["weight"]
        if not scenario["evidence"] or len(scenario["evidence"]) != len(set(scenario["evidence"])):
            errors.append(f"{prefix}.evidence must be non-empty and unique")
    if optional_weight != 100:
        errors.append("optional metric weights must total 100")
    return errors


def validate_kpi_baseline(baseline: dict) -> list[str]:
    errors: list[str] = []
    if not baseline.get("baseline_id") or baseline.get("status") != "reference-baseline" or not baseline.get("scope"):
        errors.append("baseline_id, reference-baseline status and scope are required")
    kpis = baseline.get("kpis")
    if not isinstance(kpis, list) or not kpis:
        return errors + ["kpis must be a non-empty array"]
    ids = [kpi.get("id") for kpi in kpis]
    duplicates = sorted(key for key, count in Counter(ids).items() if count > 1)
    if duplicates:
        errors.append(f"duplicate KPI ids: {', '.join(duplicates)}")
    for index, kpi in enumerate(kpis):
        required = {"id", "family", "name", "operator", "target", "unit", "measurement"}
        missing = sorted(required - set(kpi))
        if missing:
            errors.append(f"kpis[{index}] missing: {', '.join(missing)}")
            continue
        if kpi["operator"] not in {"eq", "lte", "gte"}:
            errors.append(f"kpis[{index}].operator is invalid")
        if not isinstance(kpi["target"], (int, float)) or isinstance(kpi["target"], bool):
            errors.append(f"kpis[{index}].target must be numeric")
    return errors


def reference_observations(catalog: dict) -> dict:
    return {scenario["id"]: scenario["expected"] for scenario in catalog["scenarios"]}


def evaluate(catalog: dict, observations: dict[str, str], metric_scores: dict[str, float] | None = None) -> dict:
    errors = validate_catalog(catalog)
    if errors:
        raise ValueError("; ".join(errors))
    metric_scores = metric_scores or {}
    results = []
    failed_gates = []
    weighted_score = 0.0
    for scenario in catalog["scenarios"]:
        observed = observations.get(scenario["id"], "missing")
        passed = observed == scenario["expected"]
        if scenario["mandatory"] and not passed:
            failed_gates.append(scenario["id"])
        if not scenario["mandatory"]:
            raw_score = metric_scores.get(scenario["id"], 100.0 if passed else 0.0)
            if not isinstance(raw_score, (int, float)) or isinstance(raw_score, bool) or not 0 <= raw_score <= 100:
                raise ValueError(f"metric score for {scenario['id']} must be between 0 and 100")
            weighted_score += raw_score * scenario["weight"] / 100
        results.append({"scenario_id": scenario["id"], "family": scenario["family"], "observed": observed, "passed": passed})
    score = round(weighted_score, 2)
    qualified = not failed_gates and score >= catalog["score_threshold"]
    return {
        "catalog_id": catalog["catalog_id"],
        "scenario_count": len(catalog["scenarios"]),
        "failed_gates": sorted(failed_gates),
        "score": score,
        "threshold": catalog["score_threshold"],
        "qualified": qualified,
        "decision": "QUALIFIED" if qualified else "NOT_QUALIFIED",
        "results": results,
    }


def validate_market_registry(document: dict) -> list[str]:
    errors: list[str] = []
    if not document.get("registry_id") or not document.get("coverage_note"):
        errors.append("registry_id and coverage_note are required")
    if not _is_iso_date(document.get("last_verified")):
        errors.append("last_verified must be an ISO date")
    sources = document.get("sources")
    if not isinstance(sources, list) or not sources:
        errors.append("sources must be a non-empty array")
        sources = []
    source_ids = [source.get("id") for source in sources]
    if len(source_ids) != len(set(source_ids)):
        errors.append("source ids must be unique")
    for index, source in enumerate(sources):
        if not all(source.get(key) for key in ("id", "url", "scope")):
            errors.append(f"sources[{index}] is incomplete")
        elif urlparse(source["url"]).scheme != "https":
            errors.append(f"sources[{index}].url must use HTTPS")
    groups = document.get("groups")
    if not isinstance(groups, list) or not groups:
        return ["groups must be a non-empty array"]
    all_ids: list[str] = []
    for group_index, group in enumerate(groups):
        records = group.get("records")
        if not group.get("id") or not isinstance(records, list) or not records:
            errors.append(f"groups[{group_index}] requires id and non-empty records")
            continue
        if group.get("source_id") and group["source_id"] not in source_ids:
            errors.append(f"groups[{group_index}].source_id is unknown")
        for record_index, record in enumerate(records):
            all_ids.append(record.get("id"))
            if not all(record.get(key) for key in ("id", "name", "role", "evidence_state")):
                errors.append(f"groups[{group_index}].records[{record_index}] is incomplete")
    duplicates = sorted(key for key, count in Counter(all_ids).items() if count > 1)
    if duplicates:
        errors.append(f"duplicate market ids: {', '.join(duplicates)}")
    return errors


def validate_technology_targets(document: dict) -> list[str]:
    errors: list[str] = []
    if not document.get("registry_id") or not document.get("coverage_note"):
        errors.append("registry_id and coverage_note are required")
    targets = document.get("targets")
    if not isinstance(targets, list) or not targets:
        return ["targets must be a non-empty array"]
    ids = [target.get("id") for target in targets]
    if len(ids) != len(set(ids)):
        errors.append("technology target ids must be unique")
    for index, target in enumerate(targets):
        if not all(target.get(key) for key in ("id", "name", "domains", "classification", "validation_state")):
            errors.append(f"targets[{index}] is incomplete")
        elif not isinstance(target["domains"], list) or len(target["domains"]) != len(set(target["domains"])):
            errors.append(f"targets[{index}].domains must be a non-empty unique array")
    return errors
