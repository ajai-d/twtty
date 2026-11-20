# SDLC for Agentic Apps Specialized Implementation

> This document extends the baseline SDLC implementation at [../sdlc/sdlc.md](../sdlc/sdlc.md). Everything in the baseline SDLC applies unless this document adds stricter requirements.
>
> This extension is for projects with LLM-driven behavior that cannot be fully validated by deterministic unit/integration tests alone.
>
> Copyright © 2026 Ajai Peddapanga. Licensed under
> [Apache License 2.0](../../../../LICENSE) — see
> [NOTICE](../../../../NOTICE). Suggested citation: Peddapanga, A. (2026).
> *TWTTY: SDLC for Agentic Apps.*
> https://github.com/ajai-d/twtty.

## In this document

| Section | Purpose |
|---------|---------|
| [1. Purpose](#1-purpose) | Scope of the extension for agentic apps |
| [2. Specialization activation](#2-specialization-activation) | How the Spec Agent knows this implementation is active (bootstrap-driven; mismatch check) |
| [3. Stage and gate deltas](#3-stage-and-gate-deltas) | Additions to SPEC, PLAN, and EXECUTE |
| [4. Artifact locations](#4-artifact-locations) | Where agentic artifacts live |
| [5. Runtime and roles](#5-runtime-and-roles) | Role decisions for evaluation work |
| [6. Risk enforcement profile delta](#6-risk-enforcement-profile-delta) | Agentic evaluation requirements by risk level |
| [7. Agentic-specific rules](#7-agentic-specific-rules) | Additional executable constraints |

---

## 1. Purpose

This document adds executable requirements needed for AI-agent application delivery: tool contracts, quality evaluation (including explicit statistical treatment of non-deterministic outputs), cost controls, and safety policy. It does not replace baseline SDLC; it tightens it for non-deterministic behavior.

---

## 2. Specialization activation

This specialization is activated by `twtty start project type=sdlc-for-agentic-apps …` (see the [TWTTY command dispatcher](../../../twtty.md) and [README quick start](../../../../README.md#quick-start)), which resolves `type=sdlc-for-agentic-apps` to this document. No Discovery-time routing question is asked; the Spec Agent captures the selected specialization during Discovery (`spec/1a`) and records `Specialization: sdlc-for-agentic-apps` in the spec's `## Metadata` block during drafting (`spec/1b`).

**Specialization field value.** The Spec Agent MUST record exactly the following string in the spec's `## Metadata` `Specialization` field for this implementation:

> `sdlc-for-agentic-apps`

**Mismatch check (safety net).** Before beginning Round 1, the Spec Agent MUST verify that the seed content aligns with LLM-driven behavior. If the seed clearly describes a project without LLM behavior (for example, a plain CRUD API or a data pipeline), the Spec Agent MUST surface the mismatch to the Human User, propose switching to the correct specialization, and require the Human User to `Abandon` this session and re-bootstrap with the correct prompt before proceeding. See [baseline SDLC §3.2](../sdlc/sdlc.md#32-spec) for the full mismatch-check rule.

---

## 3. Stage and gate deltas

### 3.1 Spec delta (`spec/1b`)

For the baseline buildout, compose the complete spec using strict inheritance as below. Later Iterations use the baseline template's intent-focused applicability rule: include only affected baseline/addendum sections and fields, carry forward unchanged approved requirements, and retain metadata, acceptance coverage, and applicable evaluation/safety controls.

1. Start from the baseline template [../sdlc/templates/spec-template.md](../sdlc/templates/spec-template.md) and complete the `## Metadata` block plus Sections 1-8. In the `## Metadata` block, record `Specialization: sdlc-for-agentic-apps`.
2. Insert Sections 9-12 from [templates/spec-for-agentic-apps-template.md](templates/spec-for-agentic-apps-template.md) between §8 and §13.
3. Complete the baseline `## 13. UX requirements` (conditional per UX mode), `## 14. Data classification` (always required), and `## 15. API requirements and contract` (conditional per API mode) from the baseline template.

> Steps 1–2 describe the single-domain shape. For a **multi-domain** (hub-and-spoke) iteration the overview `spec-<iteration-id>.md` carries no §6–8 (each domain's §5–8 live in `spec/domains/<domain>-<iteration-id>.md`) and §9–12 live in the overview alongside §1–§4 and §13–§15, per the spec addendum's hub-and-spoke note and [sdlc.md §8.2](../sdlc/sdlc.md#82-domain-based-separation-of-responsibilities).

The agentic baseline spec adds four required sections between §8 and §13; later Iterations include the content affected by their intent:

- Section 9: Tool schemas
- Section 10: Evaluation rubric and baseline
- Section 11: Cost budget
- Section 12: Safety policy

Section 11 (Cost budget) declares the built app's runtime cost budget from the bound [`tokenomics/product`](config/tokenomics/product/product-profile1.md) profile. A project records its approved ceilings or `none` and applicable degradation policy here. Affected LLM work records measured tokens/cost even when uncapped; only approved non-`none` caps require budget enforcement and forced-cap tests under EXECUTE-EXIT condition 8. Production spend is enforced by the app, not by TWTTY running continuously.

`SPEC-EXIT` for projects using this extension is satisfied only if all applicable baseline and addendum checks pass. Baseline specs satisfy the full required shape; iteration specs are checked against the approved intent and any inherited content they rely on, not required to repopulate every section.

### 3.2 Plan delta (`plan/2a`-`plan/2c`)

**Verification applicability.** The baseline [L1 smoke-only contract](../sdlc/config/risk-calibration/default.md#level-1-verification)
applies to AI apps too. Formal evaluation/harness, eval-first dependencies, scored
datasets, baseline/stability protocols and executable safety-test suites are required
at L2+ or when explicitly Human-selected/required by policy, not automatically at L1.
Required safe behavior and runtime guards remain mandatory. L1's basic normal-app
smoke uses the actual approved model and records observed behavior without a statistical
quality claim; it is not permission to substitute a mock.

**Inherited requirements (PLAN and EXECUTE).** Determine the active specialization from spec metadata, not the presence of Section 10. Apply evaluation, cost, and safety requirements from the current spec together with unchanged requirements carried forward from approved specs. Reference the approved sources in existing gate evidence; omitted delta sections do not waive their thresholds, run-count rules, budgets, or safety obligations. Unresolved applicable requirements MUST block the gate. Reuse unchanged approved plans and evaluation assets when still applicable; do not recreate a harness merely because its requirements are inherited. Changed behavior still requires the applicable evaluations and current evidence, not an old passing result.

Baselines compose the complete required plan below. Later Iterations use the baseline plan's applicability rule, writing affected design and current work/dependencies while referencing valid unchanged approved content:

1. Start from the baseline template [../sdlc/templates/plan-template.md](../sdlc/templates/plan-template.md).
2. Apply orchestration constraints from [templates/plan-for-agentic-apps-template.md](templates/plan-for-agentic-apps-template.md).

When formal evaluations apply, agentic planning adds eval-harness-first orchestration:

- Eval harness work items MUST use ID pattern `W-<n>-eval`.
- At least one `W-<n>-eval` item MUST be sequenced before any current `W-<m>` item that introduces or modifies LLM-driven behavior. It may verify/reuse an existing evaluation harness rather than recreate it. An iteration with no affected LLM behavior need not invent eval work or dependency edges; applicable inherited controls remain enforced.
- Apply the bound [development procedure](../sdlc/config/development/default.md#developer-workstation-inner-loop)
  to preparation. Bootstrap dependency setup and model/resource provisioning are not
  LLM application-behavior implementation and have no eval-harness prerequisite.
  Eval-first edges apply to affected LLM behavior, not to that preparation.

**Agentic technology and framework selection.** Extending the baseline [Technology currency and framework preferences](../sdlc/sdlc.md#33-plan) step, during Architecture (2a) the Architecture Agent MUST start from the project's bound **`agentic-stack`** profile (initial default: [`config/agentic-stack/default.md`](config/agentic-stack/default.md); the concrete model choice lives in that profile, not this methodology) and additionally research and propose the current, applicable **agentic** technologies — agent frameworks and SDKs, model choices and providers, orchestration and multi-agent patterns, the tool/MCP integration ecosystem, evaluation/tracing/observability tooling, guardrail and safety tooling, and reusable skills — looked up at plan time (treated as untrusted input per [core §4.5](../../core-twtty-methodology.md#45-rules), and reconciled against the bound `agentic-stack` default), and MUST explicitly ask the Human User for their **preferred agentic framework(s)** before committing `plan.md` §1.5. The resolved stack — the bound default as confirmed or overridden — the proposal, and the elicited preferences are recorded in §1.5 per the baseline currency rule. Existing projects retain adopted model choices until an approved update; do not silently repin from newer library defaults. The `agentic-stack` binding governs **what** framework/platform/model are used; the [`cloud`](../sdlc/config/cloud/) binding governs provisioning and context-appropriate authentication: developer Entra locally, Managed Identity when hosted, and no service keys.

The baseline's covering-Autopilot preference rule applies here: reuse actual Human
preferences and research/disclose remaining in-scope choices, not a fictional Human
answer or an additional routine confirmation. Do not silently substitute pinned choices
or bypass an actual scope/policy/native permission boundary.

`PLAN-EXIT` for projects using this extension is satisfied only if all applicable baseline and addendum checks pass, using the current work scope and valid inherited approved requirements/designs.

Baseline environment ownership/placement and local/hosted identity rules apply to model
dependencies too. A newly owned model for local development belongs to the local
environment; an existing authorized service is referenced without takeover. The bound
provider governs provisioning/authentication, not implicit hosting. Shared agent and
evaluation code remains outside environment IaC; UI/prototype requirements are unchanged.

### 3.3 Execute delta (`execute/3a`-`execute/3m`)

Baseline execute stage tasks and ordering remain unchanged.

**Evaluation and safety readiness (`3f`).** When formal verification applies under §3.2, EXECUTE MUST provide working evaluation/safety assets and record their actual locations/invocations. Establish required baselines and capture dataset, model/configuration, sample-count, timestamp and supported-seed evidence under core redaction rules. Reuse an existing baseline only while its inputs/applicability remain valid. Required safety fixtures MUST run and pass; unexecuted commands are not evidence. At L1 smoke-only, use existing app/verification evidence instead of inventing harnesses, datasets or safety-test suites; required safety policy and runtime guards still apply.

`EXECUTE-EXIT` is extended with two additional mandatory conditions:

7. For affected LLM behavior, `execute/3f/W-<n>` MUST record the applicable current verification. L1 smoke-only records its declared normal-app journey, actual live-model response and observed result, not invented scores or an eval report. When formal evaluations apply, record scores satisfying every current/affected inherited dimension, comparator, threshold and stability class, with report/source references and required baseline/reproducibility/safety evidence. Stochastic results MUST satisfy the declared N/pass rule and required variance under §6; only the narrowly approved L1 single-sample exception permits N=1 final formal evidence. Fast intermediate feedback is not a substitute for required gate evidence; failed targets do not authorize lowering them.
8. For affected LLM behavior, record the approved runtime budget and applicable usage/outcome evidence under the [product budget profile](config/tokenomics/product/product-profile1.md#how-it-is-enforced). Formal verification includes eval-measured tokens/per-request cost and machine-readable usage. L1 smoke-only records actual provided usage and explicitly unavailable cost measurements in existing evidence, not a mandatory eval artifact or invented zero. Approved caps/degradation and independent safety/rate/policy controls remain enforced. Required cap verification must pass; all-`none` caps make enforcement/forced-cap tests inapplicable, not unrun passing tests.

All eight conditions (baseline 1-6 plus conditions 7-8 above) MUST hold before requesting `EXECUTE-EXIT` approval.

---

## 4. Artifact locations

When formal evaluations/tests apply, use these locations in addition to baseline SDLC artifacts:

- Evaluation datasets and fixtures: `tests/eval/data/`
- Evaluation harness code: `tests/eval/`
- Evaluation run outputs (machine-readable): `reports/eval/`
- Prompt/policy fixtures for safety tests: `tests/safety/`

Concrete dataset, evaluation-output, usage-evidence, and safety-fixture paths are selected and recorded during PLAN/EXECUTE, using the defaults above unless alternatives are justified. EXECUTE records the implemented locations and invocations with the test evidence. Existing or user-mandated locations declared in SPEC remain binding; SPEC need not invent new executable commands or generated paths.

---

## 5. Runtime and roles

No new mandatory agent role is introduced.

- The baseline `Test Agent` remains the owner of evaluation execution under stage task `3f`.
- The default agent MAY configure a dedicated eval-focused custom agent, but this is optional and does not change stage-task ownership.

This resolves the role question: evaluation is a testing responsibility, not a separate required stage.

---

## 6. Risk enforcement profile delta

This section is this implementation's definition of the **Measured or sampled assessment**
requirement in [core §3.3](../../core-twtty-methodology.md#33-determinism-repeatability-and-continuity) — *how many* runs or samples are taken, *how* differences between them are reported, and *what* result counts as a pass — and it forbids treating a single run as proof of repeatability. The per-level **values** (eval coverage, stochastic run count `N`, variance measure, pass rule) are defined in the bound **`risk-calibration-delta`** overlay, [`risk-calibration/eval-delta.md`](config/risk-calibration/eval-delta.md), which adds these rows **on top of** the baseline [`risk-calibration`](../sdlc/config/risk-calibration/default.md) ladder; all baseline matrix rows continue to apply. The confirmed level (recorded in `meta/risk-level`) selects the column.

The run-count, pass-rule, and variance rows bind the evidence recorded **at gate time** — the final `execute/3f/W-<n>` entry — not intermediate development iterations, which MAY use a single fast run for feedback. A single-run score satisfies condition 7 only under the L1 exception below.

**L1 single-sample exception.** Only when the effective approved overlay permits L1 `N = 1`, the approved evaluation requirement declares `N = 1` and its pass rule, and the Human User has recorded both the L1 throwaway-prototype acknowledgment and the separate single-sample acknowledgment in `meta/risk-level`, may a passing single sample be gate evidence. Label it **single sample, not a statistically stable measurement**; it is never proof of repeatability. Missing acknowledgment blocks the exception. A stricter overlay or approved larger N still applies; do not reduce N, pass rules or quality thresholds after a failed run. Other levels require their declared multi-run evidence.

L1 smoke-only uses a direct observation under §3.2, not this formal-score exception.
For formal quality claims, a single stochastic run is a sample, not a stable measurement;
the applicable run count/pass rule scales with the cost of a false-positive gate pass.

---

## 7. Agentic-specific rules

1. Tool schemas are part of the specification contract and therefore MUST live in spec (Section 9), not only in plan.
2. Acceptance criteria MUST be observable/verifiable; vague quality adjectives require a quantified Section 10 dimension when formal quality is claimed. L1 smoke-only declares concrete journey outcomes, not an unselected scoring rubric.
3. Apply EXECUTE-EXIT condition 8 and the product budget profile for affected LLM behavior. Do not invent caps, formal evaluation work or forced-cap tests when inapplicable, or reduce independently approved safety/budget controls.
4. Safety policy in Section 12 MUST include prohibited input/output classes, PII handling, jailbreak handling, and escalation behavior.
5. Formal agentic-quality evidence MUST reference its evaluation report. L1 smoke-only records its actual observation in existing verification evidence, not a formal quality claim.
6. When formal stochastic dimensions apply, retain §6's approved N/pass rule/variance and narrow L1 exception; a fast development sample cannot replace required final evidence.
