# SDLC for Agentic Apps — default configuration (addendum)

This file holds the **shipped defaults** the `sdlc-for-agentic-apps` specialization **adds to**
the baseline SDLC defaults. It does **not** restate the baseline bindings: a project using this
specialization inherits every binding from the baseline
[`sdlc/config/default-config.md`](../../sdlc/config/default-config.md) and layers the
agentic-specific binding(s) below on top.

```yaml
specialization: sdlc-for-agentic-apps
overrides: sdlc/config/default-config.md   # adds to / overrides the baseline; keys below layer on top
```

## How this file is used

Use this source with the baseline for initial resolution or an approved refresh (see the
[baseline file](../../sdlc/config/default-config.md#how-this-file-is-used)). Copy the whole
baseline config tree and merge this specialization's config tree into the project folder.
Compose a complete local `default-config.md`, merging nested mappings by key so
`tokenomics.product` preserves `tokenomics.build`; addendum values override baseline
defaults. Write `runtimeconfig.md` with the same binding keys and nesting, substituting
approved user overrides. All config references resolve in the project-owned tree. Later
runs use that complete local configuration, not live fallback to this addendum or the
baseline library; existing project overrides remain supported. Spec-defined budgets
retain references to the project's own spec.

---

## Default bindings (additions to the baseline)

```yaml
# --- risk-calibration overlay ------------------------------------------------
# Adds agentic-evaluation control rows ON TOP OF the baseline risk-calibration
# ladder (run count N, variance, pass rule, by level). All baseline rows still apply.
risk-calibration-delta: risk-calibration/eval-delta.md   # agentic eval requirements by level

# --- tokenomics (product) ----------------------------------------------------
# The baseline binds only tokenomics.build. This specialization adds the product
# runtime budget — what the built agentic app spends at runtime (per request / session / day).
# The default profile sets all caps to `none` (tracked, not enforced); a project records its
# confirmed ceilings and degradation policy in its spec's cost-budget section (the gate).
tokenomics:
  product: tokenomics/product/product-profile1.md   # default product budget (all caps none)

# --- agentic-stack -----------------------------------------------------------
# The agentic runtime stack: agent framework/SDK, model platform, default model,
# orchestration pattern, tool/MCP ecosystem, and tracing/guardrail tooling.
# Framework/platform/model defaults live in the bound agentic-stack profile.
# The `cloud` binding still governs HOW the model endpoint is provisioned and
# authenticated (managed identity, no keys); this binding governs WHAT stack is used.
agentic-stack: agentic-stack/default.md
```

---

## What each binding governs

| Key | Governs | Default rationale |
|-----|---------|-------------------|
| `risk-calibration-delta` | agentic evaluation requirements by risk level — eval coverage, stochastic run count, variance reporting, and pass rule, added to the baseline ladder (see [`eval-delta.md`](risk-calibration/eval-delta.md)) | `eval-delta.md` — N=1/N≥3/N≥5 by level |
| `tokenomics.product` | runtime tokens/cost evidence for affected LLM work; approved non-`none` caps add enforcement/degradation tests (see [`product-profile1.md`](tokenomics/product/product-profile1.md)) | `product-profile1.md` — default no caps |
| `agentic-stack` | the agent framework/SDK, model platform, model, orchestration and tool/guardrail ecosystem; read concrete choices from the bound profile, confirm applicable changes at PLAN 2a and record them in `plan.md §1.5` | [`agentic-stack/default.md`](agentic-stack/default.md) supplies initial choices; existing projects retain adopted choices until an approved update |
