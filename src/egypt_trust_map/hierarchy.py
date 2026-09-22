from __future__ import annotations

from collections import Counter


PROHIBITED_PUBLIC_KEYS = {
    "person_name",
    "email",
    "phone",
    "username",
    "password",
    "credential",
    "private_key",
    "recovery_share",
    "endpoint",
    "ip_address",
    "biometric_template",
    "watchlist",
}


def _walk_keys(value: object) -> set[str]:
    keys: set[str] = set()
    if isinstance(value, dict):
        for key, child in value.items():
            keys.add(key.lower())
            keys.update(_walk_keys(child))
    elif isinstance(value, list):
        for child in value:
            keys.update(_walk_keys(child))
    return keys


def validate_hierarchy(model: dict) -> list[str]:
    errors: list[str] = []
    tiers = model.get("tiers")
    nodes = model.get("nodes")
    if not isinstance(tiers, list) or not tiers:
        errors.append("tiers must be a non-empty array")
        return errors
    if not isinstance(nodes, list) or not nodes:
        errors.append("nodes must be a non-empty array")
        return errors

    levels = [tier.get("level") for tier in tiers]
    if levels != list(range(len(tiers))):
        errors.append("tier levels must be contiguous from zero")
    tier_levels = set(levels)
    tier_ids = [tier.get("id") for tier in tiers]
    if any(not tier_id for tier_id in tier_ids) or len(tier_ids) != len(set(tier_ids)):
        errors.append("tier ids must be present and unique")
    node_ids = [node.get("id") for node in nodes]
    duplicates = sorted(key for key, count in Counter(node_ids).items() if count > 1)
    if duplicates:
        errors.append(f"duplicate node ids: {', '.join(duplicates)}")
    node_by_id = {node.get("id"): node for node in nodes}

    roots = []
    for index, node in enumerate(nodes):
        prefix = f"nodes[{index}]"
        if node.get("tier") not in tier_levels:
            errors.append(f"{prefix}.tier is unknown")
        parent_id = node.get("parent")
        if parent_id is None:
            roots.append(node)
        elif parent_id not in node_by_id:
            errors.append(f"{prefix}.parent is unknown")
        else:
            parent = node_by_id[parent_id]
            if parent.get("tier", -1) >= node.get("tier", -1):
                errors.append(f"{prefix}.parent must be in a higher tier")
        if not node.get("node_type") or not isinstance(node.get("public_outputs"), list):
            errors.append(f"{prefix} requires node_type and public_outputs")

    if len(roots) != 1 or roots[0].get("tier") != 0:
        errors.append("model must contain exactly one tier-zero root")

    compartments = model.get("compartments")
    if not isinstance(compartments, list) or not compartments:
        errors.append("compartments must be a non-empty array")
    else:
        compartment_ids = [compartment.get("id") for compartment in compartments]
        if any(not value for value in compartment_ids) or len(compartment_ids) != len(set(compartment_ids)):
            errors.append("compartment ids must be present and unique")
    if not isinstance(model.get("information_rules"), list) or not model["information_rules"]:
        errors.append("information_rules must be a non-empty array")

    prohibited = sorted(_walk_keys(model) & PROHIBITED_PUBLIC_KEYS)
    if prohibited:
        errors.append(f"public model contains prohibited fields: {', '.join(prohibited)}")
    return errors


def summarize_hierarchy(model: dict) -> dict:
    return {
        "model_id": model["model_id"],
        "tiers": len(model["tiers"]),
        "nodes": len(model["nodes"]),
        "compartments": len(model.get("compartments", [])),
        "information_rules": len(model.get("information_rules", [])),
    }
