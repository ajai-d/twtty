# Build tokenomics — profile 1 (default: no caps)

**Category:** `tokenomics/build` · **Status:** default

## What this binds

The **build-time** budget — what the AI Agent itself spends while building the project
(agent **tokens**, **$**, and **wall-clock**), especially under **Autopilot**. This is the
cost of *building* — not the runtime cost of a shipped LLM product.

## Budget

| Dimension | Default | Example cap |
|-----------|:-------:|-------------|
| Agent tokens (cumulative / iteration) | `none` | `5_000_000` |
| $ (cumulative / iteration) | `none` | `50` |
| Wall-clock (elapsed build time) | `none` | `4h` |

`none` = tracked but never enforced; set a cap to make it a hard ceiling.

## Advisory performance thresholds

Projects MAY configure context-size and routine-turn latency warnings independently of
hard token, cost, and wall-clock caps. Record selected advisory thresholds in the
project's `runtimeconfig.md`; they are not hard caps.

| Advisory signal | Suggested initial evaluation threshold |
|-----------------|----------------------------------------|
| Input-context size for one model request | `100_000` tokens |
| Model-processing time for a routine turn, excluding tool or approval waits | `2m` |

These are tuning starting points, not guaranteed performance limits or enabled hard
ceilings. Use a signal only where the harness exposes the corresponding measurement.
Unavailable advisory measurements MUST be marked unavailable, not inferred as exact;
their absence does not itself require escalation.

Crossing an advisory threshold SHOULD prompt profile adjustment within the Human User's
approved model policy or context rollover at the next safe boundary, following core
§4.5. It MUST NOT by itself trigger escalation, skipped verification, or interruption of
an in-flight operation. Hard-cap behavior remains unchanged.

## Mechanism

- **Capture.** Where the bound harness exposes per-run usage, the AI Agent accumulates the
  running total in `state.md` (alongside the sequence watermark). **Wall-clock is always
  measurable; tokens and $ only if the harness reports them.**
- **Timing attribution.** Existing budget checkpoints SHOULD distinguish model-processing
  time, local tool execution, CI/cloud execution, human-approval waiting, and paused time
  where measurements are available. Reports MUST distinguish elapsed time from active
  execution and MUST NOT double-count concurrent or nested operations, such as a local
  watcher waiting for a CI run. Unavailable measurements MUST be marked unavailable
  rather than inferred as exact. Timing summaries SHOULD reuse existing `meta/budget`
  entries and `state.md` budget fields, not introduce a separate documentation cycle.
- **Record.** Material build-cost checkpoints are recorded as `meta/budget` replay-log
  entries (e.g. at each gate or Autopilot burst).
- **Enforce.** If a tracked dimension would exceed its non-`none` cap, the AI Agent MUST
  `Escalate` (core §3.2) before continuing (this reuses the Autopilot cost guardrail);
  This applies in both Interactive and Autopilot modes: do not defer an overage to the
  next gate. **If the harness cannot report a
  capped dimension, that cap is best-effort — the AI Agent MUST `Escalate` the inability to
  enforce (Contract-or-Escalate) rather than silently ignore it.**

## How the AI Agent uses this file

Loaded at SEED (defaults) and confirmed in Discovery. With all caps `none`, cost is tracked
(best-effort) but never blocks; optional advisory warnings do not change that. Set caps to
make the build budget a gate — enforceable to the extent the bound harness reports usage.
