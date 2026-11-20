# TWTTY — default configuration

This file holds the **shipped defaults** used to initialize a TWTTY project's capability
bindings. Defaults apply unless the Human User overrides them. Once materialized, the
project's complete local configuration supplies effective values; execution does not
look up omitted settings in this shared file.

```yaml
specialization: sdlc
overrides: none   # baseline root — every other specialization layers its addendum on top of this
```

## How this file is used

- **At the first SEED**, when no resolved project config exists, the AI Agent uses the
  shipped defaults for repository bootstrap. Existing projects use their local config.
  SEED does not interview the Human User about bindings.
- **During initial Discovery (SPEC)**, the AI Agent copies the whole config folder
  structure and files to `<project-folder>/twtty-runtime-config/`, merges the active
  specialization's config tree, and composes a complete local `default-config.md`.
  Nested mappings merge by key; specialization values override baseline defaults.
  Source inheritance is fully resolved in that local default file.
- **`runtimeconfig.md` uses the same binding keys and nesting** as the composed local
  defaults, with user override values substituted. It contains all effective settings,
  not only overrides. Config paths point to project-local files; spec-defined settings
  may reference the project's own spec. See the [README](README.md) for the full rules.
- **Later runs reuse the project configuration.** Authorized overrides update it;
  adopting newer defaults requires an explicit refresh that preserves customizations.
  Required missing settings are surfaced, never silently loaded from shared defaults.
- **This library file is never edited per project.** Its copied/composed project-local
  counterpart is an initialization/reset reference, not an automatic runtime fallback.

## Rules that govern every binding

1. **Reference local profiles after materialization.** Library keys identify the
   provider/profile files to copy. The project keeps the full config tree, and its
   effective bindings reference those local files rather than the shared library.
   Profile files carry tool-specific detail; the methodology is not hard-coded to it.
2. **Contract-or-Escalate.** Every **provider binding** (`harness`, `devtools`, `cloud`)
   MUST state how it satisfies the TWTTY controls required by the selected `risk-calibration`
   (reviewed/isolated merge, native independent verification, attributable commits, OIDC on the
   cloud seam, an escalation destination). If a chosen provider cannot meet a required
   control, the AI Agent MUST `Escalate` (core §3.2) and MUST NOT silently proceed.
3. **Ratchet up, never down.** The `policies/` binding and any applicable `compliance/` regime
   may *raise* the controls required by the active
   `risk-calibration`; they may never relax them.
4. **Spec metadata wins per iteration.** Where a per-iteration field exists (e.g. the spec
   `## Metadata` → `Runtime target` for cloud), it is the iteration-level confirmation and
   MUST point at the same provider the project binding names when hosting is selected.
   `N/A` means no application hosting, not prohibition of approved development services.

---

## Default bindings

```yaml
# --- where/how it runs -------------------------------------------------------
harness:        harness/ghcopilot.md          # the agentic coding tool (+ model, model-escalation)
devtools:       devtools/devtools-config1.md  # repo + CI/CD + security + work-tracking ecosystem (GitHub)
cloud:          cloud/azure.md                 # Azure service/provider binding; not hosting authority; none = no cloud services
development:    development/default.md         # native local loop + required shared CI; cloud CD opt-in

# --- control ladder ----------------------------------------------------------
risk-calibration:   risk-calibration/default.md   # the default L1-L5 ladder; SEED assesses the level (floor L1) and records it via meta/risk-level

# --- knowledge overlays (ratchet controls up, never down) --------------------
# compliance is NOT a default binding: the applicable regime is driven by the risk
# level; the risk-calibration level then binds a compliance/ profile.
policies:       governance/policies/policy-profile1.md    # internal org/engineering policy bundle
best-practices: reusable-assets/best-practices/bestpractices-profile1.md # bundle: PLAN architecture inputs + EXECUTE conduct (sections within)
technical-stack: none                          # empty by default: the AI Agent proposes current standards
ux:             ux/default.md                  # UX quality-bar policy for UI-shipping iterations (overlay; see sdlc.md §10)

# --- reusable assets (harness-loaded) ----------------------------------------
# skills: a DIRECTORY. The agent inspects every skill file in it and applies the ones that are
# applicable; each skill file describes its own capability and when it is relevant (loose coupling).
reusable-assets:
  skills: reusable-assets/skills/              # directory of skills; "" = no skills
  # mcp-servers: reusable-assets/mcp-servers/  # (future) directory of MCP server bindings
  # hooks: reusable-assets/hooks/              # (future) directory of hooks

# --- tokenomics --------------------------------------------------------------
tokenomics:
  build:   tokenomics/build/build-profile1.md  # build-time budget (agent tokens / $ / wall-clock)
  # product runtime budget is an sdlc-for-agentic-apps binding (that specialization's config)

# --- escalation & execution defaults -----------------------------------------
# Discovery records the Human's Sequential/Parallel answer and any concurrency cap.
# PLAN reuses that answer and checks concrete eligibility; do not ask twice.
# Execution Mode (Interactive/Autopilot) is independent and offered at PLAN start.
# Defaults alone grant neither Parallel execution nor Autopilot.
escalation:        pr-comment                  # pr-comment | github-issue | teams | slack | email
execution-mode:    interactive                 # interactive | autopilot (autopilot is opt-in, after SEED)
execution-pattern: sequential                  # sequential | parallel (parallel is opt-in, Human-User-authorized)
concurrency-cap:   5                            # max concurrent subagents during a parallel burst (<= 5)
```

---

## What each binding governs

| Key | Governs | Default rationale |
|-----|---------|-------------------|
| `harness` | agent runtime + customization surfaces | GitHub Copilot — the current reference harness |
| `devtools` | repo/branch/PR, CI/CD, code scanning, work-tracking mirror | GitHub ecosystem |
| `cloud` | service identity, IaC and cloud delivery controls | Azure provider; does not select hosting; `none` for no cloud services |
| `development` | local execution, required CI, optional CD, environment paths and shared recipes | native inner loop + CI protecting main; CD disabled |
| `risk-calibration` | the risk ladder + control matrices | L1 floor; raised at SEED per project |
| `policies` | data controls, promotion/break-glass guardrails | baseline internal policy |
| `best-practices` | architecture inputs (PLAN) + the agent's conduct (EXECUTE) | bestpractices-profile1 loaded |
| `technical-stack` | technology choices (PLAN) | empty — agent proposes current |
| `ux` | UX quality-bar policy for UI-shipping iterations (accessibility target, design-skill/scan/evidence requirements, theme policy, usability testing) | [`ux/default.md`](ux/default.md) — applies the selected [UX controls](risk-calibration/default.md#718-ux-controls) through SDLC §10 |
| `reusable-assets` | customization surfaces (portable skills, later MCP/hooks) | `skills/` directory inspected; applicable skills applied |
| `tokenomics.build` | Autopilot cost guardrail, token/context efficiency | no caps by default |
| `escalation` | `Escalate` destination (core §3.2) | PR comment |
| `execution-mode` / `-pattern` / `concurrency-cap` | execution mode & pattern | Interactive, Sequential, cap 5 |
