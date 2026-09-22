# Contributing

Every player or capability change must include a public primary or authoritative source, a verification date, and a neutral description. Vendor claims must remain marked `first-party-claim` until an independent reproducible test produces an evidence manifest.

Country of origin, ownership, acquisition, hosting, support and jurisdiction claims require a primary corporate, regulator or legal source. Do not infer a company's nationality from a founder, employee, investor, customer or product name.

Sovereignty assessments must evaluate operational control. Every hard gate requires evidence; weighted scores cannot compensate for a failed gate. A named-product result must identify its exact version, deployment mode and test environment.

Do not submit personal data, credentials, customer names without a public source, confidential contract details, operational network data, biometric samples, or surveillance media.

Run before opening a pull request:

```bash
python -m unittest discover -s tests -v
python -m egypt_trust_map.cli verify
python -m egypt_trust_map.cli assess-sovereignty
```
