# Devtools binding — GitHub ecosystem

**Category:** `devtools` · **Status:** reference (set active in `runtimeconfig.md`)

## What this binds

The developer platform that provides the **repository + branch/PR model, CI/CD, code
scanning / security, and the optional work-tracking mirror**. This bundle is the GitHub
ecosystem; `devtools-config2.md` binds Azure DevOps as an alternative.

## Components

| Capability | GitHub provides | TWTTY uses it for |
|------------|-----------------|-------------------|
| Repository + remote | GitHub repo (created or reused at SEED first contact) | Version control from SEED; every artifact committed + published through authorized repository controls |
| Branch/PR model | Direct Sequential work where permitted; one working branch per affected domain; isolated branches/worktrees for parallel writers | Preserve existing protection; use a scope/domain PR when required, not per-item PRs; routine worker merges target the recorded working branch |
| Branch protection | Branch protection rules/rulesets | Owner-authorized required CI/merge checks by default; risk-tiered review controls |
| Ownership | `CODEOWNERS` | Required at L3+ (and at any level once 2+ Human Users) |
| CI/CD | **GitHub Actions** | Applicable build/lint/test/scan, hosting-native-IaC/deploy and gate checks per §7.1.3; no custom local-infra suite or app-CI prerequisite for initial developer-owned resource creation |
| Code scanning / security | CodeQL, Dependabot, secret scanning (GitHub Advanced Security) | §7.1.1 secret / SAST / dependency / license / container scanning |
| Work-tracking mirror | **GitHub Issues** | OPTIONAL kanban mirror of the plan's `W-<n>` work items; the plan stays source of truth |
| Async delegation | GitHub Copilot Coding Agent | `Delegate` target |

Configuration specifics (workflow YAML, protection settings, GHAS toggles) evolve and are
the AI Agent's responsibility to look up in current GitHub documentation.

## How this devtools binding satisfies the TWTTY contract

| Required control | How GitHub meets it | Escalate if |
|------------------|---------------------|-------------|
| **Reviewed merge** | PR review + branch protection requiring review before merge | Branch protection cannot be set where the risk level requires it |
| **Independent verification** | Native required application CI checks, Git/PR history and required reviews provide implementation evidence; inspect methodology artifacts directly, without generated gate-check scripts | Required native checks/reviews or explicit external policy controls cannot be satisfied |
| **Attributable commits** | Commits/PR approvals carry authenticated GitHub identities; L3+ requires verified-signature commits or platform-authenticated PR approval for the Autopilot anchor | Signature/approval identity cannot be verified at L3+ |
| **Escalation destination** | `escalation: pr-comment` or `github-issue` posts the `Escalate` to the PR/issue | The configured channel is unreachable |
| **OIDC on the cloud seam** | GitHub OIDC federated credentials to the bound cloud/deploy target (no long-lived secrets in CI) | The deploy target cannot trust GitHub OIDC |

**Evidence handling:** Use existing GitHub/native scanners and context-aware review
to keep secrets and identifiers out of persisted evidence under core §2. Invoke its
shared privacy utility before risky evidence writes, including copied identities,
provider output and errors; controlled safe metadata needs no invocation. Do not generate
a project-local evidence validator, identifier-detector test suite or methodology-only CI job.
Record actual methods/limits; secret scanning is not exhaustive identifier detection.
Native authorship/approval metadata stays outside redacted evidence. An explicitly
required organization/regulatory control that cannot be met still Escalates.

## Stage hooks

- **SEED:** create a repo/remote only when needed; preserve existing history, remotes and integration branch. Publish `seed/` through authorized repository controls.
  For a new repository, propose the confirmed project slug as its name, the explicitly
  approved owner when known (otherwise the current authenticated account), and private
  visibility absent an approved preference. Show the concrete destination and let the
  Human confirm/edit before creation. Authentication is not permission to create under
  an organization. Resolve conflicts explicitly; reuse an approved existing remote.
- **Before early gates:** use existing native Git/platform evidence and direct artifact review. Do not bootstrap custom methodology validators/CI. Application build/deploy automation remains EXECUTE work; explicit external policy controls remain binding.
- **SPEC/PLAN:** publish `spec/`, `plan/`, replay log, state and diagram through the existing PR/CI/review process. Direct bootstrap pushes are limited to new, authorized, unprotected repositories per SDLC §3.1/§8.3; never disable protection for onboarding.
- **EXECUTE (Setup):** configure/reuse one project CI workflow and matching required checks with owner authorization, plus applicable `CODEOWNERS`/review controls. CI is default, CD optional; missing CI blocks normal merge, not local work/PR creation. Do not install per-developer CI or silently bypass protection.
- **EXECUTE:** follow SDLC §5.1's Sequential/domain/parallel topology. Worker integration needs no extra approval/PR where target policy permits; protected targets retain required checks/reviews. Read actual rules, refresh candidates at integration, and do not disable strict protection or open evidence-only PRs. Do not configure PR-only protection for a new direct-development scope unless required by its approved risk/policy controls.
