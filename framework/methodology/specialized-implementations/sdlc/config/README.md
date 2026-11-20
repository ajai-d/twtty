# TWTTY capability-binding config

This directory makes TWTTY **tool-agnostic**. The methodology specs state *what* must
hold (the obligations, gates, and controls); the files here state *which tools, platforms,
clouds, thresholds, and knowledge* a given project binds those obligations to. Swap a
binding here and the same methodology runs on a different harness, platform, or cloud —
without editing the spec.

## Default source and project configuration

| File | Who writes it | When | Role |
|------|---------------|------|------|
| **`config/default-config.md`** (in this library) | shipped with the library | initial bootstrap | Defaults for the first SEED and initial config resolution. Never edited per project. |
| **`<project-folder>/twtty-runtime-config/`** (in the project repo, not here) | the **AI Agent**, via config resolution and authorized updates | **Discovery (SPEC)** onward | A complete local config tree, composed defaults, and a same-structure `runtimeconfig.md` containing all effective settings and override values. |

**Materialize the whole tree.** Copy the baseline config folder structure and all its files,
not only overrides or selected profiles, into the project-owned folder. Merge the active
specialization's config tree and compose its source default-config chain into a complete
local `default-config.md`. Merge nested mappings by key: adding `tokenomics.product`, for
example, must preserve `tokenomics.build`. Apply user overrides after composing defaults.
Normalize configuration references to the local tree; no shared config dependency may
remain. Generate the project README from
[`runtime-config-readme-template.md`](runtime-config-readme-template.md).

**Review the actual copy.** Initial materialization is a draft within the approved
scope. In the existing Discovery/config interview, show effective settings and local
files after copying/composition, mark provisional PLAN-time model/stack choices, and
offer **Use these settings / Customize settings** once. Resolve edits before the
existing `meta/config` record; this is not a new gate or per-setting interview. Prior
valid approvals and unchanged Resume configurations do not require reapproval.

**Same schema, resolved values.** The project's `runtimeconfig.md` uses the composed
default file's binding keys and nesting, with approved overrides substituted. All
effective default-derived settings are present; runtime-only choices are added as they
become known. There is no separate overrides-only schema. File-backed selections point
to local files and resolve relative to their containing config file. Spec-defined
settings may reference the project's own spec. Record which settings/profiles were
explicitly overridden in `meta/config`, rather than maintaining another authoritative
copy of their current values.

