# Cloud binding — Azure

**Category:** `cloud` · **Status:** default provider binding; confirm hosting separately in spec `Runtime target`

## What this binds

Microsoft Azure for approved development services and selected cloud hosting: identity, IaC, registry, and runtime. Binding Azure alone does not select hosting or authorize provisioning. The
`risk-calibration` matrix (§7.1.4 / §7.1.7) defines the **controls**; this file maps them to
Azure's specific services. The AI Agent MUST verify current service names and guidance in
Azure documentation at adoption time.

> **This binding is guidance, not templates.** It names resource *types* and property
> *shapes* only. It MUST NOT contain — and the AI Agent MUST NOT copy from it — any
> concrete `.bicep` / IaC file content, pinned API versions, or ready-made templates.
> All IaC is an **EXECUTE (3h) artifact** the AI Agent authors per project under `infra/`,
> using current resource schemas and API versions looked up at author time (a Bicep tool /
> `az bicep` where available). The example filenames and CLI commands below are illustrative
> invocations, not spec-shipped templates.

## Provider mapping (control → Azure implementation)

| TWTTY control (from the matrix) | Azure implementation |
|---------------------------------|----------------------|
| CI-to-cloud auth via OIDC / short-lived credential | GitHub OIDC → a **user-assigned managed identity** with a **GitHub federated credential**, both declared in IaC (`Microsoft.ManagedIdentity/userAssignedIdentities` + `federatedIdentityCredentials`). **No Entra app registration, no client secrets in CI** — `azure/login` authenticates as the UAMI |
| Cloud-hosted app auth via workload identity | **Managed identity** (user-assigned or system-assigned) |
| Local app/evaluation cloud-service auth | Approved developer **Entra** authentication, including supported Azure CLI credentials; no copied service keys or assumed container access to host login |
| IaC language | **Bicep** or Terraform (azurerm/azapi) |
| RBAC in IaC, least-privilege scope | Azure RBAC role assignments declared in IaC at resource-group / single-resource scope |
| Local-auth / shared-key disabled | Disable storage account keys, disable admin user on ACR, disable local auth on data-plane services |
| Cloud-native registry with workload-identity pull | **Azure Container Registry (ACR)** with managed-identity pull |
| Hosting identity bootstrap IaC cannot self-bootstrap | Approved UAMI/federation/RBAC Bicep is applied once via developer `az deployment` when CI has no initial credential; hosting then deploys via OIDC. No hand-created Entra app/client secret/portal shortcut. This hosting bootstrap is distinct from approved local-development dependency IaC below. |

## How this binding satisfies the TWTTY contract

| Required control | How Azure meets it | Escalate if |
|------------------|--------------------|-------------|
| **OIDC on the cloud seam** | Entra workload identity federation trusts the bound CI/CD OIDC issuer; no long-lived secrets in CI | Federation to the bound CI/CD issuer cannot be established |
| **Least-privilege identity** | RBAC role assignments scoped in IaC | The required scope cannot be expressed in IaC |
| **Cloud hosting from CD** | Hosting infrastructure/app releases use CI/CD; approved minimal local-development dependencies use reviewed IaC through developer Azure CLI below; no raw resource-create/portal/`azd up` shortcut | Required hosting CD or the approved scoped development path cannot be satisfied |

## Local-development dependencies

