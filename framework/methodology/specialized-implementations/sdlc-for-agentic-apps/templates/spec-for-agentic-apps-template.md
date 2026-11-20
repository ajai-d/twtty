# Spec Addendum (For Agentic Apps)

> This file is a strict addendum to the baseline SDLC spec template at [../../sdlc/templates/spec-template.md](../../sdlc/templates/spec-template.md).
>
> **Baseline shape — do not duplicate baseline sections here.** The composed baseline spec MUST contain, in order: (1) the baseline `## Metadata` block plus `## 1.`–`## 8.` from the baseline template; (2) Sections 9–12 from this addendum inserted between §8 and §13; (3) the baseline `## 13. UX requirements` (conditional per UX mode), `## 14. Data classification` (always required), and `## 15. API requirements and contract` (conditional per API mode). The spec's metadata MUST record `Specialization: sdlc-for-agentic-apps`.
>
> **Iteration applicability.** Follow the baseline template's intent-focused rule. Include only affected requirements/fields for tools, evaluation, budgets, or safety; unchanged approved requirements carry forward without restatement or N/A filler. New or changed requirements need acceptance coverage. Required metadata and active evaluation/safety controls remain enforced; omission is not a waiver.
>
> **Multi-domain (hub-and-spoke) iteration.** In a multi-domain iteration the overview `spec-<iteration-id>.md` carries no §6–8 (each domain's use cases, FR, NFR, ACs live in `spec/domains/<domain>-<iteration-id>.md` per [sdlc.md §8.2](../../sdlc/sdlc.md#82-domain-based-separation-of-responsibilities)), so "between §8 and §13" does not apply to the overview. Sections 9–12 are whole-system addendum foundations and live in the **overview `spec-<iteration-id>.md`** alongside §1–§4 and §13–§15. A §9–12 concern that is specific to one domain (for example, a tool or eval dimension exercised only by that domain) MAY instead live in that domain's `spec/domains/<domain>-<iteration-id>.md`. A single-domain iteration keeps §9–12 inline between §8 and §13 as described above.
>
> All `[bracketed placeholders]` MUST be replaced. Section headings MUST be preserved verbatim for mechanical validation.

---

## 9. Tool schemas

[One H3 subsection per tool used by agentic runtime behavior. ID prefix: `T-<n>`.]

### 9.1 T-1: [tool name]

- **Purpose:** [what this tool is used for]
- **Input schema:** [fields and types]
- **Output schema:** [fields and types]
- **Side effects:** [writes, external calls, mutations]
- **Failure modes:** [timeouts, invalid input, auth failure, partial writes]
- **Authorization scope:** [identity, permissions, and data boundaries]
- **Timeout and retry policy:** [limits, retry conditions, and idempotency requirements]
- **Structured errors:** [error shape and caller-recoverable versus terminal failures]
- **Audit requirements:** [events, fields, and retention]
- **Human approval:** [whether approval is required before side effects]

## 10. Evaluation rubric and baseline

[At L1, default to the baseline smoke-only verification contract: state "Basic happy-path smoke; formal evaluations not selected" and describe the normal-app journey and observable pass condition using the real model. Omit the unused formal fields below unless the Human explicitly selected formal evals or stricter policy requires them. At L2+ and for selected formal evals, define the rubric/baseline below. Existing approved requirements carry forward; new executable assets/measurements are PLAN/EXECUTE outputs.]

- **Eval type:** [rubric-based | LLM-as-judge | golden dataset | hybrid]
- **Evaluation data requirements:** [coverage, representativeness, privacy constraints, and any existing or user-mandated dataset reference; generated dataset paths are selected during PLAN/EXECUTE]
- **Stability classes:** `deterministic` = exact-match or programmatic scoring against a golden dataset (bit-reproducible; a single run suffices). `stochastic` = LLM-as-judge, sampled generation, or human-graded (run-to-run variance is expected; MUST use the declared N-run pass rule at gate time, including only the narrowly approved [L1 single-sample exception](../sdlc-for-agentic-apps.md#6-risk-enforcement-profile-delta)). Every dimension below MUST declare exactly one class.
- **Scoring dimensions:**
  - **DIM-1 [name]:** [metric definition], stability class: [deterministic | stochastic], comparator: [>= | <= | range], threshold: [number + unit], aggregation: [method]. If stochastic: run count N = [integer, per [sdlc-for-agentic-apps.md §6](../sdlc-for-agentic-apps.md#6-risk-enforcement-profile-delta) risk-tiered minimum], pass rule: threshold holds in ≥ K of N runs (state K) [default] — a CI-margin rule (mean ± CI clears threshold with margin ≥ CI width) MAY be used instead at the project's discretion, variance measure: [standard deviation | confidence interval method; required at L4–L5 regardless of which pass rule is chosen].
  - **DIM-2 [name]:** [metric definition], stability class: [deterministic | stochastic], comparator: [>= | <= | range], threshold: [number + unit], aggregation: [method]. If stochastic: run count N = [integer], pass rule: [...], variance measure: [...].
- **Stability timing:** N-run stability treatment applies only to the evidence recorded at gate time (the final `execute/3f/W-<n>` entry before this work item's contribution to `EXECUTE-EXIT`); intermediate development iterations MAY use a single fast run for feedback and are not subject to the stability requirement.
- **Baseline approach/reference:** [how a baseline will be established for each dimension, or an applicable existing measured reference; new numeric baseline values are recorded during EXECUTE]
- **Reproducibility requirements:** [fields the run evidence must capture: dataset version, model/deployment identifier, runtime configuration, sample count, timestamp, and seed where supported; actual values are collected during EXECUTE]
- **Assessment protocol:** [assessment method, scoring/aggregation procedure, required evidence, and pass conditions; executable invocations and generated output locations are implementation details]

## 11. Cost budget

[This project's confirmed runtime cost ceilings, following the `tokenomics/product` binding's
schema. Enter a cap or `none` (track without enforcing).]

| Scope | Token cap | $ cap |
|-------|:---------:|:-----:|
| Per request | <REPLACE> | <REPLACE> |
| Per session | <REPLACE> | <REPLACE> |
| Per day | <REPLACE> | <REPLACE> |

- **Degradation policy:** <REPLACE: behavior when each approved cap is hit; `none` when all budgets are `none` and no independent approved control requires degradation>
- **Usage evidence:** <REPLACE: observed tokens/cost when provided, scope and outcome; explicitly identify unavailable measurements. L1 smoke-only uses existing evidence; formal verification requires machine-readable usage. Concrete paths are selected during PLAN/EXECUTE.>

## 12. Safety policy

[Defines safety controls and escalation behavior.]

- **Prohibited input classes:** [e.g., explicit harmful instructions, secrets exfiltration requests]
- **Prohibited output classes:** [e.g., disallowed content categories]
- **PII handling:** [detection, masking/redaction, retention]
- **Jailbreak handling:** [detect/respond/escalate policy]
- **Escalation path:** [when and how handoff to human occurs]
- **Safety verification requirements:** [required safe behavior/runtime guards and applicable evidence; formal fixtures/tests follow the level/explicit selection, not an automatic L1 suite]

---

## SPEC-EXIT validation checklist (addendum)

The AI Agent MUST pass the applicable baseline checks in [../../sdlc/templates/spec-template.md](../../sdlc/templates/spec-template.md) and applicable checks below. Baselines satisfy the full shape. For iterations, section/field presence checks concern only intent-relevant changes; verify inherited tools, requirements, and references against their approved artifacts when needed. An iteration with no tool/evaluation/budget/safety changes need not repeat those sections. All active risk-level evaluation and safety controls still apply.

1. Section 9 contains at least one `T-<n>` tool schema with all ten required sub-bullets.
2. Section 10 declares L1 smoke-only and its concrete live journey/pass condition, or the applicable formal evaluation scope. For formal evaluations, declare eval type, data requirements and at least one dimension with stability class, comparator, numeric threshold and aggregation.
3. Formal evaluations declare baseline/reference and reproducibility fields. Newly measured values/deployment metadata are EXECUTE evidence, not SPEC-EXIT prerequisites.
4. Every dimension classed `stochastic` in Section 10 declares a run count N at or above the selected overlay's minimum, an explicit pass rule, and a variance measure where required. Single-run final gate evidence is prohibited except under [§6's narrowly approved L1 single-sample exception](../sdlc-for-agentic-apps.md#6-risk-enforcement-profile-delta), with both required acknowledgments and no stricter approved N. Single fast development runs remain permitted but are not substitutes for required gate evidence.
5. Section 11 declares per-request, per-session, and per-day budgets.
6. Section 11 defines explicit degradation behavior for every approved non-`none` budget threshold. If all caps are `none`, explicitly record budget enforcement/forced-cap testing as not applicable; do not invent thresholds. Independently approved safety, rate, policy and compliance controls remain enforced.
7. Section 11 defines usage/outcome evidence appropriate to smoke-only or formal verification under the product budget profile; unavailable measurements are explicit, not invented.
8. Section 12 declares prohibited input classes, prohibited output classes, PII handling, jailbreak handling, escalation path, and safety verification requirements.
9. Every `T-<n>` in Section 9 is referenced by at least one FR or NFR.
10. Every scoring dimension in Section 10 is referenced by at least one AC in Section 8.
11. No AC contains prohibited unquantified agentic-quality adjectives `helpful`, `accurate`, `relevant`, `natural`, `human-like` (case-insensitive whole-word match) unless the AC also cites a dimension/threshold in Section 10.
12. Formal Section 10 evaluations declare the assessment protocol and machine-readable evidence. L1 smoke-only needs no eval dataset/harness/report. Executable invocations/paths are PLAN/EXECUTE details.
13. Section 12 identifies safe behavior, applicable scenarios/outcomes and evidence. Formal fixtures/tests are implemented and pass when required by level, policy or explicit selection; a file path alone is not evidence.
14. Section 12 escalation path defines the trigger condition and the destination role/team.
