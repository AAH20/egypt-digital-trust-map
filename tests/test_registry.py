import json
import unittest
from pathlib import Path

from egypt_trust_map.registry import load_registry, summarize, validate_registry


ROOT = Path(__file__).resolve().parents[1]


class RegistryTests(unittest.TestCase):
    def test_seed_registry_is_valid(self):
        document = load_registry(ROOT / "registry" / "players.json")
        self.assertEqual([], validate_registry(document))

    def test_summary_counts_seed_players(self):
        document = load_registry(ROOT / "registry" / "players.json")
        self.assertEqual(9, summarize(document)["players"])

    def test_duplicate_id_fails_closed(self):
        document = load_registry(ROOT / "registry" / "players.json")
        document["players"].append(dict(document["players"][0]))
        self.assertTrue(any("duplicate" in error for error in validate_registry(document)))

    def test_insecure_source_url_is_rejected(self):
        document = load_registry(ROOT / "registry" / "players.json")
        document["players"][0]["sources"] = ["http://example.test"]
        self.assertTrue(any("non-HTTPS" in error for error in validate_registry(document)))

    def test_json_assets_parse(self):
        for path in (ROOT / "registry").glob("*.json"):
            json.loads(path.read_text())
        for path in (ROOT / "integrations").glob("*.json"):
            json.loads(path.read_text())
        for path in (ROOT / "schemas").glob("*.json"):
            json.loads(path.read_text())


if __name__ == "__main__":
    unittest.main()
