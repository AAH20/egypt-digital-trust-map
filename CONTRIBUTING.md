# Contributing

Every player or capability change must include a public primary or authoritative source, a verification date, and a neutral description. Vendor claims must remain marked `first-party-claim` until an independent reproducible test produces an evidence manifest.

Do not submit personal data, credentials, customer names without a public source, confidential contract details, operational network data, biometric samples, or surveillance media.

Run before opening a pull request:

```bash
python -m unittest discover -s tests -v
python -m egypt_trust_map.cli verify
```
