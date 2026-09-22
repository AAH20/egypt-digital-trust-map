# Contributing

Every player or capability change must include a public primary or authoritative source, a verification date, and a neutral description. Vendor claims must remain marked `first-party-claim` until an independent reproducible test produces an evidence manifest. A registry described as complete must identify the exact source, scope and snapshot date; do not infer completeness across the wider market.

Country of origin, ownership, acquisition, hosting, support and jurisdiction claims require a primary corporate, regulator or legal source. Do not infer a company's nationality from a founder, employee, investor, customer or product name.

Sovereignty assessments must evaluate operational control. Every hard gate requires evidence; weighted scores cannot compensate for a failed gate. A named-product result must identify its exact version, deployment mode and test environment.

Do not submit personal data, personnel directories, credentials, key material, recovery shares, customer names without a public source, confidential contract details, operational network data, endpoints, topology, biometric templates, watchlists, live identifiers, or surveillance media. Use abstract role names, synthetic fixtures and redacted evidence. Follow the [publication boundary](docs/PUBLICATION_BOUNDARY.md).

Hierarchy changes must preserve one tier-zero policy root, strictly downward authority references, explicit compartments and public-safe outputs. Benchmark changes must keep mandatory safety and sovereignty gates non-compensating, identify expected results and require reproducible evidence. Optional benchmark weights must total 100.

Run before opening a pull request:

```bash
python -m unittest discover -s tests -v
python -m egypt_trust_map.cli verify
python -m egypt_trust_map.cli assess-sovereignty
python -m egypt_trust_map.cli verify-hierarchy
python -m egypt_trust_map.cli benchmark
```
