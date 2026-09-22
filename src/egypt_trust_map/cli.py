from __future__ import annotations

import argparse
import json
from pathlib import Path

from .benchmarks import (
    evaluate,
    reference_observations,
    validate_catalog,
    validate_kpi_baseline,
    validate_market_registry,
    validate_technology_targets,
)
from .hierarchy import summarize_hierarchy, validate_hierarchy
from .registry import load_registry, summarize, validate_registry
from .sovereignty import assess, load_json, validate_profile, validate_provider_register


def default_registry() -> Path:
    return Path(__file__).resolve().parents[2] / "registry" / "players.json"


def main() -> int:
    parser = argparse.ArgumentParser(prog="egypt-trust-map")
    parser.add_argument(
        "command",
        choices=("verify", "summary", "assess-sovereignty", "verify-hierarchy", "benchmark"),
    )
    parser.add_argument("--registry", type=Path, default=default_registry())
    parser.add_argument("--profile", type=Path, default=Path(__file__).resolve().parents[2] / "sovereignty" / "requirements.json")
    parser.add_argument("--assessment", type=Path, default=Path(__file__).resolve().parents[2] / "sovereignty" / "reference-assessment.json")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]

    if args.command == "assess-sovereignty":
        result = assess(load_json(args.profile), load_json(args.assessment))
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0 if result["qualified"] else 1

    if args.command == "verify-hierarchy":
        hierarchy = load_json(root / "hierarchy" / "reference-hierarchy.json")
        errors = validate_hierarchy(hierarchy)
        result = {"valid": not errors, **summarize_hierarchy(hierarchy), "errors": errors}
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0 if not errors else 1

    if args.command == "benchmark":
        catalog = load_json(root / "benchmarks" / "catalog.json")
        result = evaluate(catalog, reference_observations(catalog))
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0 if result["qualified"] else 1

    document = load_registry(args.registry)
    errors = validate_registry(document)
    errors.extend(validate_profile(load_json(root / "sovereignty" / "requirements.json")))
    errors.extend(validate_provider_register(load_json(root / "registry" / "egcert-accredited-providers.json")))
    errors.extend(validate_market_registry(load_json(root / "registry" / "sector-ecosystem.json")))
    errors.extend(validate_technology_targets(load_json(root / "registry" / "technology-integration-targets.json")))
    errors.extend(validate_hierarchy(load_json(root / "hierarchy" / "reference-hierarchy.json")))
    errors.extend(validate_catalog(load_json(root / "benchmarks" / "catalog.json")))
    errors.extend(validate_kpi_baseline(load_json(root / "benchmarks" / "kpis.json")))
    if errors:
        print(json.dumps({"valid": False, "errors": errors}, indent=2))
        return 1
    if args.command == "verify":
        provider_count = len(load_json(root / "registry" / "egcert-accredited-providers.json")["providers"])
        market_records = sum(len(group["records"]) for group in load_json(root / "registry" / "sector-ecosystem.json")["groups"])
        technology_targets = len(load_json(root / "registry" / "technology-integration-targets.json")["targets"])
        benchmark_count = len(load_json(root / "benchmarks" / "catalog.json")["scenarios"])
        kpi_count = len(load_json(root / "benchmarks" / "kpis.json")["kpis"])
        print(
            json.dumps(
                {
                    "valid": True,
                    "core_players": len(document["players"]),
                    "egcert_providers": provider_count,
                    "sector_records": market_records,
                    "technology_targets": technology_targets,
                    "benchmarks": benchmark_count,
                    "kpis": kpi_count,
                },
                indent=2,
            )
        )
    else:
        print(json.dumps(summarize(document), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
