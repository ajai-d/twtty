# <REPLACE: Your Specialization> Specialized Implementation

<!--
========================================================================
  Specialized Implementation Template for Promptless Agentic SDLC
                              (TWTTY)
========================================================================

  Copy this file to:
    framework/methodology/specialized-implementations/<your-specialization>/
      <your-specialization>.md

  Then fill in every <REPLACE: ...> placeholder and delete every
  <!-- HELP: ... --> comment. Anything left in <REPLACE: ...> or
  <!-- HELP: ... --> at PR time will be flagged by the reviewer.

  Structure follows the shipped implementations. There are two valid
  shapes:

    - STANDALONE specialization (full pipeline) — like `sdlc.md`. Sections:
      1 Purpose and Goals, 2 Pipeline summary, 3 Stage & stage-task details,
      4 Artifact locations, 5 Specialization activation, a risk calibration and
      enforcement profile (required, per core §3.1), then any optional
      sections your specialization needs (Runtime, Guardrails, rules, quality
      bars).

    - EXTENSION specialization (deltas on a parent) — like
      `sdlc-for-agentic-apps.md` and `dataeng.md`. These inherit a
      parent's pipeline and present: 1 Purpose and Goals, 2 Specialization activation,
      3 Stage & gate deltas, 4 Artifact locations, then Runtime/roles,
      Risk enforcement delta, and specialization rules. An extension MAY omit the
      standalone Pipeline summary (it inherits the parent's) and MAY place
      Specialization activation early as §2.

    Whichever shape you use, the REQUIRED elements are the same: Purpose and Goals,
    the stage/task (or delta) definitions, Artifact locations, Specialization
    activation (with an explicit Specialization field value and a mismatch check),
    a risk calibration scale (per core §3.1 — standalone specializations define
    one; extensions inherit their parent's), and the core-mandated
    evidence and native verification described in §5 below.
    Cross-reference the shipped files while filling this in — they are your
    working examples.

  You MAY add sections beyond the required ones below (e.g., "6.
  Guardrails profile", "7. Risk enforcement profile"). You MUST NOT
  weaken the core specification. See CONTRIBUTING.md §1.1.
========================================================================
-->

> This document extends the [Core TWTTY Specification](../../core-twtty-methodology.md). It MUST NOT weaken the core's approval rules, stage order, or traceability requirements (see [core — Core TWTTY Specification vs. Specialization](../../core-twtty-methodology.md#core-twtty-specification-vs-specialization)).
>
> <!-- HELP: If your implementation extends another specialized implementation (e.g., extends the baseline `sdlc`), replace the paragraph above with one that also names the parent implementation. See `sdlc-for-agentic-apps.md` for the pattern. -->
>
> Copyright © <REPLACE: year> <REPLACE: your name>. Licensed under
> [Apache License 2.0](../../../../LICENSE) — see
> [NOTICE](../../../../NOTICE). Suggested citation: <REPLACE: your surname>, <REPLACE: initial>. (<REPLACE: year>).
> *TWTTY: <REPLACE: Your Specialization> Specialized Implementation.*
> https://github.com/ajai-d/twtty.

## In this document

<!-- HELP: Auto-generated table of contents. Update the section list if you add optional sections beyond the required ones. -->

| Section | Purpose |
|---------|---------|
| [1. Purpose and Goals](#1-purpose-and-goals) | What this implementation is, its intended outcomes, and how it maps to the core stages |
| [2. Pipeline summary](#2-pipeline-summary) | Visual summary of the pipeline for this specialization |
| [3. Stage and stage task details](#3-stage-and-stage-task-details) | Stage tasks, agent roles, outputs, and stage exit gates |
| [4. Artifact locations](#4-artifact-locations) | Where each stage's artifacts are written |
| [5. Specialization activation](#5-specialization-activation) | How the Spec Agent knows this implementation is active (bootstrap-driven; mismatch check) |

---

## 1. Purpose and Goals

<REPLACE: One paragraph describing who this implementation is for, when to use it, and what problem it solves that the shipped implementations do not solve well. If it extends another implementation, state exactly what it inherits and what it strengthens.>

<!-- HELP: Examples:
  - "This implementation is for teams building batch and streaming data
    pipelines on a lakehouse platform. It extends the baseline `sdlc`
    with data-lineage and semantic-model artifacts, plus a data-quality
    gate at PLAN-EXIT."
  - "This implementation is for teams building embedded firmware for
    safety-critical medical devices. It supersedes the baseline `sdlc`
    EXECUTE decomposition with a safety-case workflow." -->

  ### Goals

  <REPLACE: List the intended outcomes of this specialized implementation, not an individual project's business goals. State only additions or refinements to inherited goals, following [core section 5.3](../../core-twtty-methodology.md#53-specialization-goals).>

---

## 2. Pipeline summary

This section is a visual summary of the pipeline. [Section 3 — Stage and stage task details](#3-stage-and-stage-task-details) is authoritative for execution order, stage tasks, and stage exit gates.

<!-- HELP: You may use an ASCII diagram (like sdlc.md §2) or a Mermaid flowchart. The diagram MUST show all four stages (SEED, SPEC, PLAN, EXECUTE), the sub-stages you define, the four stage-exit gates, the replay-execution log, and the feedback loop for subsequent iterations. -->

```text
                              TWTTY <REPLACE: Your Specialization> Pipeline

    SEED ─────▶ SPEC ─────▶ PLAN ─────▶ EXECUTE
   Intent    Requirements  Strategy    <REPLACE: your EXECUTE summary>

  +-----------+--------------------------+----------------------+--------------------------------------+
  |   SEED    |           SPEC           |         PLAN         |               EXECUTE                |
  +-----------+--------------------------+----------------------+--------------------------------------+
  | 0a Intent | 1a Discovery interview   | 2a Architecture      | <REPLACE: 3a ...>                    |
  |           | 1b Draft specification   | 2b Design            | <REPLACE: 3b ...>                    |
  |           |                          | 2c Orchestration     | <REPLACE: ... continue as needed>    |
  |           |                          |                      | <REPLACE: 3m Iteration>              |
  +-----------+--------------------------+----------------------+--------------------------------------+
  | seed/     | spec/spec.md             | plan/plan.md         | <REPLACE: your artifact layout>      |
  | seed.md   | spec/spec-<id>.md        | plan/plan-<id>.md    |                                      |
  | intent-   | ...                      | ...                  |                                      |
  |  <id>.md  |                          |                      |                                      |
  +-----------+--------------------------+----------------------+--------------------------------------+
  | replay-execution/ (appended throughout all stages; baseline log plus one log per iteration)          |
  |   execution-log.md   ·   Iteration-*-execution-log.md   ...     (baseline + per iteration)           |
  +----------------------------------------------------------------------------------------------------+
                                                                                  │
                              ◀──── Feedback loop ── next iteration ────────────────┘
```

Above, `spec.md`/`plan.md` are the **baseline buildout** (unnumbered), and `<id>` is a generated `Iteration-<YYYYMMDDTHHMMSSZ>-<token>` assigned to a **later** iteration (see [core §4.2/§4.3](../../core-twtty-methodology.md#43-on-new-iteration)).

Each stage is informed by the prior stage output. No stage begins until the prior stage's exit gate (`SEED-EXIT`, `SPEC-EXIT`, `PLAN-EXIT`, or `EXECUTE-EXIT`) is approved.

---

## 3. Stage and stage task details

### Default agent as orchestrator

<REPLACE: One paragraph — state whether you use the default agent as orchestrator (recommended) or define your own custom agent role for orchestration. See sdlc.md §3 for the standard wording.>

### 3.1 Seed

<!-- HELP: You typically inherit the Seed stage from the baseline SDLC unchanged. State that explicitly, or describe any differences. -->

<REPLACE: Either "The Seed stage is inherited from the baseline SDLC — see [sdlc.md §3.1](../sdlc/sdlc.md#31-seed)" or a full definition of your Seed stage.>

### 3.2 Spec

| Stage task | Agent | Protocol | Output |
|-----------|-------|----------|--------|
| 1a. Discovery interview | Spec Agent | Discovery | <REPLACE: what your Discovery elicits> |
| 1b. Draft specification | Spec Agent | TWTTY loop | Draft spec.md §1-§8 and <REPLACE: any specialized sections required> in one coherent pass. Baselines use the complete required shape; later Iterations include only intent-relevant sections and fields. The AI MAY chunk drafting only when the content is too large for one pass. |

**Stage exit gate (`SPEC-EXIT`).** All applicable conditions MUST hold; the AI Agent MUST verify mechanical conditions before requesting approval. Baselines use the full required template; later Iterations include only content needed for the approved intent. Retain required metadata, discovery/approval records, acceptance coverage for new or changed requirements, and applicable risk/security/data controls. Unchanged approved requirements carry forward without restatement or N/A filler; omission does not remove them.

1. <REPLACE: A mechanically checkable condition — e.g., "spec.md exists at the canonical path.">
2. <REPLACE: Another mechanically checkable condition — e.g., "spec.md passes the applicable checks in the spec template's SPEC-EXIT validation checklist.">
3. Human User approval outcome on `spec/1b` is `Approved` or `Approved with changes`.

<!-- HELP: You may add specialized conditions here. Every condition must be either mechanically checkable OR the single human-approval condition. -->

### 3.3 Plan

| Stage task | Agent | Output |
|-----------|-------|--------|
| 2a. Architecture | Architecture Agent | <REPLACE: what fills plan.md §1> |
| 2b. Design | Design Agent | <REPLACE: what fills plan.md §2> |
| 2c. Orchestration | Planning Agent | <REPLACE: what fills plan.md §3> |

**Stage exit gate (`PLAN-EXIT`).** Baselines use the complete required plan. Later Iterations write affected design and current work/dependencies, referencing valid unchanged approved plans. Preserve metadata, approval records, work-item traces/footprints/DAG, execution controls, and applicable risk/safety obligations; missing copied content alone is not a failure.

1. <REPLACE: mechanical condition>
2. <REPLACE: mechanical condition>
3. Human User approval outcome on `plan/2c` is `Approved` or `Approved with changes`.

### 3.4 Execute

| Stage task | Agent | Protocol | Output | Frequency |
|-----------|-------|----------|--------|-----------|
| 3a. Setup | <REPLACE: Setup Agent> | TWTTY loop | <REPLACE: repository initialization, toolchain> | once per iteration |
| <REPLACE: 3b. ...> | <REPLACE: agent> | TWTTY loop | <REPLACE: output> | <REPLACE: per W-⟨n⟩ or per iteration> |
| <REPLACE: 3c. ...> | <REPLACE: agent> | TWTTY loop | <REPLACE: output> | <REPLACE: frequency> |
| <!-- HELP: Add as many rows as your specialization requires. Each row is one sub-stage. sdlc.md has 3a–3m; sdlc-for-agentic-apps.md adds no sub-stages but strengthens the existing ones. --> | | | | |
| 3m. Iteration | Human + Agents | TWTTY loop | Feedback capture and iteration closeout. This stage task's approval triggers `EXECUTE-EXIT`. | once per iteration |

**Work-item lifecycle.** <REPLACE: define the applicable task order and evidence. SDLC extensions reference the bound [development procedure](../sdlc/config/development/default.md#developer-workstation-inner-loop) and SDLC execution contracts rather than copying them. Standalone implementations define their own applicable EXECUTE tasks without weakening core stages or approvals.>

**Stage exit gate (`EXECUTE-EXIT`).** All conditions MUST hold; the AI Agent MUST verify mechanical conditions before requesting approval:

1. Every planned work item has an approved applicable implementation/native-operation entry, or a resolved `Abandon`/`Escalate`; define the task IDs for this implementation.
2. Every current/affected inherited AC has actual passing evidence from its applicable app test or native operation, mapped in existing execution evidence; do not invent validation wrappers for infrastructure-only outcomes.
3. <REPLACE: any specialized conditions>
4. Human User approval outcome on `execute/3m` is `Approved` or `Approved with changes`.

---

## 4. Artifact locations

<!-- HELP: State exactly where each stage-task's artifacts live in the project tree. Use the shipped implementations as your reference. -->

| Stage task | Artifact location |
|-----------|-------------------|
| 0a Seed | `seed/seed.md` (project seed; baseline buildout) + `seed/intent-<iteration-id>.md` (Iteration Intent, per later iteration) |
| 1b Spec | `spec/spec-<iteration-id>.md` (every iteration; `<iteration-id>` = the iteration's `Iteration-<YYYYMMDDTHHMMSSZ>-<token>`) |
| 2a–2c Plan | `plan/plan-<iteration-id>.md` (every iteration) |
| 3a Setup | <REPLACE: repository initialization paths> |
| 3b Implement | <REPLACE: source tree — e.g., `src/`, `pipelines/`, `firmware/`> |
| <REPLACE: your sub-stages> | <REPLACE: paths> |
| 3m Iteration | `—` (iteration is a closeout event; recorded via the replay-log entry) |
| All stages of an iteration | `replay-execution/<iteration-id>-execution-log.md` (append-only within the iteration) |

<!-- HELP: Domain structure. The spec/plan locations above show the single-domain shape (one spec-<iteration-id>.md, one plan-<iteration-id>.md). If your specialization builds systems with more than one area of responsibility, an iteration MAY use the hub-and-spoke split by domain (an overview plus spec/domains/<domain>-<iteration-id>.md and plan/domains/<domain>-<iteration-id>.md) per the baseline sdlc §8.2 domain model, which every implementation extending sdlc inherits. Do not restate that model here; reference it and note any specialization-specific footprint conventions (e.g., pipelines/<domain>/** instead of src/<domain>/**). -->

---

## 5. Specialization activation

**Activation.** This specialization is activated by `twtty start project type=<REPLACE: specialization slug> …` (see the [TWTTY command dispatcher](../../../twtty.md)); `type=<slug>` resolves to this document at `methodology/specialized-implementations/<slug>/<slug>.md`. No Discovery-time routing question is asked; the Spec Agent captures the selected specialization during Discovery (`spec/1a`) and records it in the spec's `## Metadata` `Specialization` field during drafting (`spec/1b`).

<!-- HELP: New implementations do not use routing questions. Specialization is selected by the start command's type= parameter. To ship a new implementation: add its slug to the dispatcher's type list (framework/twtty.md), add a type= row to the README project-type table, and ensure type=<slug> resolves to your methodology/specialized-implementations/<slug>/<slug>.md. -->

**Specialization field value.** State the exact string the Spec Agent MUST record in the `## Metadata` `Specialization` field for this implementation:

> `<REPLACE: exact Specialization field value, e.g., dataeng>`

**Mismatch check (safety net).** Before beginning Round 1, the Spec Agent MUST scan the seed for signals that clearly indicate a different specialization than the bootstrap selected. If mismatch is detected, the Spec Agent MUST surface it and require the Human User to `Abandon` this session and re-bootstrap with the correct prompt.

<REPLACE: Optional — one sentence describing seed signals that clearly identify this specialization vs. others. E.g., "If the seed mentions ingest / transform / serve or names a data warehouse, this is likely a dataeng iteration.">

### Evidence and verification (required by core §2 and §3.3)

Define how this implementation meets the core evidence requirements using native/
existing tooling and direct artifact review, not generated methodology validators:

1. **Append-only history.** <REPLACE: native version-control/history and review mechanism; append corrections without rewriting originals.>
2. **Private evidence.** <REPLACE: existing scanners and context-aware review before persistence; actual coverage/limitations, with no raw secret/identifier findings.>
3. **Implementation proof.** <REPLACE: native application tests/CI, provider results and required reviews; inspect actual methodology artifacts without inventing log/schema/gate-check scripts.>

<!-- HELP: Inherit core §2 and applicable existing organization/regulatory controls.
     Do not introduce a custom validator or methodology-only workflow as a default. -->

---

<!-- HELP: §6 Guardrails profile below is OPTIONAL — keep it if your specialization needs it, delete it if not. §7 Risk calibration and enforcement profile is REQUIRED by core §3.1 (a standalone specialization defines the scale; an extension inherits it from its parent). -->

## 6. Guardrails profile

<REPLACE: Optional — list any hard guardrails your specialization requires that go beyond the core guardrails (billable cloud operations, destructive git, refine deadlocks). Example: "No unreviewed medical-record schema change may pass PLAN-EXIT.">

## 7. Risk calibration and enforcement profile

Core [§3.1](../../core-twtty-methodology.md#31-risk-calibration) requires every specialization to have a calibration scale, so this section is REQUIRED — though an extension MAY satisfy it by inheriting its parent's scale.

<REPLACE: For a STANDALONE specialization — define the calibration scale: an ordered set of levels (or an equivalent rubric) in which higher positions denote higher stakes and stricter enforcement, the enforcement profile per level (which stage tasks and gates apply, and how strictly), and optionally a floor level that removes controls. Follow the pattern in sdlc.md §7 (its 1–5 ladder plus the enforcement table). For an EXTENSION specialization — state that the scale is inherited from the parent (for example, "inherits the baseline sdlc 1–5 ladder; see sdlc.md §7") and define only the per-level deltas your specialization adds, as sdlc-for-agentic-apps.md §6 does.>

---

<!-- HELP: Delete every line that still contains <REPLACE: ...> or <!-- HELP: ... --> before opening your PR. -->
