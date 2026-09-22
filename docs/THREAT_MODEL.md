# Threat model

## Protected outcomes

- No unauthorized human, agent, workload or device receives material authority.
- No supplier, administrator or executive can silently exercise unreviewed root power.
- Revocation and emergency control continue during external isolation.
- Biometric and surveillance data remain purpose-bound and locally governed.
- Investigators can reconstruct identity, delegation, policy, approval and action history.
- Egypt can replace a supplier without losing identities, policy, evidence or operational continuity.

## Trust-boundary threats

| Threat | Example | Required control | Test |
|---|---|---|---|
| Foreign control-plane dependency | SaaS outage or geopolitical cutoff blocks authentication | Local decision plane and offline continuity | Disconnect external routes during exercise |
| Vendor support backdoor | Undocumented support identity reaches production | No standing vendor admin; approved gateway only | Enumerate accounts and attempt direct access |
| Root-key capture | One operator or supplier controls recovery | HSM quorum and separated shares | Recovery ceremony with independent witness |
| Malicious update | Signed but harmful vendor package | Staging, allow-list, SBOM, behavior test and rollback | Canary update plus rollback drill |
| Telemetry leakage | Identity or camera metadata exits approved boundary | Egress deny, local collectors and data-flow monitoring | Packet capture and DNS/proxy review |
| Delegation amplification | Agent creates a stronger child | Parent-scope subset enforcement | AgentIAM adversarial test |
| RAG ACL loss | Restricted document is retrieved through embeddings | ACL propagation and pre-retrieval authorization | Cross-principal retrieval test |
| Biometric replay | Old match assertion opens a new session | Nonce, audience, device and expiry binding | Replay and audience-substitution test |
| Camera compromise | Device becomes a network pivot | Segmentation, one-way collection where possible, no Internet egress | Lateral-movement simulation |
| Evidence deletion | Compromised PAM erases its own trail | Independent append-only evidence | Privileged deletion attempt |
| Break-glass abuse | Emergency account becomes permanent master key | Sealed quorum activation, expiry and review | Unannounced activation drill |
| Supplier lock-in | Policies or secrets cannot migrate | Inspectable contracts and tested export/restore | Annual replacement exercise |
| Insider collusion | Operators combine roles outside governance | Technical role separation and multi-party approval | Collusion tabletop and access graph review |
| Model substitution | Physical agent runs an unapproved model | Model digest attestation and action lease | Digest mismatch test |
| Fail-open partition | PDP outage permits privileged action | Local HA and fail-closed enforcement | Partition injection |

## Surveillance and biometric safeguards

The repository supports governance of lawful, authorized systems. It does not provide target identification, watchlist construction, covert collection, tracking tactics, or bypasses for consent and oversight.

Mandatory design constraints:

- Document purpose, lawful authority, owner, population, geography, retention and appeal route.
- Separate identity proofing from continuous surveillance.
- Prefer match assertions over distribution of raw templates.
- Measure demographic and environmental error rates for the deployed context.
- Require human review for consequential matches.
- Record model, threshold, sensor, timestamp and confidence without placing raw biometric data in general logs.
- Delete or revoke derived data when source authority expires.