Keep service/provider selection separate from application hosting and environment ownership.
The `development` profile defines product-root infrastructure/recipe paths; configuration
binding paths still resolve inside this local config tree. PLAN records actual ownership
and entry points under the [environment-purpose rule](development/default.md#environment-iac-and-resource-ownership).
`Runtime target: N/A` may retain an Azure binding; `cloud: none` means no actual cloud
services. Select only needed shared stages; a default path does not authorize creation.

**One procedural owner.** The bound [development profile](development/default.md#policy-ownership)
owns the reusable setup/Resume/worker procedure. SDLC retains lifecycle and mandatory
controls; PLAN records app-specific decisions and real dependencies, not copied
instructions. Existing native project files remain the implemented dependency/recipe
sources; no separate requirements inventory or setup-state file is introduced.

**Reuse, override, refresh.** Users retain the ability to override settings or customize
local profiles. Subsequent invocations use the project copy, including later SEEDs;
validate unchanged settings and ask only about changed, missing, or inapplicable choices.
Do not repeat the full config interview or rewrite unchanged files. Shared-default
updates do not change existing projects. An explicit approved refresh may adopt them,
preserving user overrides and surfacing conflicts before changing customized files.
New environment rules require an approved profile/config update in existing projects;
do not recopy their tree, move resources or relabel mistaken new PLAN paths as legacy.
For approved adoption with older plans, record verified ownership in the current
plan referencing existing evidence where relevant to current work. Preserve original
artifacts; do not impose the new table format retroactively
or rewrite historical approvals. Existing unresolved ownership requires clarification.
Resetting an override is an explicit update from the local adopted defaults, not removal
of a required setting to trigger fallback.

**Incomplete or older config.** Required missing values/files are surfaced as incomplete
configuration, not silently filled from the library. Existing overrides-only projects
need explicit one-time materialization from their adopted defaults plus existing
overrides. If the adopted source cannot be established, escalate instead of guessing.

**Controls and history.** Validate effective selections against the active
`risk-calibration`, `policies`, and applicable compliance regime; inability to meet a
required control forces `Escalate` (core §3.2). Config values do not authorize Autopilot,
Parallel, or trust-boundary actions. Keep secrets outside this folder. Commit the
configuration to the project repo, never this library, and record resolution, updates,
refresh, or validated reuse per iteration in `meta/config`. Documentation references
to the methodology or vendor guidance are not configuration fallback sources.

## Folders

| Folder | Naming | What it binds |
|--------|--------|---------------|
| `harness/` | specific — `ghcopilot.md`, `claudecode.md` | the agentic coding tool: runtime modes, model + model-escalation, and the customization surfaces it exposes (instructions, custom agents, skills, MCP servers, prompts, hooks, delegate) |
| `devtools/` | generic bundles — `devtools-config1.md` (GitHub), `devtools-config2.md` (Azure DevOps) | repo + branch/PR model, CI/CD, code scanning / security, and the optional work-tracking mirror |
| `cloud/` | specific — `azure.md` (default), or `none` | cloud-service identity, IaC tooling, registry/provider; not automatic hosting authority |
| `development/` | `default.md` | native local execution, shared CI by default, optional cloud CD, self-contained environment IaC and shared verification recipes |
| `reusable-assets/` | `skills/` now; `best-practices/` guidance; room for `mcp-servers/`, `hooks/`, `prompts/` | reusable material a project pulls in — loadable capability (skills) and reference guidance (best-practices); **never authority** |
| `reusable-assets/best-practices/` | generic bundles — `bestpractices-profile1.md`, … (sections: agentic-dev, architecture, api-design, testing) | SHOULD-level craft guidance; named inputs to PLAN architecture and the agent's own conduct |
| `governance/policies/` | generic bundles — `policy-profile1.md`, … | internal org/engineering policy (data handling, access, retention, promotion) |
| `governance/compliance/` | `regulatory-controls.md` (the regime→control matrix) + regime bundles — `compliance-profile1.md`, … | external regulatory regimes (GDPR, HIPAA, SOC 2, PCI-DSS); **not a default binding** — a bundle selects the regimes; the matrix supplies the controls; bound by the risk level when a regime applies; ratchets controls up |
| `technical-stack/` | specific or empty | approved/preferred stack; empty by default so the agent proposes current standards |
| `ux/` | one profile file — `default.md` | UX quality-bar policy for UI-shipping iterations (accessibility target, design-skill/scan/evidence requirements, theme policy, usability testing); applies the selected [UX controls](risk-calibration/default.md#718-ux-controls) through [SDLC §10](../sdlc.md#10-ux-quality-bar) |
| `risk-calibration/` | one ladder file — `default.md` (the default; copy to author your own) | the methodology's own control ladder — which controls are mandatory at each level |
| `tokenomics/` | `build/` | build-time budget (all specializations); the product runtime budget is an `sdlc-for-agentic-apps` binding |

## Authoring a binding

Binding files come in two shapes, by folder:

**Provider bindings** — `harness/`, `devtools/`, `cloud/`. These name a tool/platform/cloud
that must *satisfy* TWTTY's controls, so each states:

1. **What it binds** — one or two lines.
2. **How it satisfies the TWTTY contract** — a table mapping each required control
   (reviewed/isolated merge, native independent verification, attributable commits, OIDC on the
   cloud seam, escalation destination) to how this provider meets it, and when to
   `Escalate` if it cannot.
3. **Stage hooks** — what the binding contributes at SEED / SPEC / PLAN / EXECUTE.
4. **Configuration surface** — the concrete settings/paths the agent should look up
   (kept thin; tool specifics evolve and are the agent's responsibility to verify against
   current vendor docs).

**Overlay / profile bindings** — `development/`, `risk-calibration/`, `policies/`, `compliance/`,
`best-practices/`, `technical-stack/`, `ux/`, `tokenomics/`. These *define* controls, guidance, or
budgets rather than naming a provider that must satisfy them, so each states:

1. **What it binds / defines** — and its category and status.
2. **The content** — the controls, guidance, regimes, stack, or budget itself (e.g. the
   `risk-calibration` matrices; a `policies` bundle's items; a `compliance` profile's regimes).
3. **Ratchet direction** where relevant — `policies` and `compliance` may raise the active
   `risk-calibration` controls, never relax them.
4. **How the AI Agent uses it** — at which stage, and that the plan/spec remains the source
   of truth (overlays are inputs, not a second source of truth).

See `CONTRIBUTING.md` at the repo root for the full authoring guide.

## License and disclaimer

Copyright 2026 Ajai Peddapanga. TWTTY material in this file is licensed under
[Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0); see TWTTY's
[NOTICE](https://github.com/ajai-d/twtty/blob/main/NOTICE). Independently authored
project content retains its own ownership and license. Include the license and
applicable notices when redistributing TWTTY material.

Provided "AS IS", subject to the license's warranty disclaimers and liability
limitations. AI-generated outputs may be incorrect or unsafe; validate results
before use. TWTTY does not guarantee security, regulatory compliance or production
suitability.
