# Publication Boundary

This repository is designed to improve market transparency and technical assurance without publishing an operational attack map. All contributions must pass both a public-interest test and a minimization test.

## Permitted public material

- Organization and product names already present in authoritative or first-party public sources.
- Neutral capability claims with a source, verification date and evidence state.
- Public standards, schemas, control mappings and benchmark definitions.
- Abstract organizational roles and trust relationships.
- Synthetic identities, documents, images, sensor events and machine actions.
- Redacted conformance results, hashes and aggregate measurements.

## Prohibited material

- Names or contact details of non-public personnel, administrators, custodians or reviewers.
- Usernames, passwords, tokens, certificates, private keys, recovery shares or security-question material.
- Biometric templates, watchlists, national identifiers, live faces, voiceprints or surveillance media.
- IP addresses, hostnames, private endpoints, physical locations, network paths or customer topology.
- Confidential contracts, pricing, investigative records, vulnerabilities without coordinated disclosure, or government-only information.
- Claims about customers, deployments, affiliations, control or market share without a public source.

## Abstraction rules

Use roles such as `root-policy-quorum`, `tenant-security-admin` or `evidence-reviewer`, never personal names. Model a dependency as a standards interface or product-family adapter rather than a live endpoint. Represent keys by public identifiers and algorithms, never key material. Represent biometric processing with synthetic fixture identifiers and deletion receipts, never templates. Represent surveillance behavior with synthetic event metadata, never live imagery.

## Evidence release

A public evidence manifest may state what was tested, the expected result, the observed status, component versions, artifact hashes and aggregate timing. Store sensitive source evidence in the controlled assessment environment. Redaction must be irreversible and must remove metadata that could identify people, sites or infrastructure.

Before publication, a reviewer should confirm source authority, scope, data classification, minimization, reproducibility and expiry. Uncertain material stays out of the public repository until it can be safely represented.
