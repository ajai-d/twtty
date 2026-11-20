# Product tokenomics — profile 1 (default: no caps)

**Category:** `tokenomics/product` · **Status:** default · `sdlc-for-agentic-apps` binding

## What this binds

The **product runtime** budget — what the built **agentic application** spends at runtime on
LLM/inference: **tokens and $** per request, per session, and per day, plus the degradation
behavior when a threshold is hit. This file is the reusable **schema and defaults**; a
project records its **confirmed ceilings** in its spec's cost-budget section, which is the
enforcement gate.

## Budget

| Scope | Token cap | $ cap |
|-------|:---------:|:-----:|
| Per request | `none` | `none` |
| Per session | `none` | `none` |
| Per day | `none` | `none` |

- **Degradation policy:** `none` — fallback when a cap is hit (smaller model, cached/refused response, …).

`none` = tracked but never enforced; set a ceiling to make it a hard gate.

## How it is enforced

TWTTY runs at build time; the app's live production spend is outside it. So the budget is
enforced in two complementary ways:

- **Per-request cost — formal build-time eval gate.** When formal verification applies,
  the project's evaluation run measures tokens/$
  per request on eval inputs whether caps are set or `none`. If the **measured** per-request
  cost exceeds an approved non-`none` cap, the AI Agent MUST `Escalate` before the EXECUTE
  stage-exit gate. Per-session / per-day caps are
  **design targets** projected from per-request cost × expected volume — not measurable at
  build.
- **Runtime caps + degradation — conditional app controls.** Where the approved budget
  sets non-`none` runtime caps, the built app MUST enforce the applicable caps and approved
  degradation policy. At L2+ or with selected formal tests, tests MUST force each applicable
  cap and prove its declared behavior; a missing/failing required test MUST `Escalate`.
  L1 smoke-only still verifies required guards through actual configuration/code/runtime
  evidence; do not claim an unrun cap test passed. Explicit policy-required checks remain.
  Do not invent a cap or degradation
  policy solely to make a forced-cap test applicable.
- **L1 smoke-only evidence.** Record actual model-provided usage and budget outcome in
  existing evidence, explicitly noting unavailable dollar measurements. No formal eval
  run or machine-readable eval artifact is required; never invent zero cost.
- **All caps `none`.** Formal verification still records measured usage and machine-readable
  evidence; L1 smoke-only uses the evidence above. Budget enforcement and forced-cap tests
  are not required by this profile.
  Record budget enforcement/degradation testing as not applicable because no cap is set,
  not as a passing test. Independently approved safety, rate, policy or compliance controls
  remain mandatory; an uncapped budget does not waive them.

For formal verification, the AI Agent records the measured per-request cost, budget outcome and
applicable degradation-test result or explicit no-cap non-applicability as the machine-readable **usage-evidence** artifact in the `W-<n>`
replay entry. The methodology **verifies** the budget at build; the **app enforces** it live.

## How the AI Agent uses this file

Under `sdlc-for-agentic-apps` this is the default product budget (all caps `none`). A project
sets its ceilings and degradation policy in its spec's cost-budget section.
