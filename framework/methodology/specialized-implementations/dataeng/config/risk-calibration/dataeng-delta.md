# Risk calibration — data engineering overlay

**Category:** `risk-calibration-delta` · The `dataeng` **overlay** that adds data-engineering
control rows **on top of** the baseline
[`risk-calibration/default.md`](../../../sdlc/config/risk-calibration/default.md) ladder. The
confirmed level (assessed at SEED, recorded in `meta/risk-level`) selects the **column**; all
baseline matrix rows continue to apply. These are **minimum** controls per level — a project
MAY raise them, never relax them.

**Legend:** **MUST** = required · **SHOULD** = strongly recommended, adopt-or-justify · **—** =
not required at this level · a numeric cell is the threshold for that level.

## Risk-level interpretation for data engineering

| Level | Data-eng profile |
|:-----:|-----------------|
| **L1** | Ad-hoc analysis script processing local files or a personal sandbox database |
| **L2** | Internal batch pipeline; a few tables; one team downstream; blast radius bounded |
| **L3** | Team-facing pipeline feeding shared dashboards or other teams' pipelines; downstream consumers tolerate short outages |
| **L4** | Customer-facing data (embedded analytics, reporting portal, ML feature store in production, external regulatory reporting) |
| **L5** | Regulated data at scale (GDPR / HIPAA / PCI-DSS / SOX / bank secrecy) or safety-critical decisions based on data outputs |

## 6.1 Data source and sink controls

| Requirement | L1 | L2 | L3 | L4 | L5 |
|-------------|:--:|:--:|:--:|:--:|:--:|
| Every source declared with schema, format, cadence, owner | MUST | MUST | MUST | MUST | MUST |
| Every sink declared with schema, format, cadence, consumer | MUST | MUST | MUST | MUST | MUST |
| Source contract signed with producer team (schema + cadence commitment) | — | — | MUST | MUST | MUST |
| Sink contract published for consumer teams (schema + freshness commitment) | — | — | MUST | MUST | MUST |
| PII flagged per source and per sink | MUST | MUST | MUST | MUST | MUST |

## 6.2 Data quality controls

L1 uses the baseline smoke-only verification contract: run a safe source-to-sink sample
and inspect actual results against the declared quality expectations. Formal DQ test
suites/reports require explicit Human selection or stricter policy; when selected their
approved thresholds still apply. This does not waive data classification or correctness.

| Requirement | L1 | L2 | L3 | L4 | L5 |
|-------------|:--:|:--:|:--:|:--:|:--:|
| At least one quality dimension declared with measurable threshold | MUST | MUST | MUST | MUST | MUST |
| Completeness test per required column (null-rate below threshold) | — | MUST | MUST | MUST | MUST |
| Uniqueness test on declared primary keys | — | MUST | MUST | MUST | MUST |
| Validity test per column with declared domain constraints | — | MUST | MUST | MUST | MUST |
| Referential-integrity test for declared foreign-key relationships | — | — | MUST | MUST | MUST |
| Value-distribution or anomaly-detection test | — | — | SHOULD | MUST | MUST |
| Data quality run outputs persisted under `reports/dq/` | — | MUST | MUST | MUST | MUST |
| Every `DQ-<n>` dimension has ≥1 test referencing the DQ-ID | — | MUST | MUST | MUST | MUST |
| Test failure blocks sink write (fail-closed default) | — | — | MUST | MUST | MUST |

## 6.3 Freshness and cost SLO controls

| Requirement | L1 | L2 | L3 | L4 | L5 |
|-------------|:--:|:--:|:--:|:--:|:--:|
| Freshness SLO (`F-SLO-<n>`) declared per sink | — | MUST | MUST | MUST | MUST |
| Completeness SLO (`C-SLO-<n>`) declared per sink | — | — | MUST | MUST | MUST |
| Cost SLO (`Cost-SLO-<n>`) declared (per-run or per-day) | — | — | MUST | MUST | MUST |
| Alert configured for every declared SLO | — | MUST | MUST | MUST | MUST |

## 6.4 Lineage and observability controls

| Requirement | L1 | L2 | L3 | L4 | L5 |
|-------------|:--:|:--:|:--:|:--:|:--:|
| Table-level lineage discoverable in code or tooling | MUST | MUST | MUST | MUST | MUST |
| Column-level lineage discoverable in code or tooling | — | — | MUST | MUST | MUST |
| Run history retained (min days) | 7 | 30 | 90 | 365 | 730 |

## 6.5 Data contract and schema-evolution controls

| Requirement | L1 | L2 | L3 | L4 | L5 |
|-------------|:--:|:--:|:--:|:--:|:--:|
| Sink schema versioned in `contracts/` or `schemas/` | — | MUST | MUST | MUST | MUST |
| Additive schema changes documented | — | MUST | MUST | MUST | MUST |
| Breaking-change policy documented (major version bump, dual-write window, sunset notice) | — | — | MUST | MUST | MUST |
| Deprecation window ≥ 90 days for external consumers | — | — | MUST | MUST | MUST |
| Backward-compatibility tests against last N consumer versions | — | — | MUST | MUST | MUST |
| Consumer notification protocol declared | — | — | MUST | MUST | MUST |

## 6.6 Backfill controls

| Requirement | L1 | L2 | L3 | L4 | L5 |
|-------------|:--:|:--:|:--:|:--:|:--:|
| Backfill capability supported when pipeline processes time-partitioned data | — | — | MUST | MUST | MUST |
| Backfill idempotency verified (running twice yields same result) | — | — | MUST | MUST | MUST |
| Backfill cost estimated before execution | — | — | — | MUST | MUST |
| Backfill runs logged as replay entries with the target partition range | — | — | MUST | MUST | MUST |

## Overlay application rule

Mirrors the baseline [Matrix application rule](../../../sdlc/config/risk-calibration/default.md#matrix-application-rule).
Before executing any pipeline stage task and before requesting any stage-exit gate approval,
consult the complete overlay for the confirmed level. Apply its MUST rows at the stages
defined by the specialization: declarations at SPEC, design/SLOs/dependencies at PLAN,
and implemented tests, reports, lineage, and operational evidence at their EXECUTE
checkpoints. Mechanically verify the controls due at that checkpoint and surface due
non-mechanical controls for Human attestation. Later-stage evidence is not an early-gate
prerequisite; early approval does not attest future results. Immediate core controls
remain enforced throughout.
