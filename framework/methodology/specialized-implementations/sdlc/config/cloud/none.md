# Cloud binding — none (no cloud services)

**Category:** `cloud` · **Status:** reference (explicit no-cloud-services selection in `runtimeconfig.md`)

## What this binds

**No cloud services or hosting.** Select this binding explicitly only when the approved scope uses neither cloud-service dependencies nor cloud application hosting. Do not infer it from `Runtime target: N/A`: a local app may need real Azure services and retain its Azure binding. Selection depends on actual approved dependencies, not risk level alone.

Local support services/emulators and their environment definitions may still apply under the [development profile](../development/default.md#environment-iac-and-resource-ownership). Shared CI remains required by default even without cloud services/CD.

## Effect on controls

- Cloud-access/hosting-specific identity and deployment rows are not engaged only when there is no actual cloud access/hosting. Applicable local infrastructure, data, approval, repository and CI controls remain enforced.
- Encryption-in-transit is N/A for local-only / loopback traffic that crosses no network
  boundary (documented in the plan's security architecture).
- Adding a cloud dependency requires an approved provider/configuration and scope update, not automatic hosting/CD. Adding hosting separately requires approved delivery, selected cloud environments and the applicable CI/CD, identity and acceptance controls. Preserve existing overrides; no silent refresh or provisioning.

## How this binding satisfies the TWTTY contract

There is no cloud seam, so the OIDC/workload-identity contract rows are not engaged. All
other controls (reviewed merge, native independent verification, attributable commits, escalation)
are satisfied by the bound CI/CD tooling.
