# Risk calibration — agentic evaluation overlay

**Category:** `risk-calibration-delta` · The `sdlc-for-agentic-apps` **overlay** that adds
agentic-evaluation rows **on top of** the baseline
[`risk-calibration/default.md`](../../../sdlc/config/risk-calibration/default.md) ladder. The
confirmed level (assessed at SEED, recorded in `meta/risk-level`) selects the **column**; all
baseline matrix rows continue to apply. These are **minimum** controls per level — a project
MAY raise them, never relax them.

**Legend:** **MUST** = required · **—** = not required at this level · a numeric cell is the
threshold for that level.

This overlay is this implementation's per-level calibration of the **Measured or sampled
assessment** requirement in [core §3.3](../../../../core-twtty-methodology.md#33-determinism-repeatability-and-continuity):
*how many* runs or samples are taken, *how* differences between them are reported, and *what*
result counts as a pass. It forbids treating a single stochastic-eval run as proof of
repeatability.

## Agentic evaluation controls

At L1, follow the baseline [smoke-only verification contract](../../../sdlc/config/risk-calibration/default.md#level-1-verification).
Formal evaluations require explicit Human selection or a stricter applicable policy.
If selected, their harness, declared pass rule, baseline/reproducibility and scoring
evidence are required; the L1 minimum below applies. A basic live happy-path smoke is
an observation, not a scored quality/stability claim, and requires no separate N=1
acknowledgment, dataset or evaluation report.

| Requirement | L1 | L2 | L3 | L4 | L5 |
|-------------|:--:|:--:|:--:|:--:|:--:|
| Evaluation harness present | — | MUST | MUST | MUST | MUST |
| Production-representative eval coverage | — | MUST | MUST | MUST | MUST |
| Stochastic-dimension run count N (minimum; L1 only for selected formal evals) | 1 | 3 | 3 | 5 | 5 |
| Declared pass rule (default K-of-N) | — | MUST | MUST | MUST | MUST |
| Variance measure (standard deviation or confidence interval) reported with the aggregate | — | — | — | MUST | MUST |

**Per-level notes.**

- **L1 single-sample acknowledgment (selected formal evaluations only).** A run count of `N = 1` is permitted only if the Human
  User explicitly acknowledges that the resulting score is a **single sample, not a
  statistically stable measurement**, recorded in the `meta/risk-level` entry's `Notes`
  (see the baseline [Level 1 rules](../../../sdlc/config/risk-calibration/default.md#level-1-rules)).
  Absent that acknowledgment, the AI Agent MUST `Escalate` (core §3.2). The selected L1
  dataset may be small; do not claim statistical stability from a single sample. This
  single-sample acknowledgment is **separate from, and additional to**, the baseline L1
  prototype acknowledgment: an L1 agentic project with selected formal stochastic eval dimensions
  MUST record **both** in the `meta/risk-level` entry's `Notes` — the one confirmed level
  selects the L1 column of **both** this overlay and the baseline ladder.
- **L4–L5 pass rule.** A **CI-margin** pass rule MAY be used instead of K-of-N at the
  project's discretion.

## Overlay application rule

Mirrors the baseline [Matrix application rule](../../../sdlc/config/risk-calibration/default.md#matrix-application-rule).
Before requesting any gate that attests agentic quality, the AI Agent MUST consult this
overlay for the confirmed level and apply every row marked `MUST` to the **gate-time
evaluation evidence**. The run-count, pass-rule, and variance rows bind the **gate-time**
evidence only; intermediate development iterations MAY use a single fast run for feedback and
are exempt. The specialization spec names which gate and which evaluation stage task carry the
attestation.