Follow the bound development profile for the [infra-kickoff/reuse procedure](../development/default.md#development-infrastructure-first),
[application connection settings](../development/default.md#application-connection-settings)
and [environment ownership](../development/default.md#environment-iac-and-resource-ownership).
Those procedures are not duplicated in this provider binding.

Discover only the needed service/resource types and selected deployment metadata within
the authorized RG/subscription scope; do not turn reuse into a subscription-wide audit.
Select the implementation client and workflow that fit the chosen compatible endpoint.
A model dependency does not by itself require a Foundry project or hosted-agent workflow.
Resolve any conflict between a helper workflow and the approved native IaC route before
actions, not by silently importing the helper's infrastructure or prerequisites.

For approved creation, use reviewed IaC and the developer's **Azure CLI / Entra** context.
After required provisioning consent, run `az deployment group create --resource-group <approved-group> --template-file <environment-entry.bicep> --parameters ...`
(or the approved native scope equivalent). Azure CLI compiles Bicep as part of deployment;
no mandatory separate `az bicep build`, `az deployment group validate` or `what-if`.
`what-if` is an optional separate preview for the new isolated creation path, not something
Bicep runs automatically. Apply the profile's stronger preview requirements when applicable.
Terraform retains its mandatory native initialization/plan/apply steps.

Resolve only missing Azure target, resource/model/version, identity/network and data/cost
inputs. Denied or ambiguous Azure access is **not missing** and must not trigger duplicate
provisioning. Do not retrieve service keys or use raw-create/portal shortcuts or no-op
approval flags; native prompts are not bypassed.

Development access does **not** require unrelated CI federation. Cloud hosting stays
pipeline-owned and hosted runtime uses Managed Identity; local developer authentication
is separate and applicable containers verify it in their normal run.

## Stage hooks

- **PLAN (infrastructure + security architecture):** apply [SDLC's hosting CD contract](../../sdlc.md#34-execute), mapping §1.3 to the selected Azure services. `plan §1.4` declares Azure CI federation, app Managed Identity and IaC RBAC; §3.2 sequences verified `W-<n>-identity-bootstrap` before dependent hosting/pipeline work, not unrelated local developer access.
- **PLAN (local-first profile):** `plan §1.3` declares native build/test/run, service/emulator/container applicability and approved development Azure dependencies via the developer CLI/IaC path above, with necessity/identity/data/cost boundaries and environment ownership. Concrete paths in §2.3, config and work footprints must agree. §1.6 identifies offline, real-model and deployed verification gaps. Hosted delivery requires CI promotion before hosting provisioning/app deployment. `Runtime target: N/A` retains Azure when development services need it.
- **EXECUTE (development dependencies):** apply the bound development procedure using the Azure-specific CLI/identity mapping above.
- **EXECUTE (hosting bootstrap):** verify necessary `W-<n>-identity-bootstrap` before dependent hosting/pipeline work. Hosting retains its required native static/preview and specific apply approval, followed by CD/OIDC. It is not a prerequisite for local developer services and permits no portal/raw-create, service keys or unapproved spend.
- **EXECUTE (cloud-independent verification, hosting only):** CI checks required inputs before hosting infra/app CD. Do not use this hosting prerequisite to block the separate development-resource sequence on app CI, tests or eval code. Reuse valid evidence and verify actual deployed/service acceptance at its normal app checkpoint.
- **EXECUTE (infrastructure CD):** implement [SDLC's hosting CD contract](../../sdlc.md#34-execute) with the selected Bicep/Terraform entry points and approved Azure federated pipeline identity from the provider mapping above.
- **EXECUTE (application CD):** implement the same [hosting CD contract](../../sdlc.md#34-execute) using the approved Azure runtime and Managed Identity; use ACR when image hosting applies, per the provider mapping above.

## Guided identity bootstrap (the AI Agent walks the Human User through this, once)

This one-time **hosting CI-federation bootstrap** is separate from approved local-development IaC applies. Guide the Human User interactively: confirm prerequisites/target, present commands, obtain specific approval and verify results. **Propose suitable existing identity reuse before creation**; do not take ownership or change another deployment owner's resource without approval. No Entra app registration or portal shortcut.

1. **Confirm the target.** `az login` (if not already signed in), then `az account set --subscription "<subscription>"`; confirm `az account show` names the intended subscription.
2. **Determine the ACTUAL federated subject — do not assume the textbook format.** The subject claim GitHub presents is usually `repo:<owner>/<repo>:ref:refs/heads/<branch>` (or `:environment:<env>`), **but some GitHub orgs/accounts emit an ID-qualified subject** such as `repo:<owner>@<ownerId>/<repo>@<repoId>:ref:refs/heads/<branch>` (a customized OIDC subject claim). A federated credential subject MUST match **exactly** — a mismatch fails at login with `AADSTS700213: No matching federated identity record found`, which **prints the exact subject GitHub presented**. The AI Agent MUST obtain the real subject rather than guess: preferably run the deploy/login workflow once and read the `subject claim - …` line the `azure/login` step logs (the `AADSTS700213` error prints the same string), then set the credential to that exact value. The branch of the subject MUST match the branch the deploy workflow runs on.
3. **Reuse before create (propose + get approval).** Discover identities/federation read-only. Reuse matching trust with approval; when a subject must be added, coordinate reviewed IaC with the existing deployment owner rather than raw CLI creation or takeover. Create a new identity only when no suitable authorized one exists.
4. **Author identity Bicep** for approved creation/augmentation under `W-<n>-identity-bootstrap`: owned UAMI/reference, matching federated subject/issuer/audience and least-privilege RBAC. Preserve another owner's resource declaration. Return only the non-secret identifiers needed by CI.
5. **Apply once from the dev machine** for approved creation/augmentation: `az deployment sub create -l <region> -f infra/environments/cloud/<stage>/identity.bicep -p ...` (illustrative selected-environment path; validate/preview and approve first, then use the Human User's `az login`).
6. **Wire the repo:** set the three identifiers as repo variables (not secrets — they are not passwords) — `gh variable set AZURE_CLIENT_ID` (the reused or new UAMI clientId), `AZURE_TENANT_ID`, `AZURE_SUBSCRIPTION_ID`.
7. **Verify** before dependent hosting work: approve/trigger a login-smoke workflow and confirm `azure/login` succeeds via OIDC; check federation/RBAC. Subject mismatch requires approved correction and bounded retry. Login alone does not authorize release: selected protected-merge triggers, required CI/environment approvals, compatible infrastructure and deployed acceptance still apply.
