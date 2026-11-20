# Data Engineering Specialized Implementation

> This document extends the [Core TWTTY Specification](../../core-twtty-methodology.md) and the [baseline SDLC implementation](../sdlc/sdlc.md). It MUST NOT weaken the core's approval rules, stage order, or traceability requirements (see [core — Core TWTTY Specification vs. Specialization](../../core-twtty-methodology.md#core-twtty-specification-vs-specialization)).
>
> Everything in the baseline SDLC applies unless this document adds stricter requirements.
>
> This extension is for projects whose primary output is one or more **data pipelines** — code that ingests data from sources, transforms it, and serves it to downstream consumers (warehouses, lakes, marts, dashboards, ML feature stores, other pipelines). Pipeline correctness is measured by data quality dimensions (completeness, uniqueness, validity, consistency, timeliness, accuracy) and freshness SLAs against consumers, not by pass/fail unit tests alone.

> Copyright © 2026 Ajai Peddapanga. Licensed under
> [Apache License 2.0](../../../../LICENSE) — see
> [NOTICE](../../../../NOTICE). Suggested citation: Peddapanga, A. (2026).
> *TWTTY: Data Engineering Specialized Implementation.*
> https://github.com/ajai-d/twtty.

## In this document

| Section | Purpose |
|---------|---------|
| [1. Purpose](#1-purpose) | Scope of the extension for data-pipeline delivery |
| [2. Specialization activation](#2-specialization-activation) | How the Spec Agent knows this implementation is active (bootstrap-driven; mismatch check) |
| [3. Stage and gate deltas](#3-stage-and-gate-deltas) | Additions to SPEC, PLAN, and EXECUTE |
| [4. Artifact locations](#4-artifact-locations) | Where data-eng artifacts live |
| [5. Runtime and roles](#5-runtime-and-roles) | Role decisions for pipeline work |
| [6. Risk enforcement profile delta](#6-risk-enforcement-profile-delta) | Data-eng control rows per risk level |
| [7. Data engineering rules](#7-data-engineering-rules) | Additional executable constraints |

---

## 1. Purpose

This document adds deterministic requirements needed for data-pipeline delivery: data sources and sinks as first-class specification artifacts, a data quality rubric with measurable dimensions, versioned data contracts with breaking-change policies, freshness and cost SLOs, column-level lineage, schema evolution rules, and backfill semantics. It does not replace baseline SDLC; it strengthens it for workloads where the outputs are datasets rather than applications, correctness is measured by data quality against a rubric, and consumers depend on schema and freshness contracts.

---

## 2. Specialization activation

This specialization is activated by `twtty start project type=dataeng …` (see the [TWTTY command dispatcher](../../../twtty.md) and [README quick start](../../../../README.md#quick-start)), which resolves `type=dataeng` to this document. No Discovery-time routing question is asked; the Spec Agent captures the selected specialization during Discovery (`spec/1a`) and records `Specialization: dataeng` in the spec's `## Metadata` block during drafting (`spec/1b`). Discovery has three upfront questions: Discovery mode, UX mode (typically `N/A` for pure data-eng iterations), and API mode (typically `N/A` unless the pipeline exposes a metadata / query API).

**Specialization field value.** The Spec Agent MUST record exactly the following string in the spec's `## Metadata` `Specialization` field for this implementation:

> `dataeng`

**Mismatch check (safety net).** Before beginning Round 1, the Spec Agent MUST verify that the seed content aligns with data-pipeline delivery. If the seed clearly describes a project whose primary output is UI, an API, a library, or an LLM-driven application (rather than transformed data), the Spec Agent MUST surface the mismatch to the Human User, propose switching to the correct specialization, and require the Human User to `Abandon` this session and re-bootstrap with the correct prompt before proceeding. See [baseline SDLC §3.2](../sdlc/sdlc.md#32-spec) for the full mismatch-check rule.

---

## 3. Stage and gate deltas

### 3.1 Spec delta (`spec/1b`)

For the baseline buildout, compose the complete spec using strict inheritance as below. Later Iterations use the baseline template's intent-focused applicability rule: include only affected baseline/addendum sections and fields, carry forward unchanged approved requirements, and retain metadata, acceptance coverage, and applicable data controls.

1. Start from the baseline template [../sdlc/templates/spec-template.md](../sdlc/templates/spec-template.md) and complete the `## Metadata` block plus Sections 1-8. In the `## Metadata` block, record `Specialization: dataeng`.
2. Insert Sections 9-12 from [templates/spec-for-dataeng-template.md](templates/spec-for-dataeng-template.md) between §8 and §13.
3. Complete the baseline `## 13. UX requirements` (typically `N/A per §10 (iteration ships no UI).` for pure data-eng iterations), `## 14. Data classification` (always required and especially load-bearing for data engineering), and `## 15. API requirements and contract` (typically `N/A per §11 (iteration ships no external API).` unless the pipeline exposes a metadata / query API).

> Steps 1–2 describe the single-domain shape. For a **multi-domain** (hub-and-spoke) iteration the overview `spec-<iteration-id>.md` carries no §6–8 (each domain's §5–8 live in `spec/domains/<domain>-<iteration-id>.md`) and §9–12 live in the overview alongside §1–§4 and §13–§15, per the spec addendum's hub-and-spoke note and [sdlc.md §8.2](../sdlc/sdlc.md#82-domain-based-separation-of-responsibilities).

The data-eng baseline spec adds four required sections between §8 and §13; later Iterations include the content affected by their intent:

- Section 9: **Data sources** — upstream systems, schemas, formats, cadence, ownership.
- Section 10: **Data sinks** — downstream consumers, target schemas, formats, freshness commitments.
- Section 11: **Data quality rubric** — measurable dimensions with thresholds that gate every iteration.
- Section 12: **Data contracts** — versioning strategy, breaking-change policy, deprecation window for schemas the pipeline produces.

`SPEC-EXIT` for projects using this extension is satisfied only if all applicable baseline and addendum checks pass. Baseline specs satisfy the full required shape; iteration specs are checked against the approved intent and any inherited content they rely on, not required to repopulate every section.

**Valid data classification is not optional here.** Data-engineering work handles data; an iteration with unchanged classification may carry forward the approved classification without restating §14. It MUST NOT describe inherited data handling as `No data stored, processed, or transmitted by this iteration.` merely because no new class is introduced. If a proposed data-eng scope genuinely handles no data, follow the mismatch check in §2.

### 3.2 Plan delta (`plan/2a`-`plan/2c`)

**Inherited contracts (PLAN and EXECUTE).** Apply current approved changes together with unchanged approved sources, sinks, quality dimensions, contracts, classification, and operational requirements. Omitted delta sections do not make those obligations absent. Reference the approved spec/plan sources in existing gate evidence; unresolved applicable contracts block the gate. Reuse unchanged approved designs and implementation assets when still applicable, but collect current test evidence for affected behavior. Do not invent new source/sink/contract implementation work merely to restate unchanged coverage.

Baselines compose the full required plan below. Later Iterations use the baseline plan's applicability rule, writing affected design and current work/dependencies while referencing valid unchanged approved content:

1. Start from the baseline template [../sdlc/templates/plan-template.md](../sdlc/templates/plan-template.md).
2. Apply the additional data-eng constraints from [templates/plan-for-dataeng-template.md](templates/plan-for-dataeng-template.md).

Data-eng planning strengthens the baseline plan in three ways:

- **Data architecture coverage is REQUIRED** at every level: source-to-sink data flow, storage tiers/retention, and lineage strategy. A baseline writes this in §1.2; an iteration updates affected content or references a still-applicable approved design covering current and inherited sources/sinks.
- **Operations architecture coverage is REQUIRED at every risk level:** freshness SLOs (`F-SLO-<n>`) per sink and, at L3+, completeness SLOs (`C-SLO-<n>`) per sink and cost SLOs (`Cost-SLO-<n>`). An iteration may reference unchanged approved §1.7; changed assumptions/SLOs require current design updates.
- **Current work breakdown covers the change:** provide source/transform/sink/contract work for the scope, and DQ-test items only when formal tests apply. L1 smoke-only does not invent a DQ suite/item. Iterations cover changed implementation/rules and verify affected inherited obligations using applicable existing assets.

`PLAN-EXIT` for projects using this extension is satisfied only if all applicable baseline and addendum checks pass, using current and inherited approved requirements/designs as described above.

### 3.3 Execute delta (`execute/3a`-`execute/3m`)

Baseline execute stage tasks and ordering remain unchanged. Three stage tasks are strengthened:

- **`3f Test`** — Apply the baseline L1 smoke-only contract: inspect an actual safe source-to-sink journey against its approved quality expectations without inventing automated DQ suites/reports. At L2+ or when explicitly selected/required, every applicable current/inherited `DQ-<n>` MUST have a DQ-referenced automated sink test after each pipeline run, with outputs under `reports/dq/`. Inheritance never waives selected tests or thresholds.
- **`3k Monitoring`** — Every applicable current or inherited approved SLO (freshness, completeness, cost) MUST trace to at least one alert, with its source identified in existing monitoring/gate evidence. An unchanged approved alert trace may be reused only when its configuration and assumptions remain valid; affected monitoring changes require current evidence. This does not require recreating unchanged alerts.
- **`3l Observability`** — Column-level lineage MUST be published at L3+ (via dbt exposures, OpenLineage, Marquez, or documented alternative). "Published" means: for every column in every sink schema, the upstream columns and transformations that produced it are discoverable in code or lineage tooling.

`EXECUTE-EXIT` is extended with two additional mandatory conditions:

7. Record current `execute/3f/W-<n>` evidence against applicable approved DQ requirements. L1 smoke-only records the actual source-to-sink sample and inspected outcomes in existing evidence, not a mandatory DQ suite/report. When formal DQ tests apply, record passing scores/comparators/thresholds, requirement/report references, baseline or valid reference, reproducibility context and actual invocations. Reuse baselines only while valid; changed behavior needs current evidence, not future promises or stale passes.
8. For every applicable current or inherited approved SLO (`F-SLO-<n>`, `C-SLO-<n>`, `Cost-SLO-<n>`), existing monitoring/gate evidence MUST identify its approved source and the alert configuration that traces to it. Reuse valid unchanged evidence only under the rule above; changed monitoring is recorded in the current `execute/3k` entry. Alert-without-SLO or SLO-without-alert MUST be marked `Escalate` unless explicitly re-approved.

All eight conditions (baseline 1-6 plus conditions 7-8 above) MUST hold before requesting `EXECUTE-EXIT` approval.

---

## 4. Artifact locations

In addition to baseline SDLC artifact locations:

| Artifact | Canonical location |
|----------|-------------------|
| Pipeline code (transforms, DAGs, dbt models, streaming jobs) | `pipelines/` (or `dags/`, `models/`, or language/tool convention) |
| SQL / DDL | `pipelines/sql/` or `models/` |
| Data quality tests | `tests/dq/` or `models/tests/` (dbt convention) |
| Data quality run outputs (machine-readable) | `reports/dq/` |
| Data contracts (versioned schemas consumed downstream) | `contracts/` or `schemas/` |
| Lineage exports (when tool-managed) | `reports/lineage/` |
| Backfill scripts and manifests | `pipelines/backfill/` |

Existing or user-mandated source, sink, and consumer-contract locations remain SPEC constraints. Select new implementation test/report and generated-contract locations during PLAN/EXECUTE, using the defaults above unless alternatives are justified; record actual locations and invocations with the execution evidence. SPEC declares verification and baseline requirements, not newly generated test files or observed measurements.

---

## 5. Runtime and roles

No new mandatory agent role is introduced.

- The baseline `Test Agent` remains the owner of data quality test execution under stage task `3f`.
- The baseline `Monitoring Agent` remains the owner of SLO-tied alerting under stage task `3k`.
- The baseline `Observability Agent` remains the owner of lineage publication under stage task `3l`.
- The default agent MAY configure a dedicated data-engineering custom agent (dbt-aware, Airflow-aware, Dagster-aware, Spark-aware, etc.), but this is optional and does not change stage-task ownership.

**Data catalog and lineage tools.** Common data-eng tooling (dbt, Airflow, Dagster, Prefect, Great Expectations, Soda, Monte Carlo, OpenLineage, Marquez) is configured via the customization surfaces documented in [sdlc.md §5.2](../sdlc/sdlc.md#52-customization-surfaces-and-runtime-features). Configuration decisions cross a trust boundary when they read/write production data warehouses; the default agent MUST ask before configuring any MCP server, hook, or custom agent that touches a production data plane.

---

## 6. Risk enforcement profile delta

This section adds data-eng-specific control rows to the baseline [sdlc.md §7.1 Risk calibration matrix](../sdlc/sdlc.md#71-risk-calibration-matrix). The concrete per-level **values** — and the data-eng **risk-level interpretation** of L1–L5 — are defined in the bound **`risk-calibration-delta`** overlay, [`risk-calibration/dataeng-delta.md`](config/risk-calibration/dataeng-delta.md); all baseline matrix rows continue to apply, and the confirmed level (recorded in `meta/risk-level`) selects the column. The sub-sections below are stable reference anchors; each names the controls, states **where** they are applied, and links to the correspondingly-numbered section of the overlay.

### 6.1 Data source and sink controls

Source/sink declaration (schema, format, cadence, owner/consumer), producer/consumer contracts, and PII flagging — applied in `spec §9` (sources), `spec §10` (sinks), and `spec §14` (data classification). Values: [`dataeng-delta.md §6.1`](config/risk-calibration/dataeng-delta.md#61-data-source-and-sink-controls).

### 6.2 Data quality controls

Quality-dimension declaration plus completeness, uniqueness, validity, referential-integrity, and distribution tests, persisted DQ reports, and fail-closed sink writes — the quality dimension is declared in `spec §11` and the tests run at `3f Test`. Values: [`dataeng-delta.md §6.2`](config/risk-calibration/dataeng-delta.md#62-data-quality-controls).

### 6.3 Freshness and cost SLO controls

Freshness, completeness, and cost SLOs per sink, and an alert per declared SLO — SLOs declared in `plan §1.7`, alert traces recorded at `3k Monitoring`. Values: [`dataeng-delta.md §6.3`](config/risk-calibration/dataeng-delta.md#63-freshness-and-cost-slo-controls).

### 6.4 Lineage and observability controls

Table- and column-level lineage and run-history retention — applied at `3l Observability`. Values: [`dataeng-delta.md §6.4`](config/risk-calibration/dataeng-delta.md#64-lineage-and-observability-controls).

### 6.5 Data contract and schema-evolution controls

Sink-schema versioning, additive-change documentation, breaking-change policy, deprecation window, backward-compatibility tests, and consumer notification — schemas and policy in `spec §12`, compatibility tests at `3f Test`. Values: [`dataeng-delta.md §6.5`](config/risk-calibration/dataeng-delta.md#65-data-contract-and-schema-evolution-controls).

### 6.6 Backfill controls

Backfill capability, idempotency, pre-execution cost estimation, and partition-range logging — declared in `plan §3` / `pipelines/backfill/` and logged as `execute/3i/backfill-<yyyymmdd-hhmm>` replay entries. Values: [`dataeng-delta.md §6.6`](config/risk-calibration/dataeng-delta.md#66-backfill-controls).

**Matrix application rule.** Matches [sdlc.md §7.1 Risk calibration matrix](../sdlc/sdlc.md#71-risk-calibration-matrix): spec-side rows are enforced at `SPEC-EXIT` via the spec addendum checklist; plan-side rows at `PLAN-EXIT` via the plan addendum checklist; EXECUTE-side rows at `EXECUTE-EXIT` condition 5.

---

## 7. Data engineering rules

These rules extend the baseline [sdlc.md §9 Execution rules](../sdlc/sdlc.md#9-execution-rules) with data-eng specifics.

1. **Sources and sinks are contracts.** Every data source in `spec §9` MUST have a documented schema and cadence. Every data sink in `spec §10` MUST publish a versioned contract in `contracts/` or `schemas/` at L2+. Silent schema changes on either side MUST be caught by CI schema-drift checks (see baseline [sdlc.md §7.1.3](../sdlc/sdlc.md#713-cicd-controls)).
2. **Fail closed on data quality.** At L3+, a data-quality test failure MUST prevent the sink write (fail-closed default). Alternative fail-open strategies MUST be explicitly approved by the Human User at SPEC time with rationale recorded in `spec §11`.
3. **Freshness is a first-class SLO.** Every sink MUST have a declared freshness SLO from L2+. Freshness violations MUST alert on-call, not just log. Freshness debt MUST be tracked in `plan §1.7`.
4. **Backfills are gated.** At L3+, any backfill run MUST have a pre-execution cost estimate, a rollback path (revert to prior partition), and an idempotency confirmation. Backfills MUST be logged as `execute/3i/backfill-<yyyymmdd-hhmm>` replay-log entries with the target partition range in `Execution outcome`.
5. **Schema evolution is versioned.** At L2+, sink schemas MUST be versioned in `contracts/` or `schemas/`. Breaking changes MUST bump the major version and follow the deprecation window declared in `spec §12`.
6. **Column-level lineage at L3+.** From L3 onward, every column in every sink MUST be traceable to its upstream columns and transformations via code (SQL comments, dbt refs), tool-managed lineage (dbt exposures, OpenLineage, Marquez), or documented alternative. Lineage MUST be published via the `execute/3l` replay-log entry.
7. **Cost is an iteration constraint.** Cost SLOs in `plan §1.7` at L3+ are iteration gates. An iteration that consistently exceeds its cost SLO MUST be marked `Escalate` at `execute/3m` unless the SLO is explicitly re-approved with rationale.
8. **PII flow is traced end-to-end.** For every column classified as PII in a source (per `spec §9`) or in a sink (per `spec §10`), the transformation path MUST be traced in `plan §1.2 Data architecture`, and access controls (masking, tokenization, row-level security) MUST be declared in `plan §1.4 Security architecture` per baseline [sdlc.md §7.1.6](../sdlc/sdlc.md#716-data-controls).
