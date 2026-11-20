# SDLC Specialized Implementation

> This document extends the [Core TWTTY Specification](../../core-twtty-methodology.md). It MUST NOT weaken the core's approval rules, stage order, or traceability requirements (see [core — Core TWTTY Specification vs. Specialization](../../core-twtty-methodology.md#core-twtty-specification-vs-specialization)).

> Copyright © 2026 Ajai Peddapanga. Licensed under
> [Apache License 2.0](../../../../LICENSE) — see
> [NOTICE](../../../../NOTICE). Suggested citation: Peddapanga, A. (2026).
> *TWTTY: SDLC Specialized Implementation.*
> https://github.com/ajai-d/twtty.

## In this document

| Section | Purpose |
|---------|---------|
| [1. Purpose](#1-purpose) | What this implementation is and how it maps to the core stages |
| &nbsp;&nbsp;&nbsp;&nbsp;[1.1 Capability bindings (config)](#11-capability-bindings-config) | The tool-agnostic binding model: categories, the two config files, and the binding rules |
| [2. Pipeline summary](#2-pipeline-summary) | Visual summary of the SDLC pipeline |
| [3. Stage and stage task details](#3-stage-and-stage-task-details) | Stage tasks, agent roles, outputs, and stage exit gates |
| [4. Artifact locations](#4-artifact-locations) | Where each stage's artifacts are written |
| [5. Runtime profile](#5-runtime-profile) | The bound harness, agent modes, and customization surfaces |
| [6. Guardrails profile](#6-guardrails-profile) | Guardrail categories negotiated during PLAN |
| [7. Risk enforcement profile](#7-risk-enforcement-profile) | Applicable stage tasks, gate strictness, and context isolation per risk level |
| &nbsp;&nbsp;&nbsp;&nbsp;[7.1 Risk calibration matrix](#71-risk-calibration-matrix) | Level-tiered controls within each applicable stage task |
| [8. SDLC-specific rules](#8-sdlc-specific-rules) | Rules specific to software delivery |
| [9. Execution rules](#9-execution-rules) | Software-delivery extensions to the core execution rules |
| [10. UX quality bar](#10-ux-quality-bar) | Quality profile for iteration scopes with user-facing UI |
| [11. API quality bar](#11-api-quality-bar) | Quality profile for iteration scopes shipping a network API |

---

## 1. Purpose

This document is a Software Development Life Cycle (SDLC) specialized implementation of the [Core TWTTY Specification](../../core-twtty-methodology.md). It maps the four canonical TWTTY stages (`SEED → SPEC → PLAN → EXECUTE`) to concrete stage tasks, artifacts, agent roles, and approval gates for software delivery. In this implementation, EXECUTE includes delivery and operations.

For iterations with LLM-driven behavior that cannot be fully validated by deterministic pass/fail tests alone, use the extension at [../sdlc-for-agentic-apps/sdlc-for-agentic-apps.md](../sdlc-for-agentic-apps/sdlc-for-agentic-apps.md). Baseline SDLC remains the default unless Discovery selects that extension.

### 1.1 Capability bindings (config)

This specialization is **tool-agnostic**: the document below states *what* must hold (obligations, gates, controls); the [config library](config/README.md) supplies the initial defaults for *which* tools, platforms, clouds, risk tiers, and knowledge a project binds those obligations to. After resolution, "the bound `harness`", "the bound `devtools`", "the active `risk-calibration`", etc., refer to the project's complete local configuration, not a live lookup into the shared library.

**Default source and project configuration.** The AI Agent uses shipped defaults for initial bootstrap and materializes the project-specific configuration during Discovery:

| File | Written by | When | Role |
|------|-----------|------|------|
| [`config/default-config.md`](config/default-config.md) | shipped | initial bootstrap | Defaults for the first SEED when no resolved project configuration exists. Existing projects use their local configuration. |
| `<project-folder>/twtty-runtime-config/` | the AI Agent, via the **[Config interview](#config-interview)** | **Discovery (SPEC)**, then authorized updates | A complete project-local config tree, with composed `default-config.md`, fully resolved `runtimeconfig.md`, all config files, and a project README. Active after resolution; recorded in `meta/config`. |

**Complete local copy.** Materialization MUST copy the whole baseline `config/` folder structure and files into **`<project-folder>/twtty-runtime-config/`**, including unchanged defaults and unselected provider/profile files, then merge the active specialization's config tree. Compose the source default-config chain into a complete project-local `default-config.md`; merge nested mappings by key so an addendum such as `tokenomics.product` does not discard `tokenomics.build`. Source-chain `overrides` references are resolved during composition, not followed during project execution. Configuration-file references MUST resolve within the project tree; normalize copied config references where necessary. References to methodology or vendor documentation do not provide runtime configuration fallback. Generate the project's `README.md` from [the runtime-config README template](config/runtime-config-readme-template.md).

Copied profiles are not automatically active; only resolved bindings select which apply. Copying a provider or skill definition does not install tooling or grant permissions.

**Same structure, effective values.** `runtimeconfig.md` MUST retain the composed default configuration's binding keys and nesting, including `specialization`, `reusable-assets`, and `tokenomics`, with approved override values substituted. It is the complete effective configuration, not an overrides-only document or a separate override schema. Users MAY override individual settings and customize project-local binding/profile files within the existing approval and control rules. Runtime selections without defaults are recorded as they become known; later PLAN/runtime choices update the local configuration without requiring them to be decided prematurely. Record explicitly overridden setting names and customized profiles in `meta/config`, without introducing a second authoritative set of current values. File-backed selections use project-local relative paths; spec-defined selections, such as a product cost budget, retain references to the project's own spec.

**Use and refresh.** After materialization, every invocation, including a later SEED, MUST use the project-owned configuration and profiles. A missing required setting or config file MUST be surfaced as incomplete configuration, not silently supplied from shared TWTTY defaults. An unchanged snapshot is reused and validated, not recopied or re-interviewed. Adopting newer defaults requires an explicit approved refresh that preserves user overrides and customized files; do not silently overwrite them. Existing overrides-only projects require an explicit one-time materialization from their adopted defaults and existing overrides. If that source is unavailable or ambiguous, escalate rather than substituting current library defaults. The config folder is committed to the project's repository, never this shared library; `meta/config` records resolution and reuse per iteration.

**Binding categories.** Each is a selection from the correspondingly-named folder in the config library; the "Specified in" column is where this document consumes it:

| Binding | What it binds | Specified in |
|---------|---------------|--------------|
| [`harness`](config/harness/) | the agentic coding tool that plays the agent roles (+ model, customization surfaces) | [§5 Runtime profile](#5-runtime-profile), [§5.2](#52-customization-surfaces-and-runtime-features) |
| [`devtools`](config/devtools/) | repo + remote, branch/PR, CI/CD, code scanning, work-tracking mirror | [§3.1](#31-seed), [§4](#4-artifact-locations), [§7.1 risk calibration matrix](#71-risk-calibration-matrix), [§8](#8-sdlc-specific-rules), [§9](#9-execution-rules) |
| [`cloud`](config/cloud/) | service identity, IaC language, registry/provider (or `none` = no cloud services); not automatic hosting authority | [§7.1.7](#717-identity-and-access-controls), [§9](#9-execution-rules); hosting `Runtime target` in spec `## Metadata` |
| [`development`](config/development/default.md) | native local execution, required shared CI, optional CD, isolated environment IaC and shared recipes | [Config interview](#config-interview), [§3.4](#34-execute), [§3.6](#36-existing-project-preparation) |
| [`risk-calibration`](config/risk-calibration/) | the L1–L5 control ladder and its matrices | [§7 Risk enforcement profile](#7-risk-enforcement-profile) |
| [`policies`](config/governance/policies/) | internal org/engineering policy (ratchets controls up) | [§6](#6-guardrails-profile), [§9](#9-execution-rules) |
| [`compliance`](config/governance/compliance/) | external regulatory regimes — **not a default binding**; bound by the risk level when a regime is confirmed at `spec §14` | [§7.1.8](#718-regulatory-overlay-controls-conditional) |
| [`best-practices`](config/reusable-assets/best-practices/) | PLAN architecture inputs + the agent's own conduct | [§6](#6-guardrails-profile), [§9](#9-execution-rules) |
| [`technical-stack`](config/technical-stack/) | approved/preferred stack (empty → agent proposes current) | PLAN §1.5 (via [plan template](templates/plan-template.md)) |
| [`reusable-assets`](config/reusable-assets/) | portable harness-loaded assets (skills, later MCP/hooks) | [§5.2](#52-customization-surfaces-and-runtime-features) |
| [`tokenomics`](config/tokenomics/) | build-time budget (all specializations); the product runtime budget is an `sdlc-for-agentic-apps` binding | [§8.1.1](#811-additional-meta-entries), [§9](#9-execution-rules) |

**Binding rules (normative).**

1. **Contract-or-Escalate.** Each **provider binding** (`harness`, `devtools`, `cloud`) states how it satisfies the controls the active `risk-calibration` requires. If a selected binding cannot satisfy a required control, the AI Agent MUST `Escalate` per [core §3.2](../../core-twtty-methodology.md#32-failure-handling) rather than silently degrade (see [§9 Honor the active bindings](#9-execution-rules)). (Overlay bindings — `development`, `policies`, `compliance`, `best-practices`, `technical-stack`, `tokenomics`, and the `risk-calibration` itself — *define* controls, guidance, or budgets rather than satisfy them.)
2. **Ratchet up, never down.** The `policies` binding and any confirmed `compliance` regime may *raise* the controls required by the active `risk-calibration`; they may never relax them.
3. **Spec metadata wins per iteration.** The spec `## Metadata` `Runtime target` confirms the hosting provider and matches the `cloud/` selection when hosting is selected. `N/A` means no application hosting; an Azure provider binding may still support approved local-development services.

Beyond the folder bindings above, defaults include `escalation`, `execution-mode`, `execution-pattern` and `concurrency-cap`. Discovery records the Human's Sequential/Parallel choice and any cap; PLAN reuses that answer and checks concrete eligibility under §5.1, without asking again. The separate core-mandated Execution Mode offer (Interactive/Autopilot) remains at PLAN start; a configuration default alone does not grant Autopilot or Parallel.

**Specialization config addenda.** A specialized implementation that introduces its own bindings MAY ship a config **addendum** at its `config/default-config.md` — for example [`sdlc-for-agentic-apps/config/default-config.md`](../sdlc-for-agentic-apps/config/default-config.md) (product-tokenomics binding + an agentic-evaluation `risk-calibration-delta` overlay) and [`dataeng/config/default-config.md`](../dataeng/config/default-config.md) (a data-engineering `risk-calibration-delta` overlay). Each addendum declares, in a short YAML header, its own `specialization` and the baseline `default-config.md` it `overrides` (the baseline itself declares `overrides: none`). A `risk-calibration-delta` overlay adds specialization control rows **on top of** the baseline `risk-calibration` ladder — it never restates or relaxes the baseline rows. Resolve this chain during initial materialization or an approved refresh, composing baseline and specialization defaults before applying user overrides. Subsequent execution reads the complete project-local configuration and copied profiles, not the shared inheritance chain.

---

## 2. Pipeline summary

This section is a visual summary. [Section 3](#3-stage-and-stage-task-details) defines stage/task contracts and gates. EXECUTE rows are a task catalog, not numeric execution order; development preparation follows the bound profile under §3.4 and the approved PLAN.

```text
                              TWTTY SDLC Pipeline

    SEED ─────▶ SPEC ─────▶ PLAN ─────────────────────────────▶ EXECUTE
   Intent    Requirements  Strategy            Build + Validate + Deploy + Operate

  +-----------+--------------------------+----------------------+--------------------------------------+
  |   SEED    |           SPEC           |         PLAN         |               EXECUTE                |
  +-----------+--------------------------+----------------------+--------------------------------------+
  | 0a Intent | 1a Discovery interview   | 2a Architecture      | 3a Setup                             |
  |           | 1b Draft specification   | 2b Design            | 3b Implement                         |
  |           |                          | 2c Orchestration     | 3c Code review                       |
  |           |                          |                      | 3d Code scanning                     |
  |           |                          |                      | 3e Security                          |
  |           |                          |                      | 3f Test                              |
  |           |                          |                      | 3g CI/CD pipeline                    |
  |           |                          |                      | 3h Infrastructure as code            |
  |           |                          |                      | 3i Deployment                        |
  |           |                          |                      | 3j Smoke tests                       |
  |           |                          |                      | 3k Monitoring                        |
  |           |                          |                      | 3l Observability                     |
  |           |                          |                      | 3m Iteration                         |
  +-----------+--------------------------+----------------------+--------------------------------------+
  | seed/     | spec/spec.md             | plan/plan.md         | repository source / tests / infra /  |
  | seed.md   | spec/spec-<id>.md        | plan/plan-<id>.md    | CI config  (see Artifact locations)  |
  | intent-   | ...                      | ...                  |                                      |
  |  <id>.md  |                          |                      |                                      |
  +-----------+--------------------------+----------------------+--------------------------------------+
  | replay-execution/ (the baseline log execution-log.md, plus one log per iteration; appended throughout) |
  |   execution-log.md   ·   <id>-execution-log.md   ...        (baseline + one file per iteration)       |
  |   — within each scope, the log MAY be time-period-chunked as                                         |
  |     execution-log-<period>.md / <id>-execution-log-<period>.md (optional; see core §2)               |
  +----------------------------------------------------------------------------------------------------+
                                                                                  │
                              ◀──── Feedback loop ── next iteration ────────────────┘
```

Above, `spec.md`/`plan.md` are the **baseline buildout** (unnumbered), and `<id>` is a generated `Iteration-<YYYYMMDDTHHMMSSZ>-<token>` assigned to a **later** iteration (see [core §4.2/§4.3](../../core-twtty-methodology.md#43-on-new-iteration)).

Each stage is informed by the prior stage output. No stage begins until the prior stage's exit gate (`SEED-EXIT`, `SPEC-EXIT`, `PLAN-EXIT`, or `EXECUTE-EXIT`) is approved.

The EXECUTE stage tasks listed above are the **default** set. The Planning Agent tailors the applied EXECUTE subset to the project's risk level per [Section 7 — Risk enforcement profile](#7-risk-enforcement-profile), which is the single source of truth. SPEC and PLAN stage tasks apply at every risk level.

---

## 3. Stage and stage task details

### Default agent as orchestrator

The default agent of the **bound harness** applies the TWTTY method recursively. Before producing the artifact for any stage task, the default agent decides which of the bound harness's customization surfaces is needed — instructions files, custom agents, skills, MCP servers, hooks, or prompt files (see §5.2) — and configures it through a TWTTY loop, recording each configuration decision in the replay-execution log. In particular, the ROLE column of stage-task tables (e.g., "Spec Agent", "Architecture Agent", "Setup Agent") may be fulfilled by the default agent itself or by a dedicated custom agent that the default agent configures on demand. **Agent column names in stage-task tables denote ROLES, not mandated identities** — this principle applies across §3.1 Seed, §3.2 Spec, §3.3 Plan, and §3.4 Execute.

> **For the Human User: this is invisible by default.** The default agent makes customization decisions on your behalf and only surfaces them when it needs your input — specifically when a customization crosses a trust boundary. A trust boundary is crossed when the customization installs an MCP server, adds a hook that runs shell commands, or grants an agent tools that read/write files outside the workspace root, execute shell commands, make network requests to non-project domains, or modify user or system settings. All other decisions (instructions, prompt files, skills, and low-risk custom agents) are silent; the created files are always visible in the repository for later review. The terms "default agent", "custom agent", "customization surface", "ROLE", and "TWTTY loop" are internal vocabulary — you should never have to learn them to use this methodology. If the default agent ever asks you about a customization, it MUST explain *why* in plain language and offer to proceed with a safe default if you prefer not to engage with the question.

Examples (illustrative, not prescriptive):

- **Seed (3.1)**: usually fulfilled by the default agent — small, conversational, no specialization needed.
- **Spec (3.2)**: default agent often suffices; a custom Spec Agent may help on large or regulated projects.
- **Plan (3.3)**: a project with multiple architects may benefit from separate Architecture, Design, and Planning agents; a small project rarely does.
- **Execute (3.4)**: separate Setup, Test, Security, and Deploy agents may pay off when the project is large enough that tool restrictions and specialized instructions reduce errors. Otherwise, the default agent handles the lifecycle.

### Grounding on a prior reverse-engineering assessment

If the target already contains a reverse-engineering assessment — for example a
`twtty/assessment/` produced by the [reverse-engineering specialization](../reverse-engineering/reverse-engineering.md) —
the AI Agent MUST read it first and use it to ground every TWTTY stage (SEED,
SPEC, PLAN, and EXECUTE) rather than re-deriving the system from scratch. Treat
the assessment as current-state evidence: honor its claim states (`Verified`,
`Inferred`, `Contradicted`, `Unknown`, `Proposed`) and recorded limitations,
prefer its cited sources, and re-verify any claim the work materially depends on
before relying on it. This grounding informs the Seed's intent and scope, the
Spec's requirements, the Plan's architecture, and Execute's changes; it does not
replace any stage task, gate, or approval. When no such assessment is present,
the pipeline proceeds normally.

### 3.1 Seed

| Stage task | Agent | Output |
|------------|-------|--------|
| 0a. Intent | Human User (with AI Agent assistance per [core §4.2](../../core-twtty-methodology.md#42-on-first-contact)/[§4.3](../../core-twtty-methodology.md#43-on-new-iteration)) | **Baseline buildout (first contact):** the **project seed** `<project-folder>/seed/seed.md` — a copy of [`framework/templates/seed-prompt-template.md`](../../../templates/seed-prompt-template.md) with both required sections (`## What I Want To Build` and `## Done Looks Like`) completed; the Human User authors it. **Later Iteration:** that iteration's **Iteration Intent** `<project-folder>/seed/intent-<iteration-id>.md` — a short statement of what the increment adds, changes, or fixes — which the AI Agent MAY scaffold and the Human User edits and approves. |

At **first contact** (the baseline buildout) the Human User approves the **Project Seed**, whether building new software or refactoring existing code; confirm risk and calibrate before recording `SEED-EXIT` per core §4.2. The baseline produces **unnumbered** artifacts (`spec/spec.md`, `plan/plan.md`, `replay-execution/execution-log.md`). A **later Iteration** requires the approved original Project Seed, verified initial baseline completion and its own approved **Iteration Intent** under [core §4.3](../../core-twtty-methodology.md#43-on-new-iteration). No original seed or baseline is omitted or invented. All applicable stages and gates remain mandatory.

**Repository bootstrap (first contact).** Establish or reuse version control before
`SEED-EXIT` per core §4.2. For a new repository only, initialize Git (`main` by default),
the approved devtools remote and minimal `.gitignore`. For an existing repository,
preserve history, remotes, configured integration branch and protection/review rules;
do not reinitialize or disable protection. Propose a concrete repository name from
the confirmed project slug and the bound provider's known namespace/visibility rules;
show the proposed destination with confirm/edit choices before creation. Reuse an
approved existing remote without asking settled destination questions again. Unknown
ownership, permissions or a name conflict needs focused resolution, not silent reuse,
overwrite or suffixing. Publish the approved seed through its
authorized process, including PRs and required CI/reviews where applicable. The original
Project Seed and full baseline remain mandatory. Fuller missing app/repository setup
remains at 3a; reuse existing setup. Use native Git/platform evidence and direct artifact
review, not generated validation tooling before early gates. Existing bindings apply;
shipped defaults initialize only a project with no resolved config. Discovery resolves
project choices, without authorizing app implementation or provisioning before PLAN.

**Stage exit gate (`SEED-EXIT`).** The SEED artifact is the **project seed** (`seed/seed.md`) at first contact (the baseline buildout), or the **Iteration Intent** (`seed/intent-<iteration-id>.md`) for a later Iteration. All six conditions MUST hold; the AI Agent MUST verify conditions 1–5 mechanically before requesting approval for condition 6:

1. The SEED artifact exists at its canonical path (the project seed `<project-folder>/seed/seed.md` at first contact; the Iteration Intent `<project-folder>/seed/intent-<iteration-id>.md` for a later Iteration).
2. The project seed contains both required `## What I Want To Build` and `## Done Looks Like` H2 sections; an Iteration Intent states what the increment adds, changes, or fixes.
3. No section of the SEED artifact contains the template placeholder text (`[Describe your project...]`, `[How will you know it's complete?...]`), and it contains non-whitespace content.
4. The project repository has a configured approved remote (per [§9](#9-execution-rules)), and the SEED artifact is committed and published through its authorized integration process. Reuse the existing integration branch and required PR/CI/review controls; `main` is the new-repository default, not a requirement to rename or bypass an existing branch.
5. A verified `meta/risk-level` entry applies to this scope before its `SEED-EXIT` record. First baseline work requires risk assessment/confirmation; later Iterations may carry forward verified applicable calibration, never an invented level. A later Iteration also requires the approved original Project Seed and verified initial baseline completion per core §4.3.
6. The Human User's `Approval outcome` is `Approved` or `Approved with changes` (per [core §2 — Replay-execution log format](../../core-twtty-methodology.md#replay-execution-log-format)).

**Replay-log entry on `SEED-EXIT`:**
- `<stage>/<stage-task>` = `seed/0a`
- `<approval-gate-name>` = `SEED-EXIT`
- `Artifact / path changed` MUST be `<project-folder>/seed/seed.md` (baseline buildout) or `<project-folder>/seed/intent-<iteration-id>.md` (a later Iteration)

### 3.2 Spec

| Stage task | Agent | Protocol | Output |
|------------|-------|----------|--------|
| 1a. Discovery interview | Spec Agent | Discovery (core [§1](../../core-twtty-methodology.md#interview-me)) | Discovery transcript at `<project-folder>/replay-execution/<iteration-id>-discovery-transcript.md` containing either (Interactive mode) verbatim Q&A across the four rounds or (Delegated mode) the AI-drafted chunks and Human User approvals or refinements, plus the AI Agent's rationale for every non-trivial choice. Per [core §1](../../core-twtty-methodology.md#interview-me), individual questions, answers, and per-round chunks are NOT logged as separate replay-log entries; they are recorded verbatim in the transcript. 1a produces exactly one **`spec/1a` stage-task** replay-log entry, recorded on interview termination (see below); the Discovery config interview additionally appends a `meta/config` entry, which is a separate `meta/*` entry (see [§8.1.1](#811-additional-meta-entries)), not a `spec/1a` stage-task entry. |
| 1b. Draft specification | Spec Agent | TWTTY loop (core [§1](../../core-twtty-methodology.md#the-twtty-loop)) | Draft sections 1–8 of `<project-folder>/spec/spec-<iteration-id>.md` from the [spec template](templates/spec-template.md) in one coherent pass. Baseline specs include all applicable required content; later Iterations include only the sections and detail needed for the approved Iteration Intent. The AI MAY chunk drafting only when the content is too large for one pass. |

Acronyms used in the table: **FR** (Functional Requirements), **NFR** (Non-Functional Requirements), **AC** (Acceptance Criteria), **UC** (Use Case).

The baseline buildout writes `<project-folder>/spec/spec.md`; each later Iteration writes `<project-folder>/spec/spec-<iteration-id>.md` (see [core §4.3](../../core-twtty-methodology.md#43-on-new-iteration)).

**Intra-stage stage task 1a.** Discovery is approved through its Discovery protocol cycle and produces a replay-execution log entry with `<approval-gate-name>` = `—`. Approval of the complete specification at 1b triggers `SPEC-EXIT`.

**Legacy SPEC continuation.** If an existing scope stopped during the former
`1b`/`1c`/`1d` drafting sequence, retain its approved discovery and drafted
content, complete and validate the specification through the current `1b`,
and append its `SPEC-EXIT` entry. Do not create another Iteration or rewrite
historical entries. A previously approved `SPEC-EXIT` remains valid.

**Discovery and drafting performance goals.** For typical small/medium iterations:

| Operation | Agent-time goal |
|-----------|-----------------|
| Complete discovery, including all four rounds | `10m` total |
| Complete first spec draft, including required pre-gate checks | `5m` |

Measure discovery from entry into `1a` until discovery termination is approved, and drafting from that approval until the first complete, checked draft is ready for review. Exclude Human response time and explicit pauses; include model and tool time. Chunking does not reset the clock.

These are performance goals, not hard caps. Quality takes precedence: the AI Agent MUST NOT skip discovery rounds, necessary clarification, applicable requirements, verification, or approvals; truncate output; weaken acceptance criteria; or falsely claim completion to meet a target. Continue the required work when more time is needed. Existing hard-budget and escalation rules remain unchanged. At the next existing budget checkpoint, report measured durations and any missed goal with its known cause or `unknown`, without adding a separate approval or documentation cycle. Unavailable timings MUST NOT be reported as meeting the goals.

**Specialization is selected by the start command's `type=` parameter — not by a routing question.** The Human User selects one of the shipped specializations up-front via `twtty start project type=<specialization> …` (see the [TWTTY command dispatcher](../../../twtty.md) and [README quick start](../../../../README.md#quick-start)). `type=` names exactly one of:

- [`sdlc`](../sdlc/sdlc.md) (this document) — standard software delivery
- [`sdlc-for-agentic-apps`](../sdlc-for-agentic-apps/sdlc-for-agentic-apps.md) — LLM-driven applications
- [`dataeng`](../dataeng/dataeng.md) — data pipelines
- [`reverse-engineering`](../reverse-engineering/reverse-engineering.md) — read-only assessment of an existing system

The Spec Agent MUST record the selected specialization in the spec's `## Metadata` `Specialization` field to match: `baseline SDLC`, `sdlc-for-agentic-apps`, or `dataeng`. No Discovery-time routing question is asked; Discovery has three upfront questions (Discovery mode, UX mode, API mode). **These three questions are a hard precondition on the whole SPEC stage, enforced at the front — not only at the exit gate.** Put all three to the Human User as the **first action of `spec/1a`** after reading the approved Project Seed and, for a later Iteration, its approved Iteration Intent. Missing required intent blocks discovery. Read referenced existing artifacts only after the mode answers and before relying on them in discovery. Do not elicit or draft spec content before those answers. Execution-Mode authorization is not an answer; do not infer/default these modes, and only explicit Human delegation selects Delegated. Record the answers before Round 1 in the transcript, referencing them in the single discovery-termination `spec/1a` entry. No preliminary `spec/1a` entry is permitted. Content produced prematurely is a stage violation; the [SPEC-EXIT checklist](templates/spec-template.md#spec-exit-validation-checklist) is a backstop, not permission to defer enforcement.

**Shared mode-selection mechanic (Discovery, UX, API).** All three upfront questions use the same mechanic: **Delegated** (the AI Agent decides and discloses every non-trivial choice with rationale — silent adoption is prohibited), **Interactive** (the Human User co-decides each choice with the AI Agent), and — for UX ([§10](#10-ux-quality-bar)) and API ([§11](#11-api-quality-bar)) only — **N/A** (the quality bar does not apply to this iteration). A Human User response of "you decide" or equivalent selects Delegated by definition. Each confirmed mode is recorded in the spec's `## Metadata` section. §10 and §11 apply this mechanic to their respective dimensions and do not restate it.

**Four independent axes — do not confuse them.** TWTTY has four orthogonal mode axes, and three of them offer an option literally named *Interactive*. They are independent: a project can be (say) Autopilot execution + Delegated discovery + Interactive UX + N/A API all at once.

| Axis | Options | Governs | Defined in |
|------|---------|---------|-----------|
| **Execution Mode** | Interactive · Autopilot | Who satisfies each Approval Gate (human vs. self-approving agent) | [core §1](../../core-twtty-methodology.md#execution-modes) |
| **Discovery Mode** | Interactive · Delegated | How the discovery interview is conducted | [core §1 Interview Me](../../core-twtty-methodology.md#interview-me) |
| **UX Mode** | Interactive · Delegated · N/A | How UX requirements are produced | [§10](#10-ux-quality-bar) |
| **API Mode** | Interactive · Delegated · N/A | How API requirements are produced | [§11](#11-api-quality-bar) |

"Interactive" always means *the Human User co-decides*; "Delegated" always means *the AI Agent decides and discloses*. Only the axis changes what is being decided.

**Mismatch check (safety net).** Before beginning Round 1, the Spec Agent MUST scan the seed for signals that clearly indicate a different specialization than the bootstrap selected — for example, a seed describing an LLM-driven chatbot while the bootstrap selected baseline SDLC, or a seed describing a data-warehouse ETL while the bootstrap selected agentic. On detected mismatch, the Spec Agent MUST surface the mismatch to the Human User, propose switching to the correct specialization, and require the Human User to `Abandon` this session and re-bootstrap with the correct prompt before proceeding.

**Discovery coverage dimensions.** These dimensions implement the [core §1 required-coverage rule](../../core-twtty-methodology.md#interview-me). Baseline discovery addresses each dimension or records a Human-confirmed N/A. For later Iterations, consider each dimension's relevance to the approved intent, write only the affected content, and carry forward unchanged approved requirements without restatement or N/A filler. Relevant requirements and applicable controls MUST still be covered before `SPEC-EXIT`.

- User personas and primary use cases
- Functional requirements
- Non-functional requirements (performance, security, compliance, accessibility, observability)
- Integration points and external dependencies
- Data model and data lifecycle
- Failure modes and error handling
- Success metrics and evaluation strategy
- Explicit out-of-scope items
- Constraints (budget, timeline, team, existing systems)

Extensions to this implementation (for example, [sdlc-for-agentic-apps](../sdlc-for-agentic-apps/sdlc-for-agentic-apps.md), [dataeng](../dataeng/dataeng.md)) add further dimensions via their spec addendum sections.

**Domains (identify).** As part of the technical specification, the Spec Agent records the domains it derives from the requirements per [§8.2](#82-domain-based-separation-of-responsibilities): the areas of responsibility (each a name and a one-line responsibility), the layer map (business domains plus the app-platform and infra layers where they apply), and the domain each use case and requirement belongs to. **A single-domain iteration is a single `spec-<iteration-id>.md`.** A multi-domain iteration uses a hub-and-spoke spec: an overview `spec/spec-<iteration-id>.md` (goals, the domain and layer map, cross-domain journeys, and links — interfaces are declared later in the plan, §3.3) plus one file per domain `spec/domains/<domain>-<iteration-id>.md` (that domain's use cases, FR, NFR, ACs); whole-system foundations (data classification, plus the whole-system UX (§13) and API (§15) requirements) stay in the overview. The AI Agent derives the split and the Human User reviews or overrides it in plain language; the Human User is never asked to reason in domain-modelling terms. A spec is never split by document type. See the design-decision note atop the [spec template](templates/spec-template.md).

#### Config interview

**Delivery choice.** Apply the bound [development profile's Discovery rules](config/development/default.md#discovery-and-configuration) in this existing interview, not another interview. Keep provider/service needs, application hosting and environment ownership distinct. Read-only assessments must not install workflows/protection into their investigated target.

Discovery and PLAN establish service requirements and approved boundaries, not mandatory
instance/connection details. Instance reuse/creation follows the profile's
[infra-kickoff procedure](config/development/default.md#development-infrastructure-first)
during EXECUTE. No provisioning or executable IaC before PLAN approval.

As part of **1a Discovery**, the Spec Agent resolves the project's capability bindings per [§1.1](#11-capability-bindings-config). For the first resolution, propose the shipped defaults as a coherent configuration and elicit only missing preferences, requested overrides, and decisions requiring explicit approval. Materialize the complete baseline-plus-specialization config tree, a composed local `default-config.md`, and a same-structure `runtimeconfig.md` containing all effective settings and approved override values. Generate the project README from [`runtime-config-readme-template.md`](config/runtime-config-readme-template.md).

**Finalize after materialization.** Within this existing config interview, materialize
the authorized candidate as a draft, then show its actual effective settings and
clickable local files, highlighting overrides and model/stack choices still provisional
until PLAN. Offer one **Use these settings / Customize settings** decision; resolve
requested changes and required approvals before recording `meta/config`. Do not add a
lifecycle gate, per-file/per-setting interview or second configuration layer. An earlier
valid approval remains valid; unchanged configuration on Resume needs no repeated prompt.

For later iterations, validate the existing project configuration against the current intent, risk level, policies, and confirmed regulatory scope. Reuse unchanged applicable choices; interview only for changed, missing, or no-longer-applicable settings. Do not recopy the library or rewrite unchanged config/README files. User overrides remain available during later stages and runtime; approved changes update the local effective values and relevant files, then append a fresh `meta/config` entry. Refreshing defaults or materializing an older overrides-only project requires explicit approval and preserves its overrides. These rules do not replace the required Discovery/UX/API mode questions or PLAN Execution Mode offer. Capture Sequential/Parallel once in the existing Discovery/config interview if not already answered; Sequential is the recommendation. Reuse that Human answer at PLAN, not a second pattern question. An approved config value without Human selection is not a Parallel grant.

Every effective selection MUST satisfy the confirmed `risk-calibration`, `policies`, and any applicable compliance regime; otherwise escalate per [core §3.2](../../core-twtty-methodology.md#32-failure-handling). Configuration values do not themselves authorize Autopilot, Parallel execution, or trust-boundary actions. Record the resolved configuration or validated reuse in this iteration's `meta/config` entry, and capture interview questions/answers in the discovery transcript rather than separate replay entries.

**Discovery interview (1a) termination.** The interview MUST end with an explicit termination prompt approved by the Human User. The Spec Agent proposes: *"End of discovery; proceed to 1b Draft specification."* On approval, the agent appends exactly one replay-log entry for 1a (`spec/1a`, `<approval-gate-name>` = `—`, `Execution outcome:` = `end of discovery`, `Artifact / path changed:` = `<project-folder>/replay-execution/<iteration-id>-discovery-transcript.md`). This is the only `spec/1a` log entry produced; per [core §1](../../core-twtty-methodology.md#interview-me) individual questions, answers, and per-round chunks are NOT logged as separate replay-log entries; they are recorded verbatim in the transcript file. 1b MUST NOT start before this entry is recorded.

**Stage exit gate (`SPEC-EXIT`).** All four conditions MUST hold; the AI Agent MUST verify conditions 1–3 mechanically before requesting approval for condition 4:

1. The active scope's spec exists — `<project-folder>/spec/spec.md` for the baseline buildout, or `<project-folder>/spec/spec-<iteration-id>.md` for an Iteration.
2. The file passes the applicable checks in the [spec template's `SPEC-EXIT` validation checklist](templates/spec-template.md#spec-exit-validation-checklist), including the iteration applicability rule.
3. Configuration resolution or validated reuse has completed: `<project-folder>/twtty-runtime-config/` contains the complete copied config tree, composed local `default-config.md`, fully resolved `runtimeconfig.md` with the same binding structure and approved override values, and a project `README.md`. Required config references resolve locally, effective selections meet the active controls, and a `meta/config` replay-log entry (per [§8.1.1](#811-additional-meta-entries)) records resolution or reuse for this iteration.
4. The Human User's `Approval outcome` is `Approved` or `Approved with changes` (per [core §2](../../core-twtty-methodology.md#replay-execution-log-format)).

**Replay-log entry shapes:**

| Stage task | `<stage>/<stage-task>` | `<approval-gate-name>` | `Artifact / path changed` |
|------------|------------------------|------------------------|---------------------------|
| 1a (termination, only entry) | `spec/1a` | `—` | `<project-folder>/replay-execution/<iteration-id>-discovery-transcript.md` |
| 1b (final) | `spec/1b` | `SPEC-EXIT` | `<project-folder>/spec/spec-<iteration-id>.md` |

### 3.3 Plan

| Stage task | Agent | Output |
|------------|-------|--------|
| 2a. Architecture | Architecture Agent | The `## Metadata` block (Iteration ID = the active iteration's ID, matching the spec) and Section 1 (Architecture) of `plan-<iteration-id>.md` — or, for a multi-domain iteration, the plan overview plus each `plan/domains/<domain>-<iteration-id>.md` per [§8.2](#82-domain-based-separation-of-responsibilities) — drafted from the [plan template](templates/plan-template.md). |
| 2b. Design | Design Agent | Section 2 (Design) of `<project-folder>/plan/plan-<iteration-id>.md`. |
| 2c. Orchestration | Planning Agent | Section 3 (Orchestration) of `<project-folder>/plan/plan-<iteration-id>.md`. |

The baseline buildout writes `<project-folder>/plan/plan.md`; each later Iteration writes `<project-folder>/plan/plan-<iteration-id>.md` (see [core §4.3](../../core-twtty-methodology.md#43-on-new-iteration)).

**Plan metadata.** The plan opens with a `## Metadata` block whose `Iteration ID` MUST equal the corresponding spec's Iteration ID (it is the only iteration parameter the plan restates — the rest live in the spec's `## Metadata`). The `Plan confirmed date` is set to the `PLAN-EXIT` approval date at 2c. `PLAN-EXIT` check 20 enforces this block.

**Iteration plan applicability.** Baselines use the complete required plan template. Later Iterations include only intent-relevant architecture/design changes and the current work breakdown, dependency table, Team collaboration guidance, and execution controls. Reference unchanged approved plans, diagrams, and requirements after verifying their continued applicability; do not copy them or add N/A filler. All applicable controls still apply to current plus inherited content. Current work items MUST retain valid traces, domains, file footprints, and dependency checks; execution-mode offers, execution-pattern selection, stage-task approvals, and `PLAN-EXIT` remain required. Changed behavior requires current verification, not reuse of an old passing result merely because the threshold is unchanged.

**Execution mode offer (start of PLAN).** Before beginning 2a Architecture, the Architecture Agent MUST make the core-mandated Execution Mode offer ([core §1](../../core-twtty-methodology.md#execution-modes)): present Interactive and scoped Autopilot neutrally and record the choice/required authorization evidence under §5.1. This is separate from the Sequential/Parallel answer already recorded during Discovery, which is reused rather than asked again. The Human User may request or revoke Autopilot at other allowed points under core §1.

**Intra-stage stage tasks 2a, 2b.** Each is approved through its own TWTTY loop cycle (core [§1](../../core-twtty-methodology.md#the-twtty-loop)) and produces its own replay-execution log entry with `<approval-gate-name>` = `—`. Only 2c's approval triggers `PLAN-EXIT`.

**Domains (structure).** Architecture (2a) structures the spec's domains per [§8.2](#82-domain-based-separation-of-responsibilities). **A single-domain iteration is a single `plan-<iteration-id>.md`.** The full multi-domain shape is a hub-and-spoke plan: an overview with cross-cutting architecture, domain/layer map, interfaces/diagram, global work-item index, dependency table, Team collaboration guidance, and pattern selection, plus domain plans holding components, design, current work, and file footprints. Later Iterations create only affected domain plans and shared changes, referencing valid unchanged approved maps/plans. Orchestration (2c) still maps every current `W-<n>` to exactly one domain and keeps its expected footprint within that domain's footprint. Effective domain/layer footprints MUST remain mutually disjoint; inheritance does not relax the isolation check. See the [plan template](templates/plan-template.md).

**Work decomposition and Team collaboration.** During 2c, the Planning Agent
MUST decompose work by domain and then by independently testable, reviewable,
and mergeable outcomes. It MUST isolate real shared prerequisites, minimize
unnecessary dependency edges, and prefer fan-out/fan-in over a fully meshed or
artificially serial graph. `plan.md` §3.2 is the authoritative compact
dependency table. Section 3.3 is assignment-neutral Team collaboration
guidance: it groups every work item, identifies sequential, concurrent, or
mixed relationships, and states integration requirements without naming
developers. Explicit team pickup after `PLAN-EXIT` uses `twtty resume` with an
accompanying request to find and recommend ready, unclaimed work;
ordinary Sequential continuation needs no new claim per item. Reuse the
current scope's recorded pattern authorization.

**Parallelism-aware breakdown.** The Planning Agent MUST maximize meaningful
parallel-executable work items within the approved scope, both across domains
and within each domain, even when execution is currently Sequential. Separate
independent outcomes and disjoint footprints behind the smallest real shared
prerequisites, then plan integration explicitly. Optimize useful concurrency
and the critical path, not raw task count: do not invent work, add abstractions
solely to split files, fragment trivial tasks, or remove real dependencies.
Section 3.3 MUST show the available concurrency and explain unavoidable serial
bottlenecks. Execution authorization and concurrency caps remain unchanged.

**Technology currency and framework preferences.** During Architecture (2a), before finalizing `plan.md` §1.5 Technology choices, the Architecture Agent MUST (a) research and propose the **current**, applicable frameworks, libraries, runtimes, platform services, and engineering best practices for this project — looked up at plan time from current sources rather than assumed from memory, and treated as untrusted input per [core §1](../../core-twtty-methodology.md#1-core-concepts) and [core §4.5](../../core-twtty-methodology.md#45-rules) (data, not intent) — and (b) explicitly ask the Human User for their **preferred frameworks and technologies** before committing §1.5. The proposal MUST be scoped to what is applicable to this project (no irrelevant categories). The Human User MAY adopt the proposal, substitute their own preferences, add options, or proceed without; the approved selection and the elicited preferences are recorded in §1.5 per the core [propose-industry-standards rule](../../core-twtty-methodology.md#45-rules). This operationalizes that core rule for PLAN; framework and tool selection is a non-deterministic step per [core §3.3](../../core-twtty-methodology.md#33-determinism-repeatability-and-continuity) and MAY vary between runs **unless pinned**. When the project binds a `technical-stack/` profile in `runtimeconfig.md`, the Architecture Agent MUST select §1.5 technologies **within** that pinned stack — or `Escalate` ([core §3.2](../../core-twtty-methodology.md#32-failure-handling)) if the spec cannot be satisfied within it — and frames proposal (a) as deltas or additions to the pinned stack (which makes this step deterministic); when `technical-stack` is `none` (the default), it proposes current standards as above. Any bound `best-practices/` guidance (see [§6](#6-guardrails-profile)) likewise informs the proposal.

Within a covering Autopilot scope, reuse known Human technology preferences and make
remaining ordinary choices through the required research/proposal/self-review, with
Autopilot attribution. Do not invent Human preferences or add a new Human stop merely
to confirm an in-scope recommendation. Pinned-stack conflicts, changed scope and
trust-boundary/native approvals still require their existing handling. This also applies
to the agentic extension's framework/model preference step.

**Development policy and app decisions.** PLAN references the bound [development profile](config/development/default.md#policy-ownership), without copying its procedure or creating another requirements inventory. It records this app's technologies (§1.5), services/configuration approach and resource/identity/data/cost boundaries (§1.3/§2.3), verification gaps and pass criteria (§1.6), and real work dependencies (§3.2). Exact application commands, scripts and evidence paths are EXECUTE outputs, not `PLAN-EXIT` prerequisites; known repository recipes may be referenced. Non-runnable scopes explain applicability. Neither profile selection nor planning resets gates, changes hosting selection or grants operational permission.

**Execution-pattern confirmation, not re-interview.** After 2c supplies the work-item DAG and footprints, reuse the Human's recorded Sequential/Parallel answer from Discovery or earlier in this scope. Do not ask the same question again at PLAN or Resume. For Sequential, keep one writer and do not create worker branches merely because concurrency is possible. For Parallel, verify eligible work, isolated branches/targets, cap and material cost/time boundaries; present the concrete dispatch scope within the normal PLAN approval. The approved plan plus prior explicit Parallel choice authorizes only those in-scope dispatches and routine worker integration. If no applicable answer exists, collect it once. Record `meta/execution-pattern` with its Human-answer source and applicable plan before EXECUTE. Recheck affected eligibility when the plan changes; seek new authorization only for a material change outside the recorded scope/constraints, not for wording-only edits or an unchanged choice.

**Environment consistency.** Review [PLAN check 22](templates/plan-template.md#plan-exit-validation-checklist) across ownership, configuration, affected designs/work footprints and recipe/apply paths. Preserve unchanged approved plans/layouts and documented reuse-or-create choices; resolve actual conflicts, not deferred instance selection, before approval. The work dependencies must satisfy the bound development policy.

**Stage exit gate (`PLAN-EXIT`).** All four conditions MUST hold; the AI Agent MUST verify conditions 1–3 mechanically before requesting approval for condition 4:

1. The active scope's plan exists — `<project-folder>/plan/plan.md` for the baseline buildout, or `<project-folder>/plan/plan-<iteration-id>.md` for an Iteration.
2. The file passes the applicable checks in the [plan template's `PLAN-EXIT` validation checklist](templates/plan-template.md#plan-exit-validation-checklist), including the iteration applicability rule.
3. The active scope has a `meta/execution-pattern` record referencing the existing Human answer and applicable plan; affected Parallel eligibility/targets/caps are verified. No duplicate pattern question is needed for an unchanged grant.
4. The Human User's `Approval outcome` is `Approved` or `Approved with changes` (per [core §2](../../core-twtty-methodology.md#replay-execution-log-format)).

**Replay-log entry shapes:**

| Stage task | `<stage>/<stage-task>` | `<approval-gate-name>` | `Artifact / path changed` |
|------------|------------------------|------------------------|---------------------------|
| 2a | `plan/2a` | `—` | `<project-folder>/plan/plan-<iteration-id>.md` |
| 2b | `plan/2b` | `—` | `<project-folder>/plan/plan-<iteration-id>.md` |
| 2c (final) | `plan/2c` | `PLAN-EXIT` | `<project-folder>/plan/plan-<iteration-id>.md` |

### 3.4 Execute

**Development execution policy.** Follow the bound profile's
[developer workstation inner loop](config/development/default.md#developer-workstation-inner-loop),
including [requirements](config/development/default.md#requirements-and-dependencies),
[tooling readiness and reuse](config/development/default.md#tooling-readiness-and-reuse),
[app connection settings](config/development/default.md#application-connection-settings)
and [parallel preparation](config/development/default.md#parallel-setup).
It is the authoritative setup procedure for SDLC and its agentic/data extensions;
the table below defines task responsibilities, not a second procedure.
Stage-task IDs do not require numeric execution order. Existing approvals,
§5.1 isolation and the hosting/CD contracts below remain binding.

| Stage task | Agent | Protocol | Output |
|------------|-------|----------|--------|
| 3a. Setup | Setup Agent | TWTTY loop (core [§1](../../core-twtty-methodology.md#the-twtty-loop)) | Repository/context and native dependency setup under the bound development profile; due README/license and app CI/review configuration. Setup does not implement features or an eval harness. |
| 3b. Implement | Implementation Agent | TWTTY loop | Working software increment for one `W-<n>` in the current authorized context under §5.1, without creating a branch per item. Executed **once per `W-<n>`**. |
| 3c. Code review | Code Review Agent | TWTTY loop | Structured review on the current work candidate using the checklist in [§7.1.2](#712-testing-and-code-review-controls) (SOLID, complexity, obvious defects, test coverage of the change, doc updates). At L4+, the Code Review Agent Role MUST run in an isolated context from the implementer Agent Role (see [§5.1](#51-execution-mode-and-execution-pattern)). Executed **once per `W-<n>`**. |
| 3d. Code scanning | Code Scanning Agent | TWTTY loop | Automated static analysis of the current work candidate. Required tool categories (secret, SAST, dependency vulnerability, license, container image) and severity gating are level-tiered in [§7.1.1](#711-security-controls). Findings persisted under `reports/scans/W-<n>/` or platform-native (referenced from the replay-log entry). Executed **once per `W-<n>`**. |
| 3e. Security | Security Agent | TWTTY loop | Threat-model check and security scans on the current work candidate. Threat-model rigor (STRIDE at L4+; documented equivalent at L3) and named-standard verification (OWASP ASVS, OWASP Top 10, or documented equivalent at L2+) per [§7.1.1](#711-security-controls). At L4+, the Security Agent Role MUST apply this standard adversarially — actively testing whether the implementation can be broken against each checklist item — rather than confirming the implementer's own assumptions; isolated context per [§5.1](#51-execution-mode-and-execution-pattern) is necessary but not sufficient for this independence. Executed **once per `W-<n>`**. |
| 3f. Test | Test Agent | TWTTY loop | Apply §7.1.2's selected verification: basic happy-path smoke at L1, AC-referenced tests and applicable coverage when required by level, policy or explicit selection. Every current/affected inherited AC still needs truthful evidence; L1 does not require a generated test per AC. Infrastructure-only outcomes use mapped native results, not custom infra tests. Complete due verification before integration/publication. Executed **once per applicable `W-<n>`**. |
| 3g. CI/CD pipelines | Deployment Agent | TWTTY loop | Configure/reuse one project CI pipeline and required merge checks with owner authorization before normal merge; CI is default at every level, CD optional. Cloud targets MUST use separate infrastructure and application CD definitions per the separation contract below. Additional CI jobs are level-tiered in [§7.1.3](#713-cicd-controls). Validate/reuse **once per iteration**; extend only for approved changes, not per developer. |
| 3h. Infrastructure as code | Deployment Agent | TWTTY loop | Required service definitions, approved native create/start/reuse outcomes and app bindings under the bound development profile and provider. Hosting infrastructure follows its separate CD contract below. |
| 3i. Deployment | Deployment Agent | TWTTY loop | When cloud hosting is selected, the running target is deployed post-merge through CI/CD per [§9](#9-execution-rules), with applicable deployment strategy/rollback at L3+ per [§7.1.4](#714-deployment-and-operations-controls). Approved local-development IaC and initial identity bootstrap retain their scoped developer-CLI exceptions; they are not hosting releases. No unapproved developer/portal hosting deploys. Executed **once per applicable `W-<n>` deployment**, not merely for local execution. |
| 3j. Smoke tests | Deployment Agent | TWTTY loop | Automated post-deploy checks against the deployed environment: reachability, health endpoints, and at L3+ one happy-path per top-level user-facing use case. At L3+, smoke-test failure triggers automatic rollback per [§7.1.4](#714-deployment-and-operations-controls). Executed **once per `W-<n>` deployment**. |
| 3k. Monitoring | Monitoring Agent | TWTTY loop | Alerts and dashboards. At L3+, every configured alert MUST trace to an SLO declared in `plan.md §1.7 Operations architecture` (per [§7.1.4](#714-deployment-and-operations-controls)); the trace MUST be recorded in the `execute/3k` replay-log entry. Executed **once per iteration**. |
| 3l. Observability | Observability Agent | TWTTY loop | Logs, metrics, and traces wiring. Executed **once per iteration**. |
| 3m. Iteration | Human + Agents | TWTTY loop | Feedback capture and iteration closeout. Executed **once per iteration**; this stage task's approval triggers `EXECUTE-EXIT`. Before requesting `EXECUTE-EXIT` approval, the AI Agent MUST complete the applicable [project README template](../../../templates/project-readme-template.md) content with verified implementation, quickstart/authentication, architecture, usage and testing information. Keep "How this project was built" brief, with truthful approval/evidence and continuation links resolved against the actual artifact root; do not add obsolete methodology-heavy sections. Reuse unchanged valid README content. The AI Agent MUST ensure the iteration-execution diagram at `<project-folder>/replay-execution/<iteration-id>-execution-diagram.md` — maintained incrementally at every stage-exit gate — is current for closeout per [core §2 Iteration-execution diagram](../../core-twtty-methodology.md#iteration-execution-diagram-required-derived-artifact). |

Acronyms used in the table: **IaC** (Infrastructure as Code), **SAST** (Static Application Security Testing), **CI/CD** (Continuous Integration / Continuous Delivery), **PR** (Pull Request), **W-<n>** (a work item declared in `plan.md` §3.1).

**Work-item lifecycle.** Apply the development policy to preparation and local work; retain applicable reviews/tests/CI and closeout. Complete due local functional checks before domain/scope publication and required target PR/CI/reviews. Hosting deployment/post-deploy checks follow integration. Execution isolation and integration follow §5.1.

For an infrastructure-only development item, record its author/apply/native outcome
together under `execute/3h/W-<n>` with applicable resource ACs. Do not manufacture
`3b`-`3f` prompts, wrappers or tests to repeat that same result. Applicable authorization,
secrets/identity/ownership constraints and explicitly stricter target policy remain;
service-behavior ACs are verified in the normal app run, not declared passed by provisioning.

**Local feedback.** The profile governs local execution and shared recipes within the approved `W-<n>`/tool set. Each edit does not restart SEED/SPEC/PLAN; prompt/result records and applicable reviews/tests remain mandatory.

**Cloud-independent promotion prerequisite (hosting only).** Before provisioning the target hosting stack or deploying an application release, CI MUST verify applicable build/tests/static and native offline IaC checks for the candidate inputs, even at L1 with hosting. This hosting-only prerequisite does not gate development-dependency preparation under the profile. Hosting checks use no target credentials/services; failed/missing required checks block infra/app CD. Reuse valid input-matching evidence; rerun affected checks when effective inputs change.

- **Real-cloud evidence:** fixtures/emulators do not prove cloud identity, networking, managed-service behavior, or live acceptance. The plan MUST name those gaps and where they are checked. Cloud-dependent checks MUST pass at the stage required by the active risk controls and approved plan; they MUST NOT be silently waived, represented as locally verified, or deferred past a required pre-merge gate.
- **Scoped changes:** native deployment/validation and service results cover infrastructure-only acceptance without generated infra test suites. Hosting changes retain their required CI/promotion checks; unchanged app evidence is reused only while valid. Non-runnable scopes use applicable planned checks rather than inventing app/infra work. Missing required evidence is not a pass.
- **Incomplete candidates:** only explicit plan approval permits independent/offline
  work while required access is pending. Publish an incomplete candidate only when its
  due checks and repository policy permit, marking blocked acceptance explicitly.
  A configured adapter, demo response or green offline CI is not live-model acceptance
  and cannot satisfy an applicable required gate or `EXECUTE-EXIT`.

**Separate infrastructure and application CD (cloud targets).** When the confirmed Runtime target is a cloud, `3g` MUST establish independently triggerable infrastructure and application CD pipelines, using separate workflow/pipeline definitions on the bound `devtools` platform, not merely conditional steps in one combined deployment job. Both definitions MUST enforce the cloud-independent promotion prerequisite above for their applicable inputs. Shared reusable build, validation, and deployment components MAY be used.

- **Infrastructure CD** owns IaC validation and provisioning of hosting foundations, networking, storage, identities, access bindings, and edge/TLS infrastructure. It runs for changes to desired infrastructure state or its effective inputs, relevant drift reconciliation, or an approved explicit trigger, not automatically for every app commit.
- **Application CD** consumes the verified immutable release artifact produced by trusted CI after protected merge, promotes the same digest to selected compatible environments and runs required acceptance. Local candidate images are not release artifacts; infra-only changes reuse still-valid app artifacts rather than force a rebuild. App CD MUST NOT provision missing infrastructure or routinely invoke infra CD. Ownership is explicit; infra applies preserve app-owned version/config unless coordinated change is approved. Initial hosting bootstrap artifacts are declared in the plan.
- **The handoff contract** MUST identify the target environment, resource discovery or non-secret outputs, and the required infrastructure revision or compatibility check. App CD MUST fail clearly when prerequisites are missing or incompatible; it MUST NOT silently provision them or proceed against an unverified target.
- **Coordination** MUST let app-only changes deploy without reapplying unchanged infrastructure. When both change, application deployment MUST wait for successful infrastructure CD for the required approved revision and compatible handoff. Both pipelines MUST use a shared environment-level deployment lock or equivalent mutual exclusion for mutations; waiting for the other pipeline MUST NOT hold that lock. An orchestrator MAY coordinate the two without combining their deployment responsibilities.
- **Controls remain enforced:** each pipeline MUST retain applicable approval, identity, validation, traceability, and acceptance requirements. `plan.md §1.3` MUST declare the definitions, triggers, ownership boundary, handoff, dependency ordering, and locking strategy; the existing infrastructure diagram MAY show both paths without introducing another required diagram.

**Subsequent iterations are incremental — inherit prior iterations' outputs by default, and change only what the new iteration requires.** (This implements the core invariant [§3.4 Incremental iteration](../../core-twtty-methodology.md#34-incremental-iteration).) The iteration-scoped `spec-<iteration-id>.md` and `plan-<iteration-id>.md` SHOULD be structured as **deltas**, recording only what is added, modified, or removed relative to prior iterations; unchanged content is NOT restated. An Iteration whose intent is a substantial rewrite MAY produce full-shape `spec-<iteration-id>.md` and `plan-<iteration-id>.md` documents at the AI Agent's judgment, provided the rationale is recorded in the iteration's replay log.

For iteration specs, the full template is a guide, not a mandatory document shape. Keep required metadata and discovery/approval records, but include only sections and fields needed for the approved Iteration Intent. Omission does not retire an existing requirement. New or changed requirements MUST remain clear, testable, and covered by acceptance criteria; verify any inherited requirements or references against their approved artifacts when needed. `SPEC-EXIT` applies the content checks to that scope, including relevant specialization obligations, rather than requiring every template element to be populated. This does not waive active risk, security, data, or policy controls.

Iteration-level stage tasks that produce artifacts already present from prior iterations — `3a` Setup, iteration-level `3g` CI/CD, iteration-level `3h` Infrastructure as code, `3k` Monitoring, `3l` Observability — SHOULD NOT be re-executed when their prior-iteration artifacts remain unchanged. If the new iteration requires modifying or removing any artifact produced in a prior iteration — repository configuration (`package.json`, `pyproject.toml`, `.gitignore`, toolchain configs), CI/CD workflows, infrastructure templates, monitoring rules, observability wiring, source code, tests, or documentation — the modification or removal MUST be declared as a work item in the current iteration's `plan-<iteration-id>.md` (or as an explicit constraint in `spec-<iteration-id>.md`) so that the change is traceable and gate-approved like any other work.

**Reuse before recreation.** For subsequent iterations, the AI Agent MUST identify relevant existing artifacts before proposing replacements. Unchanged setup, identity, CI/CD, monitoring, and observability artifacts SHOULD be inherited by reference rather than recreated. Prior evidence MAY be reused only when its revision, inputs, environment assumptions, and applicability remain valid; changed behavior MUST receive appropriate verification. Inheritance MUST NOT substitute for required current gate checks or actual-artifact inspection. Spec and plan deltas SHOULD contain only changed requirements, decisions, dependencies, and acceptance criteria, while retaining the metadata, references, and gate-required content needed to evaluate the current iteration.

Per-work-item stage tasks (`3b`, `3c`, `3d`, `3e`, `3f`, per-work-item `3g`/`3h`, `3i`, `3j`) execute only for the work items declared in the current iteration's `plan-<iteration-id>.md`. `3m` Iteration is always executed to close each iteration.

**Work-tracking source of truth.** `plan.md` remains authoritative for `W-<n>` scope/dependencies. Commits and applicable PR descriptions identify the domain-qualified items they deliver; multiple sequential items share the same working branch or direct context under §5.1. No branch or PR per item is required. Optional tracker mirrors do not replace the plan. Hotfix Scopes retain the incident/Hotfix-ID procedure in §3.5.

**Risk-level tailoring.** Which per-work-item sub-stages apply is determined by the confirmed risk level per the [§7 top table](#7-risk-enforcement-profile). The concrete controls **within** each stage task — required scan categories and severity gates, coverage floors, CI jobs, deployment strategy, smoke rules, SLO tracing, setup essentials, data controls — are level-tiered in [§7.1 Risk calibration matrix](#71-risk-calibration-matrix). §3.4 does not duplicate the pruning or matrix rules; the AI Agent MUST consult §7.1 before executing any 3a–3m stage task and before requesting `EXECUTE-EXIT`.

**Replay-log entry ID convention.** Iteration-level entries use `<stage>/<stage-task>` = `execute/3a`, `execute/3k`, `execute/3l`, `execute/3m`. Per-work-item entries use `<stage>/<stage-task>` = `execute/<stage-task>/<W-id>` — for example, `execute/3b/W-5`, `execute/3f/W-5`. This convention keeps entries deterministic across many work items; entries order by their numeric `<sequence-id>` per [core §2](../../core-twtty-methodology.md#replay-execution-log-format), independent of the label.

**Intra-stage cycle clarification.** Every 3a–3l entry (iteration-level or per-work-item) uses `<approval-gate-name>` = `—`. Only the final 3m Iteration entry triggers `EXECUTE-EXIT`.

**Stage exit gate (`EXECUTE-EXIT`).** All six conditions MUST hold; the AI Agent MUST verify conditions 1–5 mechanically before requesting approval for condition 6:

1. Every planned `W-<n>` has an approved implementation entry (`execute/3b/W-<n>`, or `execute/3h/W-<n>` for infrastructure-only development work), or an `Abandon`/`Escalate` with its resolution recorded.
2. Every current and affected inherited AC has current passing evidence: app behavior in `execute/3f/W-<m>` under the level's verification contract (L1 smoke plus actual artifact inspection, not a mandatory test per AC), infrastructure-only resource outcomes in `execute/3h/W-<m>` mapped to native results. A service-behavior AC still needs actual app/service evidence; deployment success alone does not satisfy it.
3. Every applicable sub-stage has completion evidence. Infrastructure-only development items use the consolidated `3h` record above, not duplicate app-stage entries.
4. Iteration-level sub-stages required by §7 have completed replay-log entries: `execute/3a` (all levels), and at applicable levels `execute/3k` and `execute/3l`.
5. Every row marked `MUST` for the confirmed risk level — in [§7.1 Risk calibration matrix](#71-risk-calibration-matrix) **and in the active specialized implementation's risk-enforcement delta (if any)** — is satisfied, mechanically verified where possible, otherwise attested in the corresponding stage-task replay-log entry's `Notes` field or in `execute/3m`.
6. The Human User's `Approval outcome` on `execute/3m` is `Approved` or `Approved with changes` (per [core §2](../../core-twtty-methodology.md#replay-execution-log-format)).

**Replay-log entry shapes:**

| Stage task | `<stage>/<stage-task>` | `<approval-gate-name>` | `Artifact / path changed` |
|------------|------------------------|------------------------|---------------------------|
| 3a (iteration-level) | `execute/3a` | `—` | Repository initialization paths (e.g., `.gitignore`, `README.md`, toolchain configs) |
| 3b (per-work-item) | `execute/3b/W-<n>` | `—` | Source files added or modified for `W-<n>` |
| 3c (per-work-item) | `execute/3c/W-<n>` | `—` | Review artifact under `reports/` or `—` if review lives on the PR |
| 3d (per-work-item) | `execute/3d/W-<n>` | `—` | Scan report path or `—` if handled by the bound `devtools` native scanning |
| 3e (per-work-item) | `execute/3e/W-<n>` | `—` | Security review artifact path or `—` if lives on the PR |
| 3f (per-work-item) | `execute/3f/W-<n>` | `—` | Test tree paths modified or added |
| 3g (iteration-level or per-work-item) | `execute/3g` or `execute/3g/W-<n>` | `—` | The bound `devtools` CI path (e.g. `.github/workflows/*`) |
| 3h (iteration-level or per-work-item) | `execute/3h` or `execute/3h/W-<n>` | `—` | Actual changed paths beneath the approved environment IaC root, including its inputs/modules |
| 3i (per-work-item) | `execute/3i/W-<n>` | `—` | `—` (deployment is a runtime event; `Execution outcome` records the deployed environment and version) |
| 3j (per-work-item) | `execute/3j/W-<n>` | `—` | `tests/smoke/*` if new smoke tests were added, else `—` |
| 3k (iteration-level) | `execute/3k` | `—` | Environment-owned monitoring IaC under the approved `infra/environments/<environment>/` root or platform-native dashboard paths |
| 3l (iteration-level) | `execute/3l` | `—` | Environment-owned telemetry IaC under its approved environment root; shared instrumentation in the source tree, or platform-native config |
| 3m (iteration-level, final) | `execute/3m` | `EXECUTE-EXIT` | `—` (iteration is a closeout event; `Execution outcome` records the iteration completion summary) |

### 3.5 Hotfix path (production incident fast path)

A **Hotfix Scope** (`H-<token>`, for example `H-7Q2K9F`) is a narrow,
urgent fix to a confirmed production incident. It is NOT an Iteration: it is
the sole bounded stage-order exception defined by
[core Lifecycle stages](../../core-twtty-methodology.md#lifecycle-stages).
The AI Agent generates `<token>` with the same collision-resistant random-token
rule used for Iteration IDs in [core §4.3](../../core-twtty-methodology.md#43-on-new-iteration);
it MUST regenerate if the incident path, log path, or branch already exists.
The active Iteration is **paused**, the Hotfix Scope runs and closes on its own
fast path, and the paused Iteration then resumes exactly where it left off.

**When to use.** A Hotfix Scope applies only to a confirmed incident in a production environment (per [§9](#9-execution-rules)) requiring a fix faster than the active iteration's remaining EXECUTE work can deliver it. It MUST NOT be used to bypass SPEC/PLAN discipline for ordinary feature work — that always goes through a full Iteration.

**Entry through Start iteration.** An explicit urgent production-incident request
accompanying `twtty start iteration` routes here after recovering the existing
scope/risk and confirming incident applicability, before creating an ordinary
Iteration ID or Intent. Unsupported or ambiguous incident requests stop for
clarification; ordinary changes retain the full lifecycle. Existing Hotfix Scopes
are recovered with `twtty resume`; their IDs, logs and pause pairs remain unchanged.

**Invocation is a hard guardrail.** Opening a Hotfix Scope MUST receive
explicit Human User approval, even under Autopilot. After approval, the AI Agent
MUST create the hotfix branch, incident record, initial
`hotfix/incident` log entry, and matching `meta/iteration-pause` entry in one
commit and push it. It MUST then open a draft hotfix PR with the Hotfix ID,
paused Iteration ID, and paths and commit references for the incident, log,
and approved pause entry in its body. The artifact commit is atomic; opening
is complete only after the PR and its approval evidence are remotely
discoverable. A failure to publish either MUST Escalate; hotfix implementation
MUST NOT begin with a partial opening.

**Shared pause discovery.** On resume, work pickup, and before merging or
deploying work, the AI Agent MUST refresh relevant hotfix PR metadata through
scoped, batched queries and verify its referenced pause/exit evidence,
including closed PRs without a matching resume. Use the derived pause index
and watermarks to inspect newly changed records and outstanding pairs, not
rescan all PR history at each boundary. Without a trustworthy index, establish
it from the relevant scope's evidence; missing coverage MUST NOT be treated as
no pause. PR metadata indexes the evidence; it is not itself approval.
An approved pause takes effect for its exact `(Iteration ID, Hotfix ID)` pair
even before its branch is merged. That Iteration stops at the next safe
boundary and MUST NOT acquire work, merge, or deploy while paused; unrelated
Iterations remain eligible. Only the matching approved resume clears it;
closing the PR alone does not. Missing or conflicting evidence MUST be
surfaced as drift, not ignored.

**Inherited risk level.** A Hotfix Scope does not confirm its own risk level; it inherits the most recently confirmed `meta/risk-level` entry from the active project.

**Minimal artifacts — no full SEED→SPEC→PLAN.** A Hotfix Scope produces one
incident record at `<project-folder>/hotfix/<hotfix-id>-incident.md` containing:
the triggering symptom, affected production environment, root-cause
hypothesis, minimal fix scope, and rollback plan. This core-authorized incident
record replaces `spec.md` and `plan.md` for the Hotfix Scope; there is no
discovery interview.

**EXECUTE controls still apply, unreduced.** A Hotfix Scope MUST execute every
applicable inherited task and control for 3b Implement, 3c Code review, 3d Code
scanning, 3e Security, 3f Test, 3i Deployment, and 3j Smoke tests under
[§7](#7-risk-enforcement-profile) and [§7.1](#71-risk-calibration-matrix).
Task 3e is also required whenever the fix touches a security-relevant surface,
even if the inherited level would not otherwise require it.

**Hotfix branch and PR lifecycle.** The incident record is the scope source of
truth in place of `plan.md` and `W-<n>` items. The branch is
`<hotfix-id>-<slug>`; its PR title and every commit subject MUST start with the
Hotfix ID. Its branch log is
`<project-folder>/replay-execution/branches/<hotfix-id>-<branch-token>-execution-log.md`,
using the private branch-reference procedure in §8.1.2, not the native branch name.
The standard `meta/branch-open`, `meta/branch-close`, and
`meta/branch-integrated` evidence applies with the Hotfix ID replacing
Iteration and `W-<n>` references. All other review, validation, CI, merge, and
post-integration rules in [§8.1.2](#812-branch-scoped-replay-logs) and
[§9](#9-execution-rules) remain unchanged.

**Replay log.** The Hotfix Scope uses its own log at
`<project-folder>/replay-execution/<hotfix-id>-execution-log.md`, using the same
entry format as an Iteration log
([core §2](../../core-twtty-methodology.md#replay-execution-log-format)), with
`<stage>/<stage-task>` values `hotfix/incident`, `hotfix/3b`, `hotfix/3c`,
`hotfix/3d`, `hotfix/3e`, `hotfix/3f`, `hotfix/3i`, and `hotfix/3j`, closing
with a `HOTFIX-EXIT` gate.

**`HOTFIX-EXIT` conditions.** All five MUST hold; the AI Agent MUST verify conditions 1–4 mechanically before requesting approval for condition 5:

1. The incident record at `hotfix/<hotfix-id>-incident.md` documents symptom, affected production environment, root-cause hypothesis, fix scope, and rollback plan.
2. Every applicable control in [§7.1](#71-risk-calibration-matrix) for the inherited risk level has a corresponding `hotfix/<stage-task>` replay-log entry with `Approval outcome` ∈ {`Approved`, `Approved with changes`}.
3. The fix is deployed to the affected production environment and `hotfix/3j` smoke tests pass. At L3+, a smoke-test failure triggers automatic rollback; no Hotfix Scope may exit until a corrected deployment passes.
4. The incident record is updated with the resolution summary and verified-fixed timestamp.
5. The Human User's `Approval outcome` on the closing entry is `Approved` or `Approved with changes`.

**Resuming the paused iteration.** On `HOTFIX-EXIT` approval, the AI Agent MUST append a `meta/iteration-resume` entry (see [§8.1.1](#811-additional-meta-entries)) for the same Iteration/Hotfix pair, publish it through the existing integration rules, and resume exactly where that Iteration left off. If a session stopped after the approved exit but before this entry, recovery verifies the exit and records the missing resume; it MUST NOT wait indefinitely for an entry it is required to create.

---

### 3.6 Existing-project preparation

Resume first recovers the selected scope's state under core §4.1, then applies the action-selection rules below before proposing lifecycle continuation. Local preparation is not an independent Setup command. Applies to SDLC and its agentic/data extensions. Preserve source layout, current branch/worktree, existing services, config overrides and valid evidence.

**Continuation responsibility.** For an unfinished baseline or Iteration, establish the Human who started it from the original approved SEED evidence and its native Human attribution. A later approved `meta/continuation-assignment` supersedes that responsibility without rewriting the original evidence. Compare this with the current Human using available native identity/approval evidence; opening a branch, Git's last author/committer, local Git configuration and matching redacted placeholders do not establish that relationship. If evidence is insufficient, ask one focused clarification and obtain the confirmation required by the project's policy; do not claim an identity was authenticated when it was only confirmed by the Human.

**Offer actions from the recovered state.**

- **Unfinished scope, same Human or approved successor:** propose the recovered next stage/task. Also offer local setup/run where applicable, without making it a prerequisite for unrelated SPEC/PLAN work.
- **Existing contributor assignment:** propose continuation only within the current Human's verified claim or authorized parent dispatch. This does not transfer responsibility for the whole Iteration.
- **Unfinished scope, different Human without that assignment:** report the scope's status, but do not offer its continuation by default. Offer applicable local setup/run, an explicitly approved handover, or a separate eligible Iteration.
- **Completed scope:** report completion and offer local setup/run, a new Iteration, or both. Offering the new-Iteration choice does not propose its intent, reopen the completed scope or create anything. Only a Human selection and confirmed intent route to core §4.3.
- **Paused, abandoned, escalated or conflicting scope:** surface its restriction and permitted recovery choices. Setup/run, reassignment and a new Iteration MUST NOT bypass the applicable pause, recovery, isolation or approval rules.

A new Iteration still requires the approved original Project Seed and verified initial baseline completion. An unfinished baseline cannot be bypassed by starting another Iteration. Other planned work is discovered only on an explicit work-pickup request; ordinary Resume does not scan/rank global assignments. An explicit action request is reused instead of asking the Human to select it again.

**Check readiness for the selected action.** Inspect only the tools, packages, configuration and access needed for that action in its actual execution context. A fresh checkout or unknown readiness alone MUST NOT interrupt recovered SPEC/PLAN work with an app-onboarding offer. Reuse verified unchanged readiness. When a prerequisite is missing or cannot be verified, offer the concrete setup or diagnostic action, obtain uncovered approvals, prepare only missing prerequisites through the bound development profile, and return to the selected action. A declined or unavailable prerequisite blocks only work that needs it; report the remaining gap explicitly.

1. Use the recovered product/artifact roots, directly relevant config/progress and selected action; ask once if unclear. Check only selected work's approval, pause, dependency and conflict evidence before lifecycle writes.
2. Reuse valid adopted project configuration; age alone does not require an update. If a required setting, file or preparation procedure is missing/incompatible, surface the gap and request an approved scoped update preserving overrides; never silently substitute shared defaults. Required materialization uses the project's adopted sources; unavailable/ambiguous sources escalate. A project never configured for TWTTY requires explicit first adoption of the chosen defaults.
3. For selected local setup/run, execute the bound development profile's separate [Resume preparation](config/development/default.md#resume-preparation) procedure. For other selected tasks, follow the bound development profile as needed. Resume chooses the first unmet prerequisite/plan obligation, not the next numeric stage-task ID; a completed `3h` does not skip app setup/implementation.
4. Record results/gaps/next actions in existing `meta/setup`/work-item evidence; no per-tool or worker-setup log. Preparation invents no historical approvals and grants no merge/release/recipient authority. Contributor assignments and Autopilot authorization do not transfer. Non-TWTTY checkouts may be operationally prepared, but implementation/refactoring requires their approved Project Seed/baseline; later Iterations require baseline completion and approved intent; preparation never substitutes for that lifecycle.

### 3.7 Project handoff

`twtty handoff` is an explicitly requested independent delivery, not local setup, deployment or a new iteration. Applies to SDLC and its agentic/data extensions. Produce a **private GitHub repository and matching ZIP** only after their source, history, destination and access boundaries are approved.

1. Resolve the actual product/artifact roots and requested snapshot. Inventory source HEAD, remotes, raw working-file hashes and status without modifying them. Approved selection is current tracked files (`git ls-files --cached -z`) plus non-ignored untracked files (`git ls-files --others --exclude-standard -z`), honoring working deletions and effective repository/global ignore rules. Tracked-but-ignored files remain selected. Review additions/exclusions and history depth; partial export is explicit, never silent.
2. Include selected project TWTTY config, artifacts, logs and history across the approved boundary, **not only the latest iteration**. Do not mistake project-owned `twtty/` for a framework clone. Exclude ignored untracked caches/dependencies/images by default. Required ignored inputs need safe approved inclusion or recipient-owned locked restoration; unresolved required gaps block delivery.
3. Freeze the approved input snapshot and work only in isolated export copies outside the source. Never copy source `.git` administration, mutate its worktree/HEAD/remotes, fetch credentials or use sender caches/data as required inputs. Carry approved safe history separately or reconstruct it in the export repository. Materialize approved LFS objects, submodule commits and symlink content; unresolved required objects, links outside the approved boundary or unsafe paths block, not silently trim.
4. Scan all selected files **and approved history** for secrets, sensitive identifiers/data, unsafe links, hooks and credential-bearing config. Sanitize export copies only with approved transformations. Describe rewritten history/log evidence truthfully; retain source provenance without claiming transformed logs are unchanged approval evidence. Historical sender approvals/claims do not authorize the recipient.
5. Generate [HANDOFF.md](templates/handoff-template.md) and link it from the payload README. Reference the **current separate authorized framework**, never bundle a framework library snapshot or silently update/reset the recipient's checkout. Supply verified tools/locked restores, shared recipes/Dockerfile, safe config names, identity/access/network/cost prerequisites, actual roots and gaps. Recipient builds its own images; an approved custom Dockerfile is revalidated.
6. Stage the export repository and matching ZIP locally from the same final sanitized snapshot/history. Verify content/history parity through canonical manifests/raw hashes, safe extraction, planned private destination/access and clean scans. Preserve documented selected link/permission semantics or declare/block required incompatibility. Keep receipt, checksums, evidence and `meta/handoff` **outside source and payload**; avoid self-referential archive checksums.
7. Recheck source HEAD/remotes/status/raw file hashes and invalidate delivery if the source snapshot changed. Only then, with specific destination/publication/access approval, publish the private GitHub repository and ZIP and verify final parity/private access. Record delivery separately from recipient readiness; unrun recipient/cloud checks remain pending. Recipient uses `twtty resume`, their own identity/services/config, never a new baseline or sender credentials/authority. Failed checks block publication.

## 4. Artifact locations

**TWTTY as a plug-in.** The `<project-folder>` MAY be a dedicated `twtty/`
directory inside the target repository, so that all process artifacts —
`seed/`, `spec/`, `plan/`, `replay-execution/`, and `twtty-runtime-config/` —
stay isolated under one folder and do not interfere with the target's existing
files (useful in brownfield and modernization scenarios). EXECUTE product and
code outputs (the table below) are written to their natural repository
locations **outside** `twtty/`. This is a layout convention only: it rewrites no
path tokens, since every `<project-folder>/...` path resolves beneath the chosen
folder.

SEED, SPEC, and PLAN artifacts are written to `<project-folder>/<stage>/` as defined in [core §2](../../core-twtty-methodology.md#2-artifacts-and-formats). Per core §2, the **baseline buildout** writes **unnumbered** artifacts (`seed/seed.md`, `spec/spec.md`, `plan/plan.md`, `replay-execution/execution-log.md`, and the baseline `discovery-transcript.md` / `execution-diagram.md`), while each **later Iteration** carries its generated iteration ID in the filename (`seed/intent-<iteration-id>.md`, `spec/spec-<iteration-id>.md`, `plan/plan-<iteration-id>.md`, `<iteration-id>-execution-log.md`, …). **Throughout this document, a reference to `spec-<iteration-id>.md` / `plan-<iteration-id>.md` / `<domain>-<iteration-id>.md` / `<iteration-id>-*` denotes the Iteration case; for the baseline buildout, substitute the unnumbered form (`spec.md`, `plan.md`, `<domain>.md`, `execution-log.md`, …).** Discovery materializes the complete project-owned configuration tree at `<project-folder>/twtty-runtime-config/`: adopted composed defaults, fully resolved `runtimeconfig.md`, all baseline/specialization profiles and the explanatory README (see [§3.2 Config interview](#config-interview)). Binding-file references resolve there; infrastructure and executable recipes resolve from the product root and do not belong in the config snapshot. EXECUTE artifacts are written to their natural locations in the repository:

UX wireframes and interactive prototypes are PLAN artifacts. The baseline uses
`<project-folder>/plan/wireframes/`; every later UI-affecting Iteration uses
`<project-folder>/plan/wireframes/<iteration-id>/` so incremental design work
never overwrites prior approved evidence.

| Stage task | Canonical location |
|------------|--------------------|
| 3a Setup | Repository initialization at repo root (e.g., `.gitignore`, `README.md`, toolchain configs, default branch) |
| 3b Implement | Project source tree (e.g., `src/`, language-conventional layout) |
| 3c Code review, 3d Code scanning, 3e Security | Tooling reports under `reports/` or the bound [`devtools`](config/devtools/) platform's native scanning |
| 3f Test | Test tree (e.g., `tests/`, `__tests__/`, language-conventional) |
| 3g CI/CD pipeline | The bound [`devtools`](config/devtools/) CI path (e.g., `.github/workflows/` for GitHub, Azure Pipelines YAML for Azure DevOps) |
| 3h Infrastructure as code | Approved environment root under `infra/environments/`: `local/` for newly owned local-development dependencies, `cloud/<stage>/` for selected shared cloud-stage infrastructure; authorized adopted layouts may be retained |
| 3i Deployment, 3j Smoke tests | Pipeline definitions plus smoke-test scripts under `tests/smoke/` or pipeline-native |
| 3k Monitoring, 3l Observability | Environment-owned monitoring/telemetry IaC within that environment's root; shared instrumentation stays in source/tooling, plus platform-native dashboards |
| Customization surfaces (per §5.2) | The bound [`harness`](config/harness/) customization paths, per current harness documentation |

The replay-execution log MUST be appended to throughout all stages using the entry format defined in [core §2 — Replay-execution log format](../../core-twtty-methodology.md#replay-execution-log-format). The AI Agent MUST also maintain the derived [project state summary](../../core-twtty-methodology.md#project-state-summary) at `<project-folder>/replay-execution/state.md`, updating it at every Approval Gate so resume stays bounded for long-lived projects.

---

## 5. Runtime profile

This SDLC implementation runs on the **bound harness** — the agentic coding tool that plays the agent roles across every stage. The harness is one of the [capability bindings defined in §1.1](#11-capability-bindings-config); it is set in `runtimeconfig.md` (`harness:`), resolved from `default-config.md` at SEED and confirmed during the Discovery config interview (see [Config interview](#config-interview)); the default reference harness is GitHub Copilot ([`harness/ghcopilot.md`](config/harness/ghcopilot.md)), which documents its runtime modes (e.g. VS Code Agent mode, Copilot CLI).

The harness binding defines the runtime modes, the model and model-escalation policy, and the customization surfaces the harness exposes (see [§5.2](#52-customization-surfaces-and-runtime-features)). Each agent in the pipeline is a role played by the chosen harness; context-isolation requirements per risk level come from [Section 7 — Risk enforcement profile](#7-risk-enforcement-profile) (and the active `risk-calibration` binding). If the bound harness cannot satisfy a control the risk level requires — for example an isolated reviewer context at L4+ — the AI Agent MUST `Escalate` per [core §3.2](../../core-twtty-methodology.md#32-failure-handling).

### 5.1 Execution mode and execution pattern

**Branching for isolation only.** Sequential is the normal execution pattern. A work item is a planning/traceability unit, not a reason to create a branch, worktree or PR. Use this topology throughout EXECUTE:

| Situation | Working context and integration |
|---|---|
| Single domain, sequential | Reuse the current authorized context on the configured integration branch when direct development is permitted; no extra branch. |
| Multiple domains | After initial infra preparation in the common working context, use one scope-limited working branch per affected domain for app work. Reuse it for sequential items, not one branch per work item; initial infra setup does not get its own branch. |
| Parallel workers | Each concurrent writer uses a separate branch and isolated worktree or clone. Base workers on their domain's working branch, or the single-domain working context; merge results back there serially. |
| Protected repository or stricter policy | Preserve required PR/CI/review controls. If direct development is prohibited, use one working branch/PR for the scope as the common base; child domain/worker branches integrate there. Publish through required target controls, not per-item PRs or a protection bypass. |

**Common working context.** Use the current authorized integration branch and checkout
where direct development is permitted, otherwise the approved scope branch required by
protection. Prepare initial local/Azure infrastructure and save app settings there first.
Commit applicable tracked infra changes there before deriving needed app-domain or worker
branches from that prepared revision. Do not create a branch or worktree solely because
initial setup writes IaC. Infrastructure ownership is unchanged; it does not dictate this
setup branch. Reuse the same checkout for Sequential development. A separate working folder
is needed for concurrent writers, not merely because Sequential work switches branches.

Domain branches last for the approved scope, not as permanent release branches. Name new branches by domain/worker and scope so concurrent Iterations do not collide; retain existing names on Resume. **Never run concurrent writers on the same branch or checkout**, even for disjoint files. Read-only review and non-mutating checks may share a candidate without becoming parallel writers.

**Worker integration is pre-authorized work.** The approved parallel-dispatch prompt includes the target working branch, Git integration tools and routine worker merges. The coordinator may merge those results and resolve straightforward conflicts without another Human approval or worker PR where target policy permits. Run affected checks on the combined result. Stop for changed scope/behavior, ambiguous conflict resolution, unapproved cost or other hard guardrails; native permission prompts remain. A merge to protected main or another protected target still requires its applicable PR/CI/reviews. No grant bypasses repository protection.

Two independent axes govern how those branches are worked. They are orthogonal — **any execution mode MAY combine with any execution pattern**.

#### Axis 1: Execution mode (governs Human-User participation)

Defined normatively in [core §1](../../core-twtty-methodology.md#execution-modes).

| Execution mode | Meaning |
|----------------|---------|
| **Interactive** *(default)* | The Human User explicitly approves every prompt at every Approval Gate. |
| **Autopilot** *(opt-in, post-`SEED-EXIT`)* | The Human User grants one up-front authorization for a defined scope — from SPEC onward — and within that scope the AI Agent self-approves subsequent gates and still writes a replay-execution log entry for every gate. Recorded via a `meta/autopilot-enable` replay-log entry. |

**Autopilot authorization evidence.** Use this fixed rule; do not improvise new
authorization ceremonies:

- **L1, absent a stricter selected policy:** one direct Human approval/request in the current native chat or confirmation
  is sufficient for the fixed scoped grant under core §1. Record its actual wording,
  timestamp and native message/approval reference, the repository/working context,
  baseline/Iteration, covered stages and unchanged constraints in `meta/autopilot-enable`.
  Verify the original native Human input, not an AI summary. No Human Git commit,
  signature setup, authorization file or pasted SHA is required. An agent-to-agent
  relay is not itself Human approval; a Human may explicitly authorize a named execution
  context through another chat only if that original native approval and its target
  can be checked. If origin/scope is unavailable or ambiguous, obtain one direct native
  Human confirmation; never fabricate the source or claim cryptographic nonrepudiation.
- **L2-L5 / stricter policy:** retain independently verifiable Human-authored
  version-control authorization. At L3+, require a verified-signature commit or
  platform-authenticated PR approval by that authorized Human and verify the native
  signature/approval metadata. An unsigned commit or agent-producible statement alone
  is not valid evidence. Existing stronger controls are not relaxed by the L1 route.

An AI-authored replay entry/commit alone never grants Autopilot. Append the existing
enable record before self-approval; preserve prior valid grants/history and do not
re-confirm unchanged applicable authorization on Resume. Risk escalation out of L1
requires the newly applicable evidence. Do not create an authorization validator.
Core hard guardrails and current-context applicability still apply.

**Resume authorization applicability.** Before reusing an Autopilot anchor, verify that it authorizes the current Human User, repository/working context, selected scope and constraints per core §4.1 step 7. Use the original native Human approval at L1 or the relevant native commit/approval metadata where required; do not infer identity from copied logs or scan unrelated assignments. A recipient/imported-history grant is not current authorization, even when setup is ready. Use Interactive unless the current context has its own verified applicable grant; retain applicable signature/approval requirements and historical evidence.

#### Axis 2: Execution pattern (governs how many branches and Agent contexts run at once)

Defined by this implementation. Software-delivery concept.

| Execution pattern | Meaning |
|-------------------|---------|
| **Sequential** *(default)* | One writer works through approved items in the same working context, completing applicable reviews/tests without a branch/PR cycle per item. In multi-domain work, use the affected domain's branch. Integrate completed scope through the repository's authorized process. |
| **Parallel** *(opt-in)* | Independent writers use distinct branches and isolated working directories. A domain branch may itself be one worker's exclusive context; additional workers within that domain use child branches. The coordinator merges worker results into their recorded working target serially, then delivers domain/scope results through required repository controls. No more than 5 subagents run concurrently. |

#### Orthogonality: the four combinations

| Execution mode × pattern | What the Human User sees | What runs |
|--------------------------|--------------------------|-----------|
| Interactive + Sequential | Human User approves every prompt. Single Agent works one `W-<n>` at a time. | 1 branch, 1 Agent context. |
| Interactive + Parallel | Human User approves dispatch including routine worker integration; no separate approval for each in-scope worker merge. Other gates/guardrails remain. | Up to 5 isolated worker branches; coordinator integrates serially into recorded working targets. |
| Autopilot + Sequential | Human User grants Autopilot up front. Single Agent works one `W-<n>` at a time and self-approves gates within scope. | 1 branch, 1 Agent context. |
| Autopilot + Parallel | Human User grants Autopilot up front AND selects Parallel via `meta/execution-pattern`. Subagents self-approve within scope; orchestrator merges serially. | Up to 5 concurrent subagent branches; same. |

#### How the AI Agent selects the execution pattern

1. **Sequential is normal; reuse the existing answer.** Use the current scope's Human selection from Discovery or an earlier explicit answer. Do not repeat the question at PLAN or Resume. If missing, collect it once; record `meta/execution-pattern` against the plan before EXECUTE.
2. **Parallel requires DAG independence.** Per `plan.md` §3.2, the AI Agent MUST NOT include any `W-<n>` in a Parallel `meta/execution-pattern` scope if that `W-<n>` depends on another `W-<n>` in the same scope, directly or through a chain of prerequisites. See [plan-template.md §3.2](templates/plan-template.md) for the DAG definition. Co-dispatched branches MUST additionally have disjoint expected file footprints (`plan.md` §3.1); see [§5.1.1](#511-parallel-pattern-discipline) step 1.
3. **Parallel requires covering Human authorization.** Reuse the explicit Parallel choice with the approved plan/dispatch scope; record eligible items, targets, concurrency cap and cost/time boundaries in `meta/execution-pattern`. A default value is not a grant. Ask again only for material expansion beyond that authorization; silent parallelism is prohibited.
4. **Dispatch only when isolation is useful.** Once Parallel is authorized, give each concurrent writer an exclusive branch/worktree and record its target working branch. Reuse an exclusive domain branch for a domain worker; use child branches for multiple workers within a domain. Undispatched work stays Sequential; do not spawn workers merely because the plan exposes possible concurrency.
5. **Concurrency is capped at 5 subagents.** The AI Agent MUST NOT have more than 5 subagents running concurrently at any point during a parallel burst. The `meta/execution-pattern` entry's `Notes` field MUST record the burst's concurrency cap, and that cap MUST be `≤ 5`. If more than 5 branches are dispatchable, the AI Agent MUST run them in successive bursts, not a single wider burst.
6. **Risk level does NOT restrict pattern choice.** Sequential and Parallel are both available at every risk level (L1–L5). Risk level restricts only which stage tasks apply and the independent-review requirement below.

#### Independent review (level-driven, orthogonal to both axes)

The Code Review Agent Role's context isolation from the implementer Agent Role is governed by [§7.1.2](#712-testing-and-code-review-controls):

- **L1–L3:** the implementer MAY play the reviewer role in the same Agent context (no isolation required).
- **L4–L5:** the reviewer Agent Role MUST run in an isolated context from the implementer. A fresh-context reviewer inspects the candidate read-only, after implementation; review isolation does not require another writable branch. Corrections return to the owning writer, and affected checks run again before integration.

Independent review is a **per-role property**, not a mode or pattern. It applies identically whether execution runs Sequential or Parallel.

See [§5.1.1](#511-parallel-pattern-discipline) for the mandatory discipline the AI Agent MUST follow when using the Parallel pattern.

### 5.1.1 Parallel pattern discipline

Parallel pattern is exceptional and uses an exclusive branch/worktree per concurrent writer. The coordinator MUST:

1. **Confirm DAG independence *and* file-footprint disjointness.** Verify against `plan.md` §3.2 that no `W-<n>` in the intended parallel scope depends on another `W-<n>` in the same scope, directly or through a chain of prerequisites. DAG independence does not imply file-level independence: two feature-independent work items may still both edit a shared file (a package manifest, a router, a shared IaC module). The AI Agent MUST NOT co-dispatch, in the same parallel burst, two branches whose declared expected file footprints (`plan.md` §3.1) overlap. Items with overlapping footprints MUST be split across successive bursts or handled Sequentially, so file-level conflicts are prevented at dispatch rather than discovered at merge. Work items in **different domains** are footprint-disjoint by construction ([§8.2](#82-domain-based-separation-of-responsibilities)) and are therefore always eligible to co-dispatch; the overlap check is decisive only **within** a domain.
2. **Obtain Human User authorization** via a `meta/execution-pattern` replay-log entry (per §5.1 rule 3).
3. **Decide dispatch per branch.** Per §5.1 rule 4, decide which branches in the enabled scope warrant a subagent and which the main Agent will handle Sequentially. Record the decision in each branch's `meta/branch-open` entry.
4. **Respect the concurrency cap.** No more than 5 subagents MAY run concurrently (§5.1 rule 5). If more branches are dispatchable, run them in successive bursts.
5. **Choose the receiving working branch.** Reuse the domain working branch or single-domain context under §5.1. Each concurrent worker has its own branch and directory, with a scope-qualified identity and branch log under §8.1.2. Never attach multiple writers to one branch; multiple domains alone do not authorize simultaneous execution.
6. **Dispatch subagents.** Disclose scope, footprint, base/target branch, applicable checks and routine integration in the approved prompt. Workers implement and check their candidate without writing to another worker's directory or manipulating the receiving branch. No per-worker PR is required unless target policy or shared-contributor claiming requires one.
7. **Integrate serially into the working target.** The coordinator merges completed worker branches one at a time under the covering dispatch approval, not straight into protected main by default. Run affected combined-result checks and resolve straightforward conflicts within scope. Re-dispatch corrective work only when needed under existing recovery limits; changed behavior or ambiguous conflicts Escalate. Complete required target-branch PR/CI/reviews wherever protection applies.
8. **Retain branch evidence.** Include worker logs in the receiving branch with the implementation, then carry them through eventual domain/scope publication before deleting branches. Record integration through existing evidence and native merge references; no evidence-only PR.
9. **Cross-reference the iteration log.** For every `execute/<stage-task>/W-<n>` recorded on a branch, the iteration log MUST contain the corresponding stage-task entry with a pointer to the branch-log path in `Notes`.

Any escalation on a parallel branch MUST halt further dispatch and surface to the Human User per [core §3.2](../../core-twtty-methodology.md#32-failure-handling).

### 5.2 Customization surfaces and runtime features

The bound harness exposes customization surfaces — repo-wide and pattern-scoped instructions, custom agents, skills, MCP servers, prompt files, hooks, and delegate — that the default agent configures on the Human User's behalf per the [§3 orchestrator framing](#default-agent-as-orchestrator). The concrete surfaces, when TWTTY configures each, their replay-log shapes, and the harness's async-delegation command are defined in the **active harness binding** (default: [`harness/ghcopilot.md`](config/harness/ghcopilot.md)). Configuration specifics (file paths, frontmatter fields, feature names, settings) evolve independently and are the default agent's responsibility to look up in current harness documentation.

Two rules are normative regardless of which harness is bound:

- **Trust-boundary surfaces require consent and provenance.** Surfaces that cross a trust boundary (MCP servers, hooks) MUST be **version-pinned and provenance-verified before install** (per [§7.1.1](#711-security-controls)), and the default agent MUST ask before configuring them.
- **Portable assets come from `reusable-assets/`.** Skills (and, later, MCP servers, hooks, prompts) meant to be reused across projects are bound via `runtimeconfig.md` → `reusable-assets` by pointing `skills` at a **directory** (see [`reusable-assets/`](config/reusable-assets/README.md)); the agent **inspects every skill in that directory and applies the ones that are applicable**, each of which describes its own capability and when it is relevant. Skills add capability, never authority — so the binding stays loosely coupled. Skills have two origins: **library skills** (shipped or external, bound as above — e.g. a UX skill) and **project-captured skills** the AI Agent authors itself. As it works, the AI Agent MAY distill a prompt it has already run into a reusable skill file in the project's own bound skills directory (under `<project-folder>/twtty-runtime-config/reusable-assets/skills/`), so later stages and resumes reuse it instead of re-deriving the same work. Capturing a skill is the AI Agent's dynamic judgement, is kept lean and deduplicated, and — being a local prompt template that crosses no trust boundary — produces no replay-log entry (see [`reusable-assets/` — Project-captured skills](config/reusable-assets/README.md#project-captured-skills)).

Work-item mirroring to an external tracker (GitHub Issues, Azure Boards, Jira, etc.) is an optional `devtools` feature, not a TWTTY-configured surface; `plan.md` §3.1 remains the source of truth (see [§9](#9-execution-rules)).

---

## 6. Guardrails profile

During the Plan stage, the Planning Agent guides the user through establishing industry-standard guardrails appropriate to the project. Guardrails are **negotiated, not prescribed**, and are determined through the TWTTY loop based on the project's scope, technology stack, and risk level. When the project binds `best-practices/` (and/or `technical-stack/`) in `runtimeconfig.md`, the Planning Agent MUST **build the architecture from that bound guidance** and record in `plan.md` how the design applies or deviates from it (with rationale for any deviation); when none is bound, it proposes current industry standards per the [core §4.5](../../core-twtty-methodology.md#45-rules) "propose industry standards" rule. Bound best-practices are SHOULD-level guidance — the plan remains the architecture's source of truth — unless a `policies/` binding elevates a specific item to MUST.

Four of the six guardrail categories are risk-tiered and enforced mechanically — for these, [§7.1 Risk calibration matrix](#71-risk-calibration-matrix) is the single source of truth; this section does not restate its content. The remaining two (Architecture, Process) are always-applicable PLAN-stage deliverables and execution conventions, not risk-tiered pass/fail controls.

| Category | Authoritative source | Captured in |
|----------|----------------------|-------------|
| **Security** | [§7.1.1](#711-security-controls), [§7.1.7](#717-identity-and-access-controls), [§7.1.8](#718-regulatory-overlay-controls-conditional) | plan §1.4 Security architecture, §2.4 Security design |
| **Quality** | [§7.1.2](#712-testing-and-code-review-controls) | plan §1.6 Test architecture, §2.5 Test design |
| **Operations** | [§7.1.3](#713-cicd-controls), [§7.1.4](#714-deployment-and-operations-controls) | plan §1.3 Infrastructure architecture, §2.3 Infrastructure design |
| **Agent & Tool Trust** | [§7.1.1](#711-security-controls) | plan §1.4 Security architecture (named consideration alongside secrets/access controls) |
| **Architecture** *(not risk-tiered)* | plan §1.1 Application architecture, §2.1 Application design | Separation of concerns, API contract design, dependency boundaries — built from the bound [`best-practices/`](config/reusable-assets/best-practices/) guidance where present |
| **Process** *(not risk-tiered)* | [§9 Execution rules](#9-execution-rules), plan §3 Orchestration | Change-management conventions, branch strategy, approval workflows |

Project-specific guardrail additions beyond this table are permitted with explicit Human User approval during PLAN, recorded in the applicable `plan.md` section per the [core §4.5](../../core-twtty-methodology.md#45-rules) "propose industry standards" rule.

---

## 7. Risk enforcement profile

This profile defines how the SDLC implementation enforces TWTTY at each [risk level](../../core-twtty-methodology.md#31-risk-calibration). This specialization instantiates the core calibration scale as a **1–5 risk ladder**, and binds the per-level enforcement to the active **`risk-calibration`** binding. The **per-level applied EXECUTE task set** (which stage tasks run at each level) is defined in the table below — this specialization owns its own stage-task taxonomy, so the bound ladder never names it. The calibration scale, the enforcement **posture** (gate strictness and context isolation per level), the §7.1 control matrices, and the **matrix application rule** are defined once in [`risk-calibration/default.md`](config/risk-calibration/default.md), the default ladder bound through `runtimeconfig.md`; the confirmed level — assessed at SEED and recorded in `meta/risk-level` — selects the column, and an org MAY bind its own ladder file instead. §7 and the bound profile together are the single source of truth for what MUST be applied at each level; the Planning Agent MAY add stage tasks or controls beyond the minimum when the project requires them.

**Applied EXECUTE task set by level.** The spec owns which of its [EXECUTE stage tasks (§3.4)](#34-execute) apply at each level; the control *values* within those tasks come from the bound `risk-calibration` matrices (§7.1).

| Level | Applied EXECUTE stage tasks |
|:-----:|-----------------------------|
| **1** | 3a, 3b, 3d (secret scanning only), 3f (basic happy-path smoke; formal tests/evals optional per §7.1.2), 3g (required CI), 3m; required local services/emulators or approved development-cloud dependencies add 3h after their dependency setup; hosting adds 3i |
| **2** | Level 1 task set with L2 verification controls + 3c, 3e; 3h/3i when applicable to selected infrastructure/cloud delivery, not mandatory hosting |
| **3** | Level 2 + 3j, 3k, 3l |
| **4** | Full EXECUTE set (3a–3m) |
| **5** | Full set (3a–3m) + regulatory overlay where a regime applies |

SEED assesses the project and records the active level in a `meta/risk-level` entry; **Level 1 is the floor** (core §3.1). The floor reduces this implementation's controls to the minimum but never waives the core obligations that hold at **every** level — the Approval Gates, the append-only replay-execution log, untrusted-input handling, and Human User authority ([core §4.5](../../core-twtty-methodology.md#45-rules)). The `policies/` binding and any `compliance/` regime confirmed for the project (at `spec §14`) may raise these controls; nothing may relax them.

**Integration follows repository policy.** Apply §5.1's sequential/domain/parallel topology at every level. Existing protection and stricter risk/policy controls remain mandatory; use a scope branch/PR when they prohibit direct work. Do not introduce per-item branches or worker PR approvals merely because a risk level is selected. Applicable review, test and publication checks still apply.

**Risk re-calibration across iterations.** **Subsequent iterations assume the most recently confirmed level by default** — the most recent `meta/risk-level` entry is always the active level (per [core §4.1](../../core-twtty-methodology.md#41-on-resume)), and a fresh `meta/risk-level` entry is required only to *change* it, which re-baselines the iteration's controls to the newly confirmed level. The level MAY change between iterations as a project matures (for example, an `Iteration-20261105T230435Z-7Q2K9F` level-2 internal prototype becoming an `Iteration-20261218T142010Z-3M8XP2` level-4 customer-facing service). **Within Levels 1–3, the Human User MAY set or override the level at their discretion** — the SEED assessment is advisory at these tiers, and moving to or between Levels 1–3 needs no re-calibration hard-guardrail (the Level 1 acknowledgment still applies whenever L1 is in effect). Confirming or raising to **Level 4–5**, or *lowering* the level for an iteration that ships to an already-production system, MUST be surfaced to the Human User as a hard guardrail and acknowledged in the `meta/risk-level` entry's `Notes`.

**Execution pattern selection (Sequential vs Parallel).** Every level may use either pattern under §5.1. Sequential is normal; reuse the current scope's recorded Human answer rather than asking twice. Parallel requires DAG-independent, footprint-disjoint work on isolated branches and covering approval recorded in `meta/execution-pattern`. Risk level governs applicable controls, not automatic parallel dispatch. Execution Mode (Interactive/Autopilot) remains independent.

Two Level-1-specific rules — the **Level 1 acknowledgment** (the AI Agent MUST enumerate the skipped controls to the Human User when confirming the level, obtain explicit acknowledgment that the project is a prototype NOT intended for real users, customer data, production traffic, or long-lived operation, and record it in the `meta/risk-level` `Notes`; absent it, `Escalate` per [core §3.2](../../core-twtty-methodology.md#32-failure-handling)) and the **Level 1 shortest-path deployment** rule (L1 takes the shortest path to a running build — local, or a single cloud demo/sandbox target opted in via a cloud `Runtime target` in the spec `## Metadata`; a cloud target adds 3g/3h/3i and makes CI/CD mandatory) — are defined in the active risk-calibration binding's [Level 1 rules](config/risk-calibration/default.md#level-1-rules).

If the bound harness cannot satisfy the isolation or gate requirements for the confirmed risk level, the agent MUST escalate per [core §3.2](../../core-twtty-methodology.md#32-failure-handling).

### 7.1 Risk calibration matrix

The concrete controls within those stage tasks — the full **L1–L5 matrices** and the **matrix application rule** — are defined in the active `risk-calibration` binding, [`risk-calibration/default.md`](config/risk-calibration/default.md). The [normative rule in §9](#9-execution-rules) requires the AI Agent to consult that matrix for the confirmed risk level before every EXECUTE stage task and before `SPEC-EXIT` / `PLAN-EXIT` / `EXECUTE-EXIT`. Identify every MUST row, including confirmed regulatory overlays, but verify each at its defined stage/checkpoint per the matrix application rule. Later implementation or runtime results are not early-stage gate prerequisites, nor may early approval be represented as proof of those future results.

The sub-sections below are retained as stable reference anchors; each maps to the correspondingly-numbered section of `default.md`.

#### 7.1.1 Security controls

Secret / SAST / dependency / license / container scanning, finding-severity merge gates, threat modeling, named-standard security review, untrusted-input handling, trust-boundary customization-surface provenance (see [§5.2](#52-customization-surfaces-and-runtime-features)), and replay-log scanning / append-only enforcement — see [`default.md` §7.1.1](config/risk-calibration/default.md#711-security-controls).

#### 7.1.2 Testing and code-review controls

AC-to-test traceability, test independence, diff/patch and cumulative coverage floors, the code-review checklist, and reviewer-context isolation — see [`default.md` §7.1.2](config/risk-calibration/default.md#712-testing-and-code-review-controls).

#### 7.1.3 CI/CD controls

Applicable native build/test/scan/integration, hosting-IaC/deploy checks, required reviews,
OIDC, SBOM, signing and provenance are defined in the bound risk matrix and devtools
provider. No custom methodology gate-check job or validator is generated.

#### 7.1.4 Deployment and operations controls

IaC-only provisioning, deployment strategy and rollback, smoke tests with auto-rollback, SLOs, and alert-to-SLO tracing — see [`default.md` §7.1.4](config/risk-calibration/default.md#714-deployment-and-operations-controls).

#### 7.1.5 Setup and repository controls

`.gitignore`, `LICENSE`, `README.md` (per the [project README template](../../../templates/project-readme-template.md)), branch protection, and `CODEOWNERS` — see [`default.md` §7.1.5](config/risk-calibration/default.md#715-setup-and-repository-controls). How branch protection and `CODEOWNERS` are expressed comes from the active [`devtools`](config/devtools/) binding.

#### 7.1.6 Data controls

Data classification, PII flagging, retention windows, encryption in transit / at rest, current cryptographic algorithms, and data-flow diagrams — see [`default.md` §7.1.6](config/risk-calibration/default.md#716-data-controls).

#### 7.1.7 Identity and access controls

Cloud-agnostic controls: CI-to-cloud OIDC / short-lived credentials, app-runtime workload identity, RBAC-in-IaC at least-privilege scope, disabled local-auth, workload-identity registry pull, and identity-before-deploy sequencing — see [`default.md` §7.1.7](config/risk-calibration/default.md#717-identity-and-access-controls). The provider-specific implementation (managed identity vs IAM role vs service account; the IaC language; the registry) comes from the active [`cloud`](config/cloud/) binding and the iteration's `Runtime target` metadata.

#### 7.1.8 Regulatory overlay controls (conditional)

Applies only when a named regime (SOC 2 / HIPAA / PCI-DSS / GDPR / derived) is confirmed via `spec §14` or Human User declaration — gated by confirmed regime membership, not by risk level. Because this overlay is **regime-gated, not risk-level-gated**, its control matrix lives with the compliance binding rather than the risk ladder: the overlay rows (access logging, managed-key encryption, data-subject rights, audit-log retention, breach notification, subprocessor agreements, independent audit) are the canonical [regulatory controls](config/governance/compliance/regulatory-controls.md#regulatory-controls) matrix, and the bound [`compliance/`](config/governance/compliance/) profile selects which regimes apply. This is a starting checklist, not a substitute for qualified legal/compliance review, which the AI Agent MUST recommend whenever a regime is confirmed.

**Expectation by level.** Compliance is gated by confirmed regime membership, not by risk level, but a rough expectation tracks the ladder: **L1** — no regime expected (if regulated data comes into scope, re-calibrate up rather than bolting compliance onto L1); **L2** — not expected; **L3 / L4** — if a regime applies, bind the matching [`compliance/`](config/governance/compliance/) profile (its MUST rows ratchet the level's controls up); **L5** — a regime is expected. Whenever a regime applies, bind the matching profile and recommend qualified legal/compliance review.

## 8. SDLC-specific rules

These rules are specific to software delivery and extend (do not replace) the core rules.

- In this implementation, deployment and operations are part of EXECUTE, not separate top-level stages.
- EXECUTE follows the approved plan in the §5.1 working topology: implement and verify locally, integrate worker results into their working target, then publish domain/scope results through required repository controls. Domain/parallel isolation, not work-item count, determines branches. Hotfix Scopes retain §3.5's separate incident procedure; external tracker mirrors remain optional.

### 8.1 SDLC-specific replay-log extensions

This implementation defines nine additional `meta/*` entries and one additional replay-log layout beyond those defined in [core §2](../../core-twtty-methodology.md#replay-execution-log-format), under the extension permission stated there.

#### 8.1.1 Additional meta entries

- **`meta/continuation-assignment`** — records an explicitly approved change or resolution of responsibility for continuing a baseline/Iteration. `Approval outcome` is `Approved` or `Approved with changes`; `Execution outcome` is `continuation responsibility assigned`. `Notes` references the affected scope, prior SEED/assignment evidence when available, the successor's native Human confirmation and the approval authorizing the assignment under project policy. Use safe native evidence references, not real identities copied into redacted records. When historical responsibility cannot be established, disclose that limitation and record a current approved assignment, never an invented historical starter. Append through the existing authorized publication process before successor lifecycle execution. Contributor claims, historical approvals, paused-state restrictions and Autopilot grants remain separate; this record does not transfer them.
- **`meta/execution-pattern`** — records the current scope's Human-selected pattern, reusing its Discovery/earlier answer rather than asking again. `Approval outcome` is `Approved` or `Approved with changes`; `Execution outcome` is `sequential selected` or `parallel enabled`. `Notes` references the Human answer and applicable plan; Parallel also records eligible domain-qualified items, working/worker targets, cap (`≤ 5`) and cost/time constraints. Record before EXECUTE. Plan changes require affected eligibility checks and an updated entry where material; only scope/constraint changes beyond the grant require new Human authorization.
- **`meta/branch-open`** — first branch-log entry, `Execution outcome: branch opened`. `Notes` identifies scope/Iteration ID, domain, selected domain-qualified work items (or Hotfix ID and paused Iteration), receiving working branch and dispatch decision. For an internal worker, reference the approved parent dispatch/claim; do not invent a separate Human approval. Record once per actual branch, not per sequential item; active-scope references follow §8.1.2.
- **`meta/branch-close`** — final branch-log entry before integrating its completed domain/worker/scope, not each work item. `Approval outcome` is `Approved`, `Execution outcome` is `branch closed; ready for integration`. Reference delivered items or Hotfix ID, validated delivery revision, checks and branch-entry IDs. Candidate changes invalidate affected evidence and require an appended replacement close after revalidation; never rewrite prior entries.
- **`meta/branch-integrated`** — active-scope integration record, `Approval outcome: Approved`, `Execution outcome: branch integrated`. Reference delivered items/Hotfix ID, source/receiving branches, validated source revision, actual native merge/PR reference, applicable branch-entry IDs and combined-result checks. Append in the receiving working context at the next ordinary evidence update, batching related integrations when appropriate. Do not predict a resulting SHA or create an immediate evidence-only PR; native Git/platform merge history is authoritative until the next regular publication.
- **`meta/iteration-pause`** — the AI Agent pauses the active Iteration to open a Hotfix Scope (see [§3.5](#35-hotfix-path-production-incident-fast-path)). `Approval outcome` MUST be `Approved` or `Approved with changes`. `Execution outcome` MUST be `iteration paused for H-<token>`. `Notes` MUST record the paused Iteration ID, Hotfix Scope ID, and triggering incident.
- **`meta/iteration-resume`** — the AI Agent resumes a paused Iteration after the corresponding Hotfix Scope reaches approved `HOTFIX-EXIT`. `Approval outcome` MUST be `Approved`. `Execution outcome` MUST be `iteration resumed after H-<token>`. `Notes` MUST identify the same paused Iteration ID and Hotfix Scope ID, and reference the approved closing entry. It MUST be later than its matching pause.
- **`meta/config`** — the AI Agent records initial resolution, an approved update/refresh, or validated reuse per the [Config interview](#config-interview). `Approval outcome` MUST be `Approved` or `Approved with changes`. `Execution outcome` MUST be `config resolved`. `Artifact / path changed` MUST include `<project-folder>/twtty-runtime-config/runtimeconfig.md` and any config files created or updated. `Notes` MUST identify materialization, update, refresh, or unchanged reuse; list the resolved `harness`, `devtools`, `cloud`, `risk-calibration`, and `policies` selections; record explicitly overridden setting names/customized profiles and the adopted default source when resolving or refreshing; and record any binding that could not meet a required control (which MUST then have been escalated). Unchanged reuse MUST NOT be described as a file modification. The confirmed regulatory regime remains in `spec §14`; any resulting config selection is recorded here. Each iteration records its effective config, even when reused; authorized changes append a fresh entry, never rewrite earlier ones.
- **`meta/budget`** — the AI Agent records a build-tokenomics checkpoint against the active `tokenomics/build` budget (see [§9 Honor the build-tokenomics budget](#9-execution-rules)). `Execution outcome` MUST be `budget checkpoint` or `budget exceeded`. `Notes` MUST record cumulative build-time token / cost / wall-clock usage and the remaining budget; a `budget exceeded` outcome MUST have been escalated per [core §3.2](../../core-twtty-methodology.md#32-failure-handling) unless the cap was explicitly re-approved.

#### 8.1.2 Branch-scoped replay logs

Use a branch-scoped replay log for actual domain/parallel branches and independently
claimed contributor contexts. Sequential direct development uses the active scope log.
Sole-writer Sequential work through a policy-required scope PR may also use that log without a duplicate
auxiliary log or branch-open/close ceremony. Keep its actual source/receiving context,
validated revision, PR/merge and checks in ordinary scope evidence using safe references.
This does not waive required PRs, CI/reviews, shared claims or worker/domain isolation.
Existing branch logs remain authoritative and must continue/close under these rules,
not be abandoned to switch layouts. Carry branch evidence with the implementation into
its receiving working branch and eventual repository integration, not in separate
evidence-only PRs.

- **Location on the branch.** New logs use `<project-folder>/replay-execution/branches/<scope-id>-<branch-token>-execution-log.md`, where `<scope-id>` is the Iteration ID or Hotfix ID, or `baseline` for baseline work. Allocate a random 32-hex reference once under the shared utility's [branch-evidence procedure](../../../tools/README.md#branch-evidence-tokens); no key or hash of the native name is required. Never copy raw branch names into new evidence filenames.
- **Private branch references.** Use the same token in structured `Branch reference` fields, source/receiving-branch references, Notes and derived state. Resolve native names privately from approved Git/PR context for actual operations; native Git refs and PR head/base metadata remain unchanged. Do not persist a raw-name-to-token map. Recover the allocated reference from opening/claim/dispatch evidence, never regenerate it on Resume. Missing or inconsistent recovery evidence blocks rather than selecting another log. Existing project-keyed references remain supported with their adopted key; do not silently replace them.
- **Stable filename.** Reuse the recorded token across sessions, not a fresh allocation per invocation. The filename MUST NOT add a timestamp beyond the timestamp already contained in its stable Iteration ID. Scope ID and branch reference provide stable uniqueness; event time belongs in each entry's required `Timestamp` field and commit history.
- **Sequence IDs on the branch log.** New logs use `br-<branch-token>-<n>`, where `<n>` is a zero-padded integer starting at `001`.
- **Legacy compatibility.** Existing non-identifying legacy filenames/IDs may continue unchanged on Resume. Never silently rename files, rewrite entries or reset counters to adopt tokens. If a legacy name/ID contains sensitive identifiers, block new exposure and obtain the existing explicit privacy-remediation approval before extending or copying it. Historical records remain intact.
- **First entry on the branch log.** MUST be a `meta/branch-open` entry (see §8.1.1).
- **Final entry on the branch log.** Use `meta/branch-close` when that branch's approved scope is ready for integration, not after every sequential item. An affected candidate change requires revalidation and a new appended close; an unrelated main-branch advance alone is not a reason to rebuild or rewrite logs.
- **Active-scope-log cross-reference.** The baseline, Iteration or Hotfix replay-execution log MUST record branch work through the corresponding stage-task entries and MUST record completed integration through `meta/branch-integrated`. Each reference MUST identify the safe branch-log path and exact `br-<branch-token>-<n>` entry IDs relied upon, or verified non-identifying legacy IDs under the compatibility rule; branch entries MUST NOT be copied into the active-scope log.
- **Archive with implementation.** Commit branch logs with the work and retain them through worker-to-domain and domain/scope-to-integration merges. A local worker merge does not require a separate PR merely to archive its evidence. Do not delete the only reachable copy of required evidence.
- **Immutability.** Recorded branch-log entries MUST NOT be edited, reordered or removed, before or after archive. Append corrections to the current scope's log, referencing the exact archived branch entry and preserving the originals. `meta/backfill` records authorized artifact drift; it never authorizes rewriting replay history. Necessary privacy/history remediation requires the separate explicit approval and integrity safeguards in core §2, not a general backfill exception.
- **Resume behavior.** Identify the current context from its actual branch, opening evidence and applicable plan, never the newest archived log. Direct Sequential work uses the active scope log. A domain/shared-contributor claim or internal worker's recorded parent dispatch identifies selected items and receiving target; an internal worker does not need its own PR when its parent claim/authorization covers it. Verify identity, authorization, pause status and unfinished evidence, including a branch with only `meta/branch-open`. Missing/conflicting evidence is drift; a required shared-contributor claim still must be published before implementation. Recover legacy identities only when unambiguous without rewriting history. Reuse valid setup, never acquire unrelated work on Resume, and report abandoned/escalated/integrated claims with next actions. Active-scope and branch integration evidence must agree; do not concatenate branch logs into a global chronology.

### 8.2 Domain-based separation of responsibilities

A **domain** is a coherent area of responsibility in the system — related behavior, data, and code that changes together and can be owned as a unit (for example, *identity*, *billing*, *notifications*). Domains keep concurrent work from colliding and make ownership explicit: each domain owns a **disjoint slice of the codebase**, and every work item stays inside one domain's slice.

**Two independent knobs — do not couple them.** Domains have two orthogonal dimensions:

1. **Structure** — how the system is partitioned into domains — scales with **system complexity**. A single-purpose system is **one domain**; a system with several clear areas of responsibility is partitioned, *even for a solo developer*, because the partition organizes the work and lets parallel work items (or AI subagents) run in isolation.
2. **Ownership enforcement** — CODEOWNERS-required review by *distinct people* — scales with **team size**. It is meaningful only with two or more Human Users. With one Human User, domain boundaries are organizational (self-reviewed); with a team they become mechanically enforced approval boundaries.

So: simple + solo → one domain, no ceremony. Complex + solo → domain *structure* for organization and isolation, self-review. Complex + team → structure **plus** enforced per-domain ownership.

**The Human User is never required to know this model.** The AI Agent elicits ordinary requirements and use cases (Discovery is unchanged), then **derives** the domains itself and presents them in plain language — *"here is how the system divides into areas of responsibility."* The Human User reviews, corrects, or **overrides** the split in plain terms — real teams already own areas (Conway's law), so the AI Agent proposes but the Human User's domain map is authoritative. The AI Agent MUST NOT require domain-modelling vocabulary of the Human User.

**Layers.** Beyond business domains, two cross-cutting layers own the shared substrate — each with its own footprint and owner. **Business domains MAY depend on them; never the reverse** (dependencies flow downward only and MUST NOT form a cycle):

| Layer | Owns (typical footprint) | Concern |
|-------|--------------------------|---------|
| **Business domains** | `src/<domain>/**` | product areas of responsibility |
| **App platform** | `platform/**` | shared application substrate — identity/auth, shared services, common libraries |
| **Infra** | `infra/**`, the bound devtools CI path (e.g. `.github/workflows/**`) | IaC, pipelines, cloud resources, environments, observability |

An optional thin **shared-business** domain (`shared/**`) exists only when there is shared business logic that is not platform. A business domain needing a change to app-platform or infra opens a **pull request to that layer, gated by its owner** — so cross-cutting files (`package.json`, CI, IaC, shared libraries) always have one clear home and owner, and the disjoint-footprint rule never forces two domains to fight over a shared file. App platform and infra are the same domain machinery (footprint + owner + spec/plan slice) applied to the technical substrate that [§7.1.7](#717-identity-and-access-controls), [§9](#9-execution-rules), and stage tasks 3g/3h/3k/3l already govern.

**Proportional by default.** The default is **one domain at the repository root** — no layers, no `domains/` split, no per-domain owners, no ceremony. The layered, partitioned apparatus appears only when the AI Agent's analysis (confirmed by the Human User) finds genuinely separate areas of responsibility. A church site or a URL shortener sees none of it.

**How each stage realizes it:**

1. **SPEC identifies domains ([§3.2](#32-spec)).** The AI Agent records the derived domains and the layer map, and attributes each use case and requirement to a domain. A multi-domain system uses a **hub-and-spoke** spec: an overview (`spec/spec-<iteration-id>.md` — goals, the domain/layer map, cross-domain journeys, and links; interfaces are a PLAN concern per §3.3) plus one file per domain (`spec/domains/<domain>-<iteration-id>.md` — that domain's use cases, FR, NFR, ACs). Whole-system foundations (data classification, plus the whole-system UX (§13) and API (§15) requirements) live in the overview; domain-specific instances live in the domain files. A single-domain system stays a single `spec-<iteration-id>.md`.
2. **PLAN structures them ([§3.3](#33-plan)).** The full shape has an overview (`plan/plan-<iteration-id>.md`) and per-domain plans (`plan/domains/<domain>-<iteration-id>.md`). Later Iterations retain the current work-item index, DAG, and pattern selection, update affected slices, and reference valid unchanged approved maps/designs. Every current `W-<n>` maps to one domain and stays within its effective footprint. Interfaces and a domain diagram are needed only with multiple domains; unchanged approved diagrams need not be copied.
3. **EXECUTE realizes them ([§3.4](#34-execute)).** Each domain and layer is a **folder** whose path is its footprint (`src/<domain>/`, `platform/`, `infra/`). At 3a Setup, `CODEOWNERS` maps each domain and layer footprint to its owner; with a team (2+ Human Users) a pull request touching a domain requires that domain's owner's review.

**The isolation guarantee (mechanical).** Domain isolation is enforced by footprints at `PLAN-EXIT` and at dispatch: each domain and layer declares a footprint; footprints MUST be **mutually disjoint**; every `W-<n>`'s expected footprint (`plan.md` §3.1) MUST be a **subset of its domain's footprint**. Because footprints are disjoint and every work item nests within its domain, any two work items in **different domains are automatically footprint-disjoint** — always safe to run concurrently — so the per-pair footprint check in [§5.1.1](#511-parallel-pattern-discipline) is decisive only *within* a domain. Domains are the coarse-grained unit of both ownership and safe concurrency.

**Domain integration.** Branch topology follows §5.1; infrastructure ownership does not dictate a separate initial-setup branch. Domain ownership, footprints and required cross-domain reviews remain.

**Domains evolve.** Splitting, merging, or renaming a domain across iterations is **normal tracked work**: it is declared as work items in the iteration's plan (with the file and folder moves as their footprint) and the overview domain/layer map is updated — no special mechanism.

**Relationship to components.** A domain is coarser than a component (`plan.md` `C-<n>`): a domain groups components. Footprints are the physical realization of a domain's slice; the disjoint-footprint discipline in [§5.1.1](#511-parallel-pattern-discipline) is the execution-time mechanism. Domains add the *why*, the *ownership*, and the *boundary*; footprints remain the *mechanism*. How gates and ownership work across multiple people is defined in [§8.3](#83-multi-developer-collaboration).

### 8.3 Multi-developer collaboration

More than one Human User (core defines the Human User as a *team*) collaborates on one project through the **shared repository as the coordinator** — no central agent, no consensus protocol. Two layers keep it simple.

**Local gates (private).** Each Human User runs the loop in their own authorized working context. Concurrent writers, including concurrent Iterations or contributors within one domain, MUST use distinct branches and isolated worktrees/clones. An idle domain branch may be reused exclusively for sequential continuation; never share its checkout concurrently. Use the active scope log for direct Sequential work and branch evidence only where §8.1.2 applies.

**Work pickup is proposed, not assigned in PLAN.** `plan.md` §3.3 Team
collaboration remains assignment-neutral. Only when a Human explicitly requests
finding/recommending ready, unclaimed work with `twtty resume`, the AI Agent
considers open, planned Iterations within any requested Iteration/domain scope and
groups eligible `W-<n>` items by domain. Ordinary Resume never scans/ranks global
assignments or replaces an existing claim. A work item is eligible only when its
Iteration is not paused, dependencies are verified in the receiving working
context (including required cross-domain integration), it is not complete,
no open pull request claims the same `(Iteration ID, domain, work-item ID)`,
and its expected footprint does not collide with active work. Overlapping
work remains ordered under the existing footprint rules; an integration
checkpoint does not by itself authorize simultaneous conflicting edits. The AI Agent MUST
rank and present clickable proposals, placing its recommendation first and
explaining dependencies, critical-path value, work unblocked, footprint
isolation, testability, and review scope. It MUST NOT assign work until the
Human User selects a proposal.

After selection, the AI Agent MUST refresh the remote and repeat the eligibility
check, then establish an exclusive domain context or isolated parallel-worker
branch under §5.1, recording the receiving working target and scope identity.
Reuse that context for its selected sequential bundle, not a branch per item.
For shared contributor pickup, publish a draft PR or equivalent visible claim
against the receiving working branch and recheck competing claims before writing.
An internal orchestrated worker may be covered by its parent's shared claim and
recorded dispatch; it needs no extra PR solely to merge locally.
The shared claim and branch-opening evidence MUST agree on this identity:

```text
Iteration: <iteration-id>
Domain: <domain>
Work items: <complete list of domain-qualified W-IDs>
Branch log: <canonical path>
```

That change request is the shared claim. Check every bundled item's complete
identity, not only the title's primary W-ID. A competing claim
wins by the bound platform's creation timestamp, with change-request ID as the
tie-breaker. Immediately after opening its claim, the AI Agent MUST refresh
remote claims; a losing Agent closes its later claim, records `Abandon`, and
refreshes the proposals. Closing any claim without merge requires an `Abandon`
or `Escalate` entry before the work becomes eligible again. Starting work this
way joins the existing Iteration; it never creates another Iteration. Later
sessions in the claimed branch or worktree use `twtty resume`.

**Bounded recovery.** An unfinished hotfix, no eligible work, or a lost claim
returns a clear status and actionable choices; it MUST NOT start a polling
loop waiting for another developer or a PR. Remote failures follow the
existing finite retry limits, then Escalate. Unknown claim or pause identity
MUST be resolved from evidence, not treated as available work. A missing
resume after verified approved `HOTFIX-EXIT` is repaired and published under
§3.5; it is not a reason to wait indefinitely.

**Fast coordination path.** Share one boundary-scoped metadata snapshot across
dispatcher, eligibility, claim, and pause checks instead of repeating the same
queries in each rule. Reuse verified evidence when its source revision is
unchanged. Refresh before claim publication after Human selection, after
publication, and immediately before merge/deployment; a stale snapshot MUST
NOT authorize those actions. Routine local edit/build/test cycles require no
additional PR-history scans or coordination-only model turns. Inspect only
candidate work and affected active footprints; broad reconstruction is a
missing/inconsistent-evidence recovery path, not normal execution. Record
derived index updates at the existing log/state cadence, without another file
or documentation cycle.

**Shared gates (authoritative).** Work becomes shared truth only through two **native platform gates**:

1. **Repository publication gates** apply where policy requires them. Protected integration uses required PR checks and reviews; local approval is only a working checkpoint until they pass and merge. Reuse the domain/scope PR rather than create a PR per work item or integration receipt. Authorized unprotected Sequential work may publish directly, completing applicable CI before claiming shared completion. Worker integration into an unprotected working target is routine pre-authorized work, not a new stage-exit or Human approval gate.
2. **Deployment gates** gate **iteration into a shared or production environment** — required reviewers on the environment, the same primitive as the production-promotion hard guardrail in [§9](#9-execution-rules). This is the "safe to ship to real users" approval, which is inherently centralized.

**Concurrency is the platform's.** Two reviewers disagreeing on a spec PR is resolved by native pull-request semantics: `request changes` **blocks** the merge, a new commit **dismisses stale approvals**, and the PR merges only when the branch-protection policy is met. No approval silently overrides a rejection. TWTTY adds no consensus machinery.

**Ownership is enforced by CODEOWNERS — proportional to team size ([§8.2](#82-domain-based-separation-of-responsibilities)).** With a team, `CODEOWNERS` maps each domain and layer path to its owners, so a change to a domain's spec, plan, or code cannot merge without that domain's owners' approval — **no domain team can override another's.** With a single Human User this is self-review and the boundaries are organizational only. Because enforcement scales with team, `CODEOWNERS` MUST be present at **any** risk level once a project has 2+ Human Users — in addition to the L3+ requirement in [§7.1.5](#715-setup-and-repository-controls).

**Spec finalization is domain-scoped.** In a hub-and-spoke spec each domain's team finalizes its own `spec/domains/<domain>-<iteration-id>.md` (CODEOWNERS-enforced), and `SPEC-EXIT` is the aggregate — every domain spec plus the overview approved. When the single-file `spec-<iteration-id>.md` is used instead (the Human User's choice for a simpler project), domain finalization is a **review rule** rather than a path-owned guarantee: the spec's domain tags make each item's owner legible, a change to a domain's items requires that domain's owners' approval on the spec PR, and no domain overrides another. Product Managers and developers collaborating on a spec is expected; collaboration happens on the way to the spec PR's approval.

**Gate realization tracks the platform.** Artifacts/evidence are committed and published from first contact. Direct bootstrap publication through PLAN is permitted only for a new repository where authorized and unprotected. Existing repositories retain their integration branch and required PR/CI/review process from SEED onward; a first baseline does not imply absent protection. The authoritative gate is the reviewed, CI-passing merge where PR-gated, not local approval alone. EXECUTE uses §5.1's topology: no per-item PR, and no removal of required protection. Deployments keep their separate applicable gates.

---

## 9. Execution rules

These rules extend the core TWTTY rules ([§4.5](../../core-twtty-methodology.md#45-rules)) with software-delivery specifics.

**Failure limits.** Baseline SDLC and its agentic/data-engineering extensions allow **1 automatic retry per failing operation within a stage task**, after the initial attempt (**2 attempts total**). A failed retry MUST escalate under core §3.2. Allow **3 refinement cycles per active artifact**; on reaching that limit without convergence, follow core's `Abandon` rule. Retry counts reset only after the operation succeeds or the Human User approves a materially different recovery scope. Refinement counts reset after artifact approval; after abandonment, a new scope requires Human approval. Rephrasing a prompt, editing a file, changing a task label, or rolling context MUST NOT reset either count. If counts cannot be recovered, escalate rather than assume zero. `Abandon`/`Escalate` outcomes are logged per core. These limits do not waive approval, budget, or trust-boundary controls, and the extensions inherit them unless they specify stricter limits.

- **Never skip a gate.** At risk levels 4–5, all gates MUST be enforced (see [Section 7](#7-risk-enforcement-profile)).
- **Consult the risk calibration matrix before every gate.** Before executing any EXECUTE stage task and before requesting `SPEC-EXIT`, `PLAN-EXIT`, or `EXECUTE-EXIT`, consult [§7.1 Risk calibration matrix](#71-risk-calibration-matrix) and identify every applicable MUST row for the confirmed risk level and overlays. Verify the controls due at this stage/checkpoint per the bound matrix application rule: SPEC requirements, PLAN design/dependencies, and implementation/results at their EXECUTE, merge, or deployment checkpoints. Surface due non-mechanical controls for Human attestation. Do not demand future-stage artifacts to pass an earlier gate, count a planned control as implemented, or defer a control beyond its required checkpoint. Immediate approval, trust-boundary, redaction, and log-integrity controls apply throughout.
- **Use native checks and truthful evidence.** Reuse required application tests/CI/scanners, provider results, Git/PR history and native approval metadata. Verify methodology artifacts directly against the actual applicable checklist, recording the method and limitations rather than claiming an unrun machine verdict. Do not generate TWTTY replay-log/identifier, methodology Markdown/schema or gate-check validators, their synthetic test suites, or methodology-only CI workflows. The shared privacy utility and its focused maintainer tests under core §2 are the sole framework-privacy exception; use that utility at risky evidence writes, not generated project-local copies/wrappers. This restriction does not prohibit approved application validation/evaluation/safety code. Native required app checks/reviews still block integration when missing/failing, and external policies remain binding. Keep secrets/identifiers out of candidate evidence under core §2; a secret scanner is not an exhaustive identifier detector. Do not copy native real identities into redacted records.
- **Infrastructure is IaC-only.** All approved development-cloud creation/updates use reviewed IaC at every level; hosting resources use IaC at L2+ and L1 cloud per [Level 1 rules](config/risk-calibration/default.md#level-1-rules). Use self-contained selected environments under `infra/environments/`, preserving approved existing layouts/owners. No shared/cross-environment IaC modules or duplicate ownership; authorized existing resources may be referenced without takeover. Raw CLI resource creation/portal clicks are prohibited. Developer-machine IaC apply is limited to approved minimal local-development dependencies per the provider binding, one-time identity bootstrap and logged break-glass. Hosting foundations stay CD-owned. Unauthorized resources created outside IaC are drift and need approved correction before the next `PLAN-EXIT`.
- **Honor environment purpose and ownership.** Apply the [development profile's ownership rule](config/development/default.md#environment-iac-and-resource-ownership) consistently in design, configuration, work footprints and execution. Changed approved plans/config require refinement and recorded approval; historical logs and published releases are not rewritten.
- **Cloud-hosting deploys originate from CI/CD.** At L2+ and L1 cloud, hosted code/infrastructure deploys use the bound `devtools` pipelines and are traceable to merged PRs. Developer/portal hosting deploys are prohibited except approved one-time identity bootstrap or logged break-glass. Approved minimal local-development IaC through developer Azure CLI is a separate pre-merge preparation path, not a hosting release.
- **Identity before code (mandatory for cloud hosting).** A **`W-<n>-identity-bootstrap` work item is REQUIRED before dependent cloud-hosting/pipeline work**, unless verified reusable CI↔cloud trust already covers it. Sequence it in `plan.md §3.2`; document OIDC federation, hosted workload identity and IaC RBAC in §1.4, and verify applicable controls at PLAN/EXECUTE exits. This hosting bootstrap does not precede unrelated developer-service preparation under the development profile. For hosting bootstrap, present the target/change, obtain required approval and verify actual federation/RBAC before dependent hosting work. Reuse suitable authorized identities; no portal/raw-create, client-secret or unapproved role shortcut. The provider binding supplies current commands.
- **Version control from SEED (remote required).** Establish or reuse the project repository and approved **remote** at **first contact** per [§3.1](#31-seed), not EXECUTE. Every approved artifact — seed, resolved config, spec/plan/domain files, replay log, state and diagram — MUST be committed and published as produced, anchoring evidence to pushed commits. Publication preserves the configured integration branch, remotes and existing PR/CI/review controls from SEED onward. Direct bootstrap pushes through PLAN are allowed only for a new repository where authorized and unprotected; no onboarding exception bypasses existing protection. EXECUTE follows §5.1's sequential/domain/parallel topology. Remote establishment/authentication remains a trust-boundary action per [§5.2](#52-customization-surfaces-and-runtime-features). If authorized publication cannot be completed, `Escalate` under [core §3.2](../../core-twtty-methodology.md#32-failure-handling); do not bypass controls or claim the gate passed.
- **Use branches only for isolation or required publication.** Follow §5.1: no extra branch for single-domain Sequential work where direct development is permitted; one working branch per affected domain otherwise; separate isolated branches for concurrent writers. Reuse one scope branch/PR if existing or stricter policy requires it. Worker merges into an authorized working target need no new approval within the covering dispatch, but protected targets retain required PR/CI/review controls. Never force-push, disable protection or use an administrator bypass to avoid those controls. Hotfix Scopes keep §3.5's incident branch.
- **Use plan-based work management.** Each execution item maps to `plan.md` §3.1; commits and applicable PR descriptions reference delivered domain-qualified `W-<n>` items. A branch/PR can carry the whole domain or sequential scope. Optional issue mirrors reference plan IDs, never replace the plan. Hotfix Scopes use their incident record and Hotfix ID.
- **Avoid protection-driven churn.** Read actual branch/ruleset requirements before publication. Refresh a domain/scope candidate when it reaches integration, then run affected checks and every required target check; use a merge queue when available and approved. Do not repeatedly synchronize all idle branches after unrelated merges, rerun unaffected suites merely for bookkeeping, or create evidence-only PRs. Native merge records provide the resulting revision; append concise integration references at ordinary publication. A stale/failed required check still blocks integration; this is not permission to disable strict up-to-date protection.
- **Optimize for token and context efficiency.** The AI Agent SHOULD minimize context-window usage and the number of LLM calls, provided no gate, approval, self-review, or traceability requirement is weakened. The concrete efficiency techniques are the **Agentic development → Context & window discipline** guidance in the bound `best-practices` bundle (see [`best-practices/`](config/reusable-assets/best-practices/)). This operationalizes the core [context-bounding rule](../../core-twtty-methodology.md#45-rules) for software delivery and MUST NOT be used to justify skipping a required stage task, gate, self-review, or replay-log entry.
- **Honor the risk level.** Use the context-isolation and gate-strictness defined in [Section 7](#7-risk-enforcement-profile) for the confirmed risk level.
- **Honor the active bindings (contract-or-Escalate).** The AI Agent MUST operate on the complete project-owned [capability bindings](#11-capability-bindings-config) in `runtimeconfig.md` and its local config tree (`harness`, `devtools`, `cloud`, `development`, `risk-calibration`, `policies`, `best-practices`, `technical-stack`, `reusable-assets`, `tokenomics`). Required missing settings/files are configuration errors, not permission to fall back to shared defaults. Each bound provider states how it satisfies the controls the active `risk-calibration` requires; if a binding cannot satisfy a required control, the AI Agent MUST `Escalate` per [core §3.2](../../core-twtty-methodology.md#32-failure-handling) rather than silently degrade. The `policies` binding and any `compliance/` regime confirmed for the risk level (`spec §14`) ratchet controls up, never down.
- **Honor the build-tokenomics budget.** When the active `tokenomics/build` binding sets a non-`none` cap (tokens / cost / wall-clock), the AI Agent MUST track cumulative build-time usage in `state.md` to the extent the bound harness reports it (wall-clock is always measurable; tokens and $ only if the harness surfaces them), record `meta/budget` checkpoints (see [§8.1.1](#811-additional-meta-entries)), and `Escalate` per [core §3.2](../../core-twtty-methodology.md#32-failure-handling) before exceeding a cap rather than silently continuing (this reuses the Autopilot cost guardrail); if the harness cannot report a capped dimension, the AI Agent MUST `Escalate` the inability to enforce rather than silently ignore it. This build-time budget is distinct from the product runtime budget, which for agentic apps remains the `sdlc-for-agentic-apps` §11 gate.
- **Production promotion is a hard guardrail.** Where [§7](#7-risk-enforcement-profile) makes 3i Deployment applicable (L2+), the environment `plan.md §1.3 Infrastructure architecture` designates as serving real users, real customer data, or production traffic is the iteration's production environment. The first `execute/3i/W-<n>` deploy targeting that environment in an Iteration MUST receive explicit Human User approval per [core §1](../../core-twtty-methodology.md#execution-modes), even under Autopilot with a recorded scope that would otherwise cover it. Subsequent deploys to the same already-approved production environment within the same Iteration follow the recorded Autopilot scope normally.

---

## 10. UX quality bar

Apply `UX-001`-`UX-014` and the bound [`ux` profile](config/ux/default.md) when the scope ships
user-facing UI. Otherwise record UX mode `N/A` with Human confirmation.

The [UX control matrix](config/risk-calibration/default.md#718-ux-controls) is authoritative
for UX outcomes and default level applicability. Apply universal `UX-*` controls and every
selected level-sensitive `UX-*` control; the bound profile may strengthen but not redefine them.

**L1 routine design approval under Autopilot.** When the Human's grant explicitly
delegates routine L1 rendered-design review, apply UX-005's L1 approval route. The
Agent must actually render/exercise the affected prototype and inspect the required
design evidence before approving it under that grant; label it AI-reviewed, never
Human-rendered approval. Interactive/L2-L5/stricter Human-only requirements remain.
An existing spec explicitly requiring Human review needs an approved refinement before
using this route; never silently upgrade copied project profiles or rewrite old approvals.

UX mode is **Delegated**, **Interactive**, or **N/A**. Delegated mode requires rationale for
non-trivial choices; Interactive mode co-decides them with the Human.

| Stage | Canonical home | Action |
|---|---|---|
| SPEC | `spec.md` UX section | Record mode and selected testable UX outcomes. |
| PLAN | `plan.md` UX-design section | Apply the bound design skill and record the selected design/evidence. |
| EXECUTE | affected work items | Implement the approved design and collect selected evidence. |

Wireframes are incremental, not baseline-only. Every later Iteration that
changes a screen, workflow, state, component, token, or theme MUST create
current wireframes and interactive prototypes for each affected surface under
`plan/wireframes/<iteration-id>/` during PLAN. It MAY use prior approved
artifacts as inputs, but MUST NOT overwrite them. Unaffected surfaces MAY
remain reference-only when the impact analysis below proves them unchanged.

Apply the complete selected process only to affected surfaces. Reuse unchanged artifacts only
when [UX impact analysis](#ux-impact-analysis) preserves their evidence. Name the design skill by role in Spec/Plan;
record its concrete identity and pinned version in runtime configuration and
`meta/skill-install`. Templates define the exact section locations and exit checks.

### UX impact analysis

Reuse prior evidence only when recorded impact analysis proves implementation, dependencies,
assumptions, environment, and transitive effects unchanged.

---

## 11. API quality bar

For any Iteration shipping a network API (REST, gRPC, GraphQL, WebSocket, or other RPC surface), the SPEC MUST include API requirements meeting the quality bar below. If the iteration ships no external API (backend consumed only by its own UI, CLI-only tool, library with no network surface, etc.), the Human User MUST explicitly confirm the exclusion — recorded as "N/A" per the [core §1 required-coverage rule](../../core-twtty-methodology.md#interview-me).

**Guiding principles.** Every API is a contract with someone — a paying customer, an internal team, a future self. Contracts MUST be versioned, MUST have a documented breaking-change policy, and MUST be discoverable by their consumers. Silent breaking changes are the single biggest source of API-driven outages; the quality bar exists to make them impossible by construction.

**API mode.** Per the shared mode-selection mechanic ([§3.2](#32-spec)), the Spec Agent asks the Human User which API mode applies to this scope:

- **Delegated** — the AI Agent decides and discloses: it sets the API *contract obligations* at spec time and produces the API *design* at plan time (style, endpoints/resources, schemas, versioning implementation, the drafted OpenAPI / protobuf / GraphQL document), reviewing both with the Human User.
- **Interactive** — the AI Agent walks the Human User through the API dimensions and co-decides each choice — contract obligations at SPEC, design at PLAN.
- **N/A** — the iteration ships no external API; this satisfies the exclusion confirmation required above. The remainder of §11 does not apply for this iteration.

**Requirements vs. design — where each lives.** API splits across two stages, matching the methodology's SPEC = *what* / PLAN = *how* line (and consistent with the rule that interfaces are a PLAN concern):

- **API contract & requirements → SPEC (`spec.md` §15).** The style-agnostic obligations the API MUST satisfy: it MUST be versioned, publish a machine-readable contract, and carry a breaking-change policy, deprecation window, auth model, error contract, and backward-compatibility tests.
- **API design → PLAN (`plan.md` §2.7).** The solution that satisfies those obligations: the chosen API style, endpoint/resource design, schema shapes, versioning mechanism, and contract format/repository path — the concrete authoring of the contract. Existing consumer contracts and approved user-mandated choices remain constraints; do not require new implementation artifacts to exist at SPEC-EXIT.

**API contract & requirements (both modes; SPEC §15).** Regardless of mode, the following apply to every API-shipping iteration scope:

- **Versioning strategy** — Explicit version-identification and compatibility obligations, including how consumers are protected when versions change. A consumer-mandated interface remains a SPEC constraint; otherwise PLAN chooses the URI/header/media-type/schema mechanism.
- **Contract document** — At L2+, the API MUST publish a machine-readable contract in the repository under a stable path and regenerate or verify it in CI. SPEC states that obligation; PLAN selects and records its format/path and authors the contract, and EXECUTE implements the CI verification. Existing or user-mandated contract locations may be referenced in SPEC.
- **Breaking-change policy** — Explicit definition of what constitutes a breaking change and how breaking changes are introduced (major version bump, sunset header, deprecation notice).
- **Deprecation window** — Minimum notice period for breaking changes. At L3+, this MUST be no less than 6 months for external consumers unless a shorter window is explicitly approved by the Human User with rationale recorded in `Notes` on `spec/1b`.
- **Auth and authorization** — Authentication mechanism (OAuth 2.x, mTLS, API key, signed request, or documented alternative) and authorization model (RBAC, ABAC, capability tokens, or documented alternative). At L3+, per-consumer rate limits and quota enforcement MUST be declared.
- **Error contract** — Standard error shape (HTTP status codes + structured body, gRPC status + details, GraphQL error extensions, or documented alternative) applied uniformly across the API surface.
- **Backward-compatibility tests** — At L3+, at least one automated test per prior public version MUST run in CI and gate merges.

**API design (both modes; PLAN §2.7).** The design that satisfies the §15 obligations is produced in the plan:

- **API style** — Named style (REST, gRPC, GraphQL, WebSocket, or documented alternative) and rationale.
- **Interface design** — Endpoint/resource/operation design, request/response schemas, status semantics, and the concrete mechanism satisfying the §15 versioning obligations. Record the contract format and repository path in `plan.md §2.7` and author the contract there, honoring any existing or user-mandated SPEC constraints.

**Delegated-mode disclosure.** In Delegated mode the AI Agent MUST disclose every non-trivial API choice — the style chosen, the versioning strategy adopted, the auth mechanism selected, the deprecation window set — with brief rationale (contract-level choices in SPEC §15.8; design choices in PLAN §2.7).

**Canonical home.** API *contract & requirements* live in the spec's §15 API requirements and contract section ([templates/spec-template.md §15](templates/spec-template.md#15-api-requirements-and-contract)); API *design* lives in the plan's §2.7 API design section ([templates/plan-template.md §2.7](templates/plan-template.md#27-api-design)). SPEC-EXIT rule 15 enforces §15 non-emptiness and PLAN-EXIT rule 17 enforces §2.7 non-emptiness when API mode ≠ `N/A`.

Rationale: professional API design is a deliberate practice, not a byproduct of implementation. This bar exists to prevent the common failure modes where an API ships without a stable contract, without an explicit versioning story, or without a documented deprecation policy — leaving both producer and consumer teams to reverse-engineer the contract from the running code.
