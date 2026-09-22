# Procurement, deployment and exit gates

## Gate 0 — mission and data classification

Define the protected mission, identities, assets, actions, availability objective, recovery objective, data classifications, biometric or surveillance involvement, and consequences of false allow and false deny. A product comparison without this scope is invalid.

## Gate 1 — ownership and jurisdiction disclosure

Record the contracting entity, parent companies, development and support locations, subprocessors, applicable laws, hosting regions, telemetry destinations, update-signing authority and acquisition-change clauses. Country of origin is recorded as evidence, not used as the only risk score.

## Gate 2 — architecture and key custody

The supplier must disclose every control plane, management endpoint, support path, trust anchor, recovery secret, outbound dependency and privileged account. Sovereignty-tier roots and recovery shares remain under Egyptian quorum control.

## Gate 3 — offline and isolation test

Block all unapproved external traffic and demonstrate local authentication, authorization, revocation, privileged recovery, logging and incident response for the defined isolation period. A slide or contractual promise is not evidence.

## Gate 4 — interoperability and replacement

Export users, groups, roles, policies, certificates, secrets metadata, audit events and configuration through documented formats. Restore into a clean environment and migrate at least one representative workflow to a different implementation.

## Gate 5 — supply-chain admission

Require pinned artifacts, signatures, SBOM, vulnerability disposition, staged deployment, reproducible configuration, canary monitoring, rollback and emergency patch procedure. Automatic production updates are prohibited in critical zones.

## Gate 6 — operational control

Test joiner/mover/leaver latency, privileged approval, session recording, credential rotation, revocation, policy rollback, backup, clean-room recovery and evidence verification. Validate staff can operate without supplier intervention.

## Gate 7 — biometric and surveillance review

Where applicable, require documented purpose, authority, retention, access, model and threshold governance, demographic and environmental evaluation, appeal process, false-match handling, human review and deletion verification.

## Gate 8 — commercial exit

Contract for configuration and evidence ownership, data return, verified deletion, transition assistance, source or escrow arrangements where justified, acquisition notification, subprocessor changes, vulnerability disclosure, breach notification and predictable termination cost.

## Acceptance decision

A deployment qualifies only when:

- Every sovereignty hard gate passes.
- Weighted score is at least 80/100.
- No critical evidence item is self-attested without a reproducible test.
- Named owners accept remaining risks with expiry dates.
- Recovery and replacement exercises succeed.

## Recurring evaluation

| Interval | Exercise |
|---|---|
| Continuous | Unauthorized-action, revocation, telemetry-egress and evidence-integrity monitoring |
| Monthly | Privileged-account and vendor-access inventory |
| Quarterly | Isolation, failover, restore and policy rollback sample |
| Semiannual | Root-role review, support-path review and supply-chain reassessment |
| Annual | Full recovery ceremony, provider replacement exercise and independent review |
| Event-driven | Reassess after acquisition, jurisdiction change, major vulnerability, architecture change or material incident |
