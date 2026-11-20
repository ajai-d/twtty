# Devtools binding — Azure DevOps ecosystem

**Category:** `devtools` · **Status:** reference (set active in `runtimeconfig.md`)

## What this binds

The developer platform providing repository + branch/PR model, CI/CD, scanning, and the
optional work-tracking mirror — bound to **Azure DevOps** as an alternative to the GitHub
ecosystem (`devtools-config1.md`).

## Components

| Capability | Azure DevOps provides | TWTTY uses it for |
|------------|-----------------------|-------------------|
| Repository + remote | Azure Repos (Git) | Version control from SEED |
| Branch/PR model | Direct Sequential work where permitted; one working branch per affected domain; isolated branches/worktrees for parallel writers | Preserve existing policies; use a scope/domain PR when required, not per-item PRs; routine worker merges target the recorded working branch |
| Branch protection | Branch policies | Owner-authorized required CI/merge checks by default; risk-tiered review controls |
| Ownership | Required reviewers / path policies (CODEOWNERS equivalent) | Required at L3+ (or 2+ Human Users) |
| CI/CD | **Azure Pipelines** | Applicable build/lint/test/scan, hosting-native-IaC/deploy and gate checks per §7.1.3; no custom local-infra suite or app-CI prerequisite for initial developer-owned resource creation |
| Code scanning / security | Advanced Security for Azure DevOps (CodeQL, dependency, secret scanning) | §7.1.1 scanning controls |
| Work-tracking mirror | **Azure Boards** work items | OPTIONAL mirror of the plan's `W-<n>` work items; the plan stays source of truth |

Configuration specifics (YAML pipelines, branch policies, Advanced Security toggles) are
the AI Agent's responsibility to look up in current Azure DevOps documentation.

## How this devtools binding satisfies the TWTTY contract

| Required control | How Azure DevOps meets it | Escalate if |
|------------------|---------------------------|-------------|
| **Reviewed merge** | PR + branch policy requiring reviewers before completion | Branch policy cannot be set where required |
| **Independent verification** | Native required application pipeline checks, Git/PR history and required reviewers provide implementation evidence; inspect methodology artifacts directly, without generated gate-check scripts | Required native checks/reviews or explicit external policy controls cannot be satisfied |
| **Attributable commits** | Authenticated AAD identities; L3+ verified-signature commit or platform-authenticated PR approval for the Autopilot anchor | Signature/approval identity unverifiable at L3+ |
| **Escalation destination** | `escalation` posts to the PR or a Boards work item | Channel unreachable |
| **OIDC on the cloud seam** | Azure Pipelines workload-identity federation to the bound cloud/deploy target | The deploy target cannot trust the pipeline's federated identity |

**Evidence handling:** Use existing Azure DevOps/native scanners and context-aware
review to keep secrets and identifiers out of persisted evidence under core §2. Invoke its
shared privacy utility before risky evidence writes, including copied identities,
provider output and errors; controlled safe metadata needs no invocation. Do not generate
a project-local evidence validator, identifier-detector test suite or methodology-only pipeline.
Record actual methods/limits; secret scanning is not exhaustive identifier detection.
Native authorship/approval metadata stays outside redacted evidence. An explicitly
required organization/regulatory control that cannot be met still Escalates.

## Stage hooks

- **SEED:** create a repo/remote only when needed; preserve existing history, remotes and integration branch. Publish `seed/` through authorized repository controls.
  Propose the confirmed project slug as the repository name within the known approved
  organization/project; respect inherited project visibility and permissions. Show the
  concrete destination with confirm/edit choices. Resolve missing project authority or
  name conflicts explicitly; do not create an organization/project or change visibility
  merely to create a repo. Reuse an approved existing remote.
- **Before early gates:** use existing native Git/platform evidence and direct artifact review. Do not bootstrap custom methodology validators/pipelines. Application build/deploy automation remains EXECUTE work; explicit external policy controls remain binding.
- **SPEC/PLAN:** commit and push approved artifacts to the authorized working branch; update the existing scope/domain PR when required. Stage approval does not require a separate PR or merge per stage; apply SDLC §8.3. Required build policies/reviews still gate integration, and explicit earlier-merge policies remain binding. Direct bootstrap pushes are limited to new, authorized, unprotected repositories per SDLC §3.1/§8.3; never disable protection for onboarding.
- **EXECUTE (Setup):** configure/reuse one project CI pipeline and matching required build policies with owner authorization, plus applicable reviewers. CI is default, CD optional; missing CI blocks normal completion, not local work/PR creation. No per-developer pipeline or silent protection bypass.
- **EXECUTE:** follow SDLC §5.1's Sequential/domain/parallel topology. Worker integration needs no extra approval/PR where target policy permits; protected targets retain required checks/reviews. Read actual policies, refresh candidates at integration, and do not bypass them or open evidence-only PRs. Do not configure PR-only policies for a new direct-development scope unless required by its approved risk/policy controls.
