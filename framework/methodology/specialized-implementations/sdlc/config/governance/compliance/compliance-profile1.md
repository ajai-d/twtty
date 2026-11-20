# Compliance profile 1 — EU SaaS (GDPR + SOC 2)

**Category:** `compliance` · **Status:** example bundle (generic; author your own as `compliance-profile2.md`, …)

A **bundle** that selects which regulatory regimes apply for a given context. The selected
regimes' `MUST` rows come from the [regulatory-controls.md](regulatory-controls.md#regulatory-controls)
matrix; compliance **ratchets controls up, never down**.

## Regimes in this bundle

- **GDPR** — EU personal-data protection.
- **SOC 2** — trust-services criteria (security/availability/confidentiality).

## Authoring other bundles

Create `compliance-profile2.md` (HIPAA + HITECH), `compliance-profile3.md` (PCI-DSS), etc. —
each names the regimes active for its context; the shared [`regulatory-controls.md`](regulatory-controls.md)
matrix supplies the controls and disclaimer.
