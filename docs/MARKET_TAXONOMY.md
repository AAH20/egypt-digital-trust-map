# Egypt digital-trust market taxonomy

The map records organizations by demonstrated role rather than placing every company in a broad “cybersecurity” bucket.

| Layer | Included roles | Evidence priority |
|---|---|---|
| Public authority | Regulators, national CERT, root trust and sector supervisors | Official register, law, mandate or authority publication |
| Trust services | Root CA, government CA, licensed signature and seal providers | ITIDA license listing and certificate-policy documents |
| Identity infrastructure | Directories, federation, authentication, PKI and identity proofing | Protocol documentation and reproducible integration test |
| Privileged access | Credential issuance, secrets, session control, JIT access and recovery | Architecture disclosure and adversarial test |
| Cybersecurity services | EG-CERT-accredited providers and permitted service/customer scopes | Live EG-CERT register |
| Telecom and hosting | Licensed telecom, data-center, cloud and connectivity providers | Regulator or first-party service evidence |
| Financial infrastructure | Banks, payments, clearing, fintech and sector trust | Regulator and operator evidence |
| Physical security | Cameras, NVR/VMS, access control, sensors and integrators | Product documentation and lab inspection |
| Biometrics | Proofing, matching, liveness and assertion services | Evaluation protocol, privacy controls and deployed-context test |
| AI and data | Agent frameworks, RAG, VLA models, digital twins and analytics | Versioned model/system card and authorization evidence |
| Assurance | GRC, audit, conformance, incident response and forensic evidence | Reproducible control evidence and assessor scope |
| Education and research | Universities, labs, training and professional bodies | Institutional program evidence |

## Record states

- `authoritative`: the organization publishes its own legal mandate or register.
- `authoritative-listing`: an authority lists the organization in a defined role.
- `first-party-claim`: the organization claims a capability; no independent test is implied.
- `independently-tested`: a reproducible evidence bundle supports the stated version and scope.
- `expired`: the cited status or evidence passed its review date.
- `disputed`: a material challenge is under documented review.
- `superseded`: a newer record preserves but replaces the earlier conclusion.

## Completeness

“Every player” is an ongoing coverage objective. The repository may claim completeness only for a named authoritative register, snapshot date and captured sequence. It must never imply that a snapshot exhausts informal providers, new entrants, government-only suppliers, resellers, unpublicized contracts or changes after verification.

## Vendor and product neutrality

Registry inclusion is not approval. Product nationality is recorded where supported, while sovereignty scoring evaluates who controls roots, policy, data, telemetry, recovery, updates and exit. This prevents both uncritical foreign dependence and unsupported nationality-based conclusions.
