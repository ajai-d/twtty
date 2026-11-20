# Policy profile 1 — baseline internal policy

**Category:** `policies` · **Status:** default bundle (generic; author your own as `policy-profile2.md`, …)

Internal org/engineering policy applied at SPEC and PLAN. Policies may **raise** the active
`risk-calibration` controls (ratchet up), never relax them. They are distinct from external
regulatory compliance regimes.

## Baseline policy items

- **Data handling.** Confirm and record data classification truthfully; default to the
  least data necessary; no real customer/PII data in prototypes or non-production environments.
- **Secrets.** No secrets in source, logs, or the replay log; use the bound tooling's
  secret store; rotate on exposure.
- **Access.** Least-privilege by default; production-data access is logged and attributable.
- **Change management.** All production-affecting change flows through PR + CI gates; the
  production-promotion guardrail and break-glass procedure (with logged justification) are honored.
- **Retention.** Declare and honor a retention window per data class.

## How the AI Agent uses this file

Consult at SPEC/PLAN. Where a policy item is stricter than the active `risk-calibration` cell,
apply the stricter requirement and note the ratchet in the relevant plan/spec
section. Replace or extend this bundle with your organization's actual policy.
