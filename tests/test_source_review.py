import copy
import unittest
from datetime import date
from pathlib import Path

from egypt_trust_map.source_review import freshness, review_candidate
from egypt_trust_map.sovereignty import load_json


SNAPSHOT = load_json(Path(__file__).resolve().parents[1] / "registry" / "egcert-accredited-providers.json")


class SourceReviewTests(unittest.TestCase):
    def test_freshness_is_date_relative_and_never_implies_accreditation_scope(self):
        self.assertEqual("current", freshness(SNAPSHOT, date(2026, 9, 23))["status"])
        self.assertEqual("stale", freshness(SNAPSHOT, date(2026, 10, 23))["status"])
        self.assertEqual("future-dated", freshness(SNAPSHOT, date(2026, 9, 21))["status"])

    def test_unchanged_candidate_needs_no_change_review(self):
        result = review_candidate(SNAPSHOT, copy.deepcopy(SNAPSHOT))
        self.assertTrue(result["valid"])
        self.assertFalse(result["requires_human_review"])

    def test_rename_and_renumber_are_explicit(self):
        candidate = copy.deepcopy(SNAPSHOT)
        candidate["providers"][0]["name"] += " updated"
        candidate["providers"][0]["id"], candidate["providers"][1]["id"] = (
            candidate["providers"][1]["id"], candidate["providers"][0]["id"]
        )
        result = review_candidate(SNAPSHOT, candidate)
        self.assertTrue(result["valid"])
        self.assertTrue(result["requires_human_review"])
        self.assertEqual(2, len(result["changes"]["renamed"]))
        self.assertEqual(2, len(result["changes"]["renumbered"]))

    def test_source_change_and_invalid_register_fail_closed(self):
        candidate = copy.deepcopy(SNAPSHOT)
        candidate["source_url"] = "https://unrelated.example"
        candidate["providers"].pop()
        result = review_candidate(SNAPSHOT, candidate)
        self.assertFalse(result["valid"])
        self.assertTrue(result["errors"])


if __name__ == "__main__":
    unittest.main()
