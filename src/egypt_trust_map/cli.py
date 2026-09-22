from __future__ import annotations

import argparse
import json
from pathlib import Path

from .registry import load_registry, summarize, validate_registry


def default_registry() -> Path:
    return Path(__file__).resolve().parents[2] / "registry" / "players.json"


def main() -> int:
    parser = argparse.ArgumentParser(prog="egypt-trust-map")
    parser.add_argument("command", choices=("verify", "summary"))
    parser.add_argument("--registry", type=Path, default=default_registry())
    args = parser.parse_args()
    document = load_registry(args.registry)
    errors = validate_registry(document)
    if errors:
        print(json.dumps({"valid": False, "errors": errors}, indent=2))
        return 1
    if args.command == "verify":
        print(json.dumps({"valid": True, "players": len(document["players"])}, indent=2))
    else:
        print(json.dumps(summarize(document), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
