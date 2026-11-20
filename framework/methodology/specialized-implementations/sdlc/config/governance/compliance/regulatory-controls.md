# Regulatory controls (canonical)

**Category:** `compliance` · The canonical regime→control matrix — the single source of
common technical controls per regulatory regime. A `compliance` **profile** selects which
regimes apply; this file defines what each requires. Gated by regime membership, not risk
level; **ratchets controls up, never down**.

## Regulatory controls

**Application.** For each regime that applies (as selected by the bound profile), the `MUST`
cells below are added on top of the active level's column (per the risk-calibration matrix
application rule). Retention and notification windows vary by jurisdiction — the AI Agent
MUST look up the current figure.

| Requirement | If SOC 2 | If HIPAA | If PCI-DSS | If GDPR |
|-------------|:--------:|:--------:|:----------:|:-------:|
| Access to production data logged and attributable to an individual identity (no shared/service-account interactive access) | MUST | MUST | MUST | MUST |
| Data-at-rest encryption uses customer- or platform-managed keys with a documented key-rotation policy | SHOULD | MUST | MUST | MUST |
| Data-subject rights procedure (access, correction, deletion) documented and executable | — | MUST (PHI access/amendment) | — | MUST |
| Audit log of access to regulated data retained for the regime's current minimum retention period | MUST | MUST | MUST | MUST |
| Breach/incident notification procedure documented with the regime's current notification window | SHOULD | MUST | MUST | MUST |
| Data-processing / business-associate agreement executed with every subprocessor touching regulated data | — | MUST (BAA) | — | MUST (DPA) |
| Cardholder data, if present, never stored unencrypted and scoped to the smallest feasible network segment | — | — | MUST | — |
| Independent third-party audit or attestation scheduled and tracked | MUST (Type II) | — | MUST (as applicable) | — |

**Other regimes.** For a regime not listed (FedRAMP, ISO/IEC 27001, NIST 800-53, CCPA/CPRA,
SOX, FERPA, COPPA, or a jurisdiction-specific law), derive an equivalent MUST/SHOULD/— set
from the same eight control categories, research its current authoritative requirements
(core §4.5), and record the derived rows, the regime, and the source.

## Required disclaimer

A **starting checklist** of common technical controls — **not** a substitute for qualified
legal/compliance review, and not exhaustive. Whenever a regime applies, the AI Agent MUST
recommend that review, surface this disclaimer (core §4.5), and record the confirmed regimes
and sources consulted.
