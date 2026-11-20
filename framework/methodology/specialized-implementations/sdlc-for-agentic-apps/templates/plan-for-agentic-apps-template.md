# Plan Addendum (For Agentic Apps)

> This file is a strict addendum to the baseline SDLC plan template at [../../sdlc/templates/plan-template.md](../../sdlc/templates/plan-template.md).
>
> **Do not duplicate baseline sections 1-3 here.** Start from the baseline plan template, then apply the addendum constraints below.
>
> In a **multi-domain** (hub-and-spoke) iteration, the baseline sections these constraints reference are distributed per [sdlc.md §8.2](../../sdlc/sdlc.md#82-domain-based-separation-of-responsibilities): apply each constraint to whichever file holds that section — the overview `plan-<iteration-id>.md` for cross-cutting sections, or the relevant `plan/domains/<domain>-<iteration-id>.md`.

> **Iteration applicability.** Baselines use the full applicable plan. Iterations write changed design/current work and reference valid unchanged assets. Formal eval-first constraints below apply at L2+ or when explicitly Human-selected/required by policy; L1 smoke-only needs no eval item/harness. Classify LLM impact by behavior, not file type; inherited selected requirements remain binding. Unaffected harnesses and technology selections need not be recreated.

---

## 3. Orchestration delta

### 3.1 Work breakdown (additional constraints)

[When formal evaluations apply, their implementation/readiness items MUST use `W-<n>-eval`; reuse applicable harnesses. L1 smoke-only uses normal app verification, not an invented eval item. Non-eval features use `W-<n>`.]

Formal-evaluation example (omit for L1 smoke-only):

| ID | Title | Description | Traces to |
|----|-------|-------------|-----------|
| W-1-eval | [eval harness setup] | [description] | C-1, NFR-1 |
| W-2 | [feature work item] | [description] | C-2, FR-1 |

### 3.2 Sequencing and dependencies (additional constraints)

[When formal evaluations apply, record eval-first edges for affected LLM behavior under the [agentic planning rules](../sdlc-for-agentic-apps.md#32-plan-delta-plan2a-plan2c). L1 smoke-only has no eval-first edge. Preparation follows the bound development profile, not an eval-harness prerequisite.]

Formal-evaluation example (omit for L1 smoke-only):

- **W-2 depends on:** W-1-eval

---

## PLAN-EXIT validation checklist (addendum)

The AI Agent MUST pass the applicable baseline checks in [../../sdlc/templates/plan-template.md](../../sdlc/templates/plan-template.md) and checks below. Read applicable evaluation, cost, and safety requirements from the current spec and unchanged approved specs it builds on, following [the inheritance rule](../sdlc-for-agentic-apps.md#32-plan-delta-plan2a-plan2c). Reference those sources in existing gate evidence rather than requiring their sections to be restated. Unresolved applicable requirements block the gate. Existing evaluation assets may be reused when applicable; their presence does not replace evaluation of changed behavior.

1. Determine specialization from metadata and verification applicability from the confirmed level, policy and explicit selection. Formal affected LLM work has an implementation/readiness `W-<n>-eval`; L1 smoke-only does not.
2. When formal evaluations apply, every item introducing/modifying LLM behavior depends on an applicable `W-<n>-eval` item.
3. Record only those required eval-first edges; do not invent them for L1 smoke-only or work with no affected LLM behavior.
4. At least one current work item traces to each current or inherited approved evaluation dimension applicable to affected behavior, including implementation or verification with the existing dataset, scorer, and report output where unchanged. Unaffected dimensions do not require new implementation items merely to restate coverage.
5. New or changed agentic technology choices record the proposal and Human User preferences per [sdlc-for-agentic-apps.md §3.2](../sdlc-for-agentic-apps.md#32-plan-delta-plan2a-plan2c). Unchanged selections may reference their approved plan and effective project configuration after validating continued applicability; a new iteration alone does not require reselecting the stack.
