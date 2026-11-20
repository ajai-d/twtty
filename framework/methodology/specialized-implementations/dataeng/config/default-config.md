# Data Engineering — default configuration (addendum)

This file holds the **shipped defaults** the `dataeng` specialization **adds to** the baseline
SDLC defaults. It does **not** restate the baseline bindings: a project using this
specialization inherits every binding from the baseline
[`sdlc/config/default-config.md`](../../sdlc/config/default-config.md) and layers the
data-eng-specific binding(s) below on top.

```yaml
specialization: dataeng
overrides: sdlc/config/default-config.md   # adds to / overrides the baseline; keys below layer on top
```

## How this file is used

Use this source with the baseline for initial resolution or an approved refresh (see the
[baseline file](../../sdlc/config/default-config.md#how-this-file-is-used)). Copy the whole
baseline config tree and merge this specialization's config tree into the project folder.
Compose a complete local `default-config.md`, merging nested mappings by key; addendum
values override baseline defaults. Write `runtimeconfig.md` with the same binding keys
and nesting, substituting approved user overrides. All config references resolve in the
project-owned tree. Later runs use that complete local configuration, not live fallback
to this addendum or the baseline library; existing project overrides remain supported.

---

## Default bindings (additions to the baseline)

```yaml
# --- risk-calibration overlay ------------------------------------------------
# Adds data-engineering control rows ON TOP OF the baseline risk-calibration
# ladder (source/sink, data quality, SLOs, lineage, contracts, backfill — by level).
# All baseline rows still apply.
risk-calibration-delta: risk-calibration/dataeng-delta.md   # data-eng requirements by level
```

---

## What each binding governs

| Key | Governs | Default rationale |
|-----|---------|-------------------|
| `risk-calibration-delta` | data-engineering control values by risk level — source/sink declaration and contracts, data-quality tests, freshness/completeness/cost SLOs, lineage and observability, schema-evolution, and backfill, added to the baseline ladder (see [`dataeng-delta.md`](risk-calibration/dataeng-delta.md)) | `dataeng-delta.md` — the default data-eng ladder |
