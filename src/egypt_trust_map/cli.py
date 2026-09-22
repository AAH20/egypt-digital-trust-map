from __future__ import annotations

import argparse
import json
from pathlib import Path

from .registry import load_registry, summarize, validate_registry
from .sovereignty import assess, load_json, validate_profile, validate_provider_register


def default_registry() -> Path:
    return Path(__file__).resolve().parents[2] / "registry" / "players.json"


def main() -> int:
    parser = argparse.ArgumentParser(prog="egypt-trust-map")
    parser.add_argument("command", choices=("verify", "summary", "assess-sovereignty"))
    parser.add_argument("--registry", type=Path, default=default_registry())
    parser.add_argument("--profile", type=Path, default=Path(__file__).resolve().parents[2] / "sovereignty" / "requirements.json")
    parser.add_argument("--assessment", type=Path, default=Path(__file__).resolve().parents[2] / "sovereignty" / "reference-assessment.json")
    args = parser.parse_args()

    if args.command == "assess-sovereignty":
        result = assess(load_json(args.profile), load_json(args.assessment))
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0 if result["qualified"] else 1

    document = load_registry(args.registry)
    errors = validate_registry(document)
    root = Path(__file__).resolve().parents[2]
    errors.extend(validate_profile(load_json(root / "sovereignty" / "requirements.json")))
    errors.extend(validate_provider_register(load_json(root / "registry" / "egcert-accredited-providers.json")))
    if errors:
        print(json.dumps({"valid": False, "errors": errors}, indent=2))
        return 1
    if args.command == "verify":
        provider_count = len(load_json(root / "registry" / "egcert-accredited-providers.json")["providers"])
        print(json.dumps({"valid": True, "core_players": len(document["players"]), "egcert_providers": provider_count}, indent=2))
    else:
        print(json.dumps(summarize(document), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
