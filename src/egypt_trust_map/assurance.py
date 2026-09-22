"""Export benchmark reference runs using the shared assurance-result v1 contract."""

from __future__ import annotations

import hashlib
import json


def digest(value: dict) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def envelope(catalog: dict, result: dict) -> dict:
    artifact_hash = digest(result)
    failed = sorted(result["failed_gates"])
    return {
        "schema_version": "bpa.assurance-result.v1",
        "result_id": f"{catalog['catalog_id']}:{artifact_hash[:16]}",
        "producer": {
            "repository": "AAH20/egypt-digital-trust-map",
            "component": "reference-benchmark",
            "version": "0.3.0",
        },
        "run": {"kind": "synthetic-reference", "environment": "local-reference"},
        "subject": {
            "pack_id": catalog["catalog_id"],
            "pack_version": catalog["catalog_id"].rsplit("-", 1)[-1],
            "pack_sha256": digest(catalog),
        },
        "qualification": {
            "qualified": result["qualified"],
            "failed_gates": failed,
            "score": result["score"],
            "score_basis": "reference-fixture",
        },
        "evidence": {
            "artifact_sha256": artifact_hash,
            "receipt_root_sha256": None,
            "verification": "none",
        },
        "limitations": [
            "Score is computed from reference fixtures, not observed provider performance.",
            "No signed receipt chain or independent verification is provided.",
        ],
    }
