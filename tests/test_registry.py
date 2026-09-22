import json
import unittest
from pathlib import Path

from egypt_trust_map.benchmarks import (
    evaluate,
    reference_observations,
    validate_catalog,
    validate_kpi_baseline,
    validate_market_registry,
    validate_technology_targets,
)
from egypt_trust_map.assurance import digest, envelope
from egypt_trust_map.hierarchy import summarize_hierarchy, validate_hierarchy
from egypt_trust_map.registry import load_registry, summarize, validate_registry
from egypt_trust_map.sovereignty import assess, load_json, validate_profile, validate_provider_register


ROOT = Path(__file__).resolve().parents[1]


class RegistryTests(unittest.TestCase):
    def test_seed_registry_is_valid(self):
        document = load_registry(ROOT / "registry" / "players.json")
        self.assertEqual([], validate_registry(document))

    def test_summary_counts_seed_players(self):
        document = load_registry(ROOT / "registry" / "players.json")
        self.assertEqual(9, summarize(document)["players"])

    def test_full_egcert_snapshot_is_valid(self):
        document = load_json(ROOT / "registry" / "egcert-accredited-providers.json")
        self.assertEqual([], validate_provider_register(document))
        self.assertEqual(42, len(document["providers"]))

    def test_duplicate_id_fails_closed(self):
        document = load_registry(ROOT / "registry" / "players.json")
        document["players"].append(dict(document["players"][0]))
        self.assertTrue(any("duplicate" in error for error in validate_registry(document)))

    def test_insecure_source_url_is_rejected(self):
        document = load_registry(ROOT / "registry" / "players.json")
        document["players"][0]["sources"] = ["http://example.test"]
        self.assertTrue(any("non-HTTPS" in error for error in validate_registry(document)))

    def test_json_assets_parse(self):
        for directory in ("registry", "integrations", "schemas", "sovereignty", "controls", "hierarchy", "benchmarks"):
            for path in (ROOT / directory).glob("*.json"):
                json.loads(path.read_text())

    def test_sector_ecosystem_is_valid_and_source_scoped(self):
        document = load_json(ROOT / "registry" / "sector-ecosystem.json")
        self.assertEqual([], validate_market_registry(document))
        self.assertEqual(48, sum(len(group["records"]) for group in document["groups"]))

    def test_technology_targets_are_valid(self):
        document = load_json(ROOT / "registry" / "technology-integration-targets.json")
        self.assertEqual([], validate_technology_targets(document))
        self.assertEqual(35, len(document["targets"]))

    def test_public_hierarchy_is_valid(self):
        model = load_json(ROOT / "hierarchy" / "reference-hierarchy.json")
        self.assertEqual([], validate_hierarchy(model))
        self.assertEqual(7, summarize_hierarchy(model)["tiers"])
        self.assertEqual(27, summarize_hierarchy(model)["nodes"])

    def test_public_hierarchy_rejects_sensitive_fields(self):
        model = load_json(ROOT / "hierarchy" / "reference-hierarchy.json")
        model["nodes"][0]["password"] = "synthetic-is-still-not-allowed"
        self.assertTrue(any("prohibited fields" in error for error in validate_hierarchy(model)))

    def test_benchmark_catalog_is_valid(self):
        catalog = load_json(ROOT / "benchmarks" / "catalog.json")
        self.assertEqual([], validate_catalog(catalog))
        self.assertEqual(32, len(catalog["scenarios"]))

    def test_kpi_baseline_is_valid(self):
        baseline = load_json(ROOT / "benchmarks" / "kpis.json")
        self.assertEqual([], validate_kpi_baseline(baseline))
        self.assertEqual(16, len(baseline["kpis"]))

    def test_reference_benchmark_qualifies(self):
        catalog = load_json(ROOT / "benchmarks" / "catalog.json")
        result = evaluate(catalog, reference_observations(catalog))
        self.assertTrue(result["qualified"])
        self.assertEqual(100.0, result["score"])
        item = envelope(catalog, result)
        self.assertEqual("reference-fixture", item["qualification"]["score_basis"])
        self.assertEqual("none", item["evidence"]["verification"])
        self.assertEqual(digest(result), item["evidence"]["artifact_sha256"])

    def test_benchmark_gate_is_non_compensating(self):
        catalog = load_json(ROOT / "benchmarks" / "catalog.json")
        observations = reference_observations(catalog)
        gate = next(scenario for scenario in catalog["scenarios"] if scenario["mandatory"])
        observations[gate["id"]] = "unexpected"
        metric_scores = {
            scenario["id"]: 100 for scenario in catalog["scenarios"] if not scenario["mandatory"]
        }
        result = evaluate(catalog, observations, metric_scores)
        self.assertFalse(result["qualified"])
        self.assertEqual(100.0, result["score"])
        self.assertIn(gate["id"], result["failed_gates"])

    def test_sovereignty_profile_totals_100(self):
        profile = load_json(ROOT / "sovereignty" / "requirements.json")
        self.assertEqual([], validate_profile(profile))

    def test_reference_sovereignty_architecture_qualifies(self):
        profile = load_json(ROOT / "sovereignty" / "requirements.json")
        submission = load_json(ROOT / "sovereignty" / "reference-assessment.json")
        result = assess(profile, submission)
        self.assertTrue(result["qualified"])
        self.assertEqual(95.0, result["score"])

    def test_foreign_saas_fixture_fails_non_compensating_gates(self):
        profile = load_json(ROOT / "sovereignty" / "requirements.json")
        submission = load_json(ROOT / "sovereignty" / "foreign-saas-negative-fixture.json")
        result = assess(profile, submission)
        self.assertFalse(result["qualified"])
        self.assertIn("no-mandatory-foreign-control-plane", result["failed_gates"])

    def test_high_score_cannot_compensate_for_failed_gate(self):
        profile = load_json(ROOT / "sovereignty" / "requirements.json")
        submission = load_json(ROOT / "sovereignty" / "reference-assessment.json")
        submission["gates"]["no-standing-vendor-super-admin"] = False
        result = assess(profile, submission)
        self.assertEqual(95.0, result["score"])
        self.assertFalse(result["qualified"])


if __name__ == "__main__":
    unittest.main()
