# Plan Addendum (For Data Engineering)

> This file is a strict addendum to the baseline SDLC plan template at [../../sdlc/templates/plan-template.md](../../sdlc/templates/plan-template.md).
>
> **Do not duplicate baseline sections here.** Start from the baseline plan template, then apply the constraints below. The `## Metadata` block of the corresponding spec MUST record `Specialization: dataeng`.
>
> In a **multi-domain** (hub-and-spoke) iteration, the baseline sections these constraints reference are distributed per [sdlc.md §8.2](../../sdlc/sdlc.md#82-domain-based-separation-of-responsibilities): apply each constraint to whichever file holds that section — the overview `plan-<iteration-id>.md` for cross-cutting sections, or the relevant `plan/domains/<domain>-<iteration-id>.md`.

> **Iteration applicability.** Baselines use the complete required shape. Later Iterations write affected design and current work items, referencing valid unchanged approved sources, sinks, DQ rules, contracts, diagrams, and SLOs. All checks use current plus inherited approved requirements, not only sections present in the delta spec. Missing or unresolved coverage blocks approval; inheritance does not waive verification of affected behavior.

---

## 1. Architecture — data-eng constraints

### 1.2 Data architecture (REQUIRED — not Optional here)

Data-architecture coverage is REQUIRED at every risk level. Baselines write §1.2 in full; iterations update affected design or reference an approved design verified to cover current and inherited sources/sinks. The coverage MUST include:

- **Data flow diagram** from every applicable current or inherited approved `SRC-<n>` to every applicable `SNK-<n>`, showing all transformation stages between them.
- **Storage tier declaration** for each intermediate and final data layer (for example: `raw` → `cleansed` → `curated` → `mart`), with retention per tier.
- **Lineage-tracking strategy:** declarative in SQL comments and dbt refs; tool-managed via dbt exposures / OpenLineage / Marquez; or a documented alternative. Named strategy MUST be recorded here so `execute/3l` knows how to publish lineage.

### 1.7 Operations architecture (REQUIRED at every risk level)

Operations-architecture coverage is REQUIRED at every risk level (not conditional at L3+ per baseline). Use current §1.7 or a verified applicable approved plan reference. It MUST cover:

- **Freshness SLOs (`F-SLO-<n>`)** per `SNK-<n>`: target lag from source event time to sink availability, measurement window.
- **Completeness SLOs (`C-SLO-<n>`)** per `SNK-<n>` at L3+: percentage of expected records delivered, measurement window.
- **Cost SLOs (`Cost-SLO-<n>`)** at L3+: per-run compute cost, per-day / per-month total, backfill cost cap.
- **Alerting approach:** how alerts fire (on-call rotation, paging platform).
- **On-call model:** who is on-call, rotation cadence, escalation path.
- **Incident-response entry point:** runbook location, initial triage steps.
- **Error-budget policy:** what happens when an SLO burns budget — for example, freeze non-critical features until debt recovers.

Example SLO declarations:

- **F-SLO-1:** `SNK-1` freshness — event time to sink ≤ 15 min P95 over 24 h window.
- **C-SLO-1:** `SNK-1` completeness — ≥ 99.5% of expected daily records over 30-day window.
- **Cost-SLO-1:** total pipeline compute cost ≤ $120 per day averaged over 7-day window; backfill cost cap $500 per run.

---

## 3. Orchestration — data-eng constraints

### 3.1 Work breakdown (additional constraints)

Baselines include implementation work for every source, sink, transformation, quality dimension, and contract. Iterations include work for new or changed implementation/rules and verify affected inherited obligations using existing assets; unchanged assets do not require new implementation items. Naming enables mechanical coverage checks:

| Item pattern | Purpose | One per |
|--------------|---------|---------|
| `W-<n>-source` | Implements source ingestion | Each `SRC-<n>` in `spec §9` |
| `W-<n>-transform` | Implements a transformation stage | Each transformation stage in `plan §1.2` data flow |
| `W-<n>-sink` | Implements sink write and schema publish | Each `SNK-<n>` in `spec §10` |
| `W-<n>-dq` | Implements a required/selected formal data quality test; not an automatic L1 smoke item | Each `DQ-<n>` needing formal test implementation |
| `W-<n>-contract` | Publishes a versioned contract | Each `DC-<n>` in `spec §12` |

Example:

| ID | Title | Description | Traces to |
|----|-------|-------------|-----------|
| W-1-source | Ingest orders API | Poll orders API hourly; land raw JSON in `raw.orders`. | C-1, SRC-1 |
| W-2-transform | Cleanse orders | Type-cast, dedupe, filter invalid records. | C-2, SRC-1 |
| W-3-sink | Publish curated orders | Materialize `curated.orders`; publish schema `contracts/curated-orders/v1.yaml`. | C-3, SNK-1 |
| W-4-dq | Completeness on curated.orders | Null-rate ≤ 0.1% on order_id and customer_id. | DQ-1, SNK-1 |
| W-5-contract | Contract v1 for curated.orders | Publish and notify consumer teams. | DC-1, SNK-1 |

### 3.2 Sequencing and dependencies (additional constraints)

Current work items MUST show these dependency edges when both items are current work. Where a prerequisite is already implemented, reference and verify the existing approved prerequisite instead of inventing a new implementation item:

- Every `W-<n>-transform` depends on the relevant `W-<n>-source` items.
- Every `W-<n>-sink` depends on the relevant `W-<n>-transform` items.
- Every `W-<n>-dq` depends on the corresponding `W-<n>-sink` (quality tests run against the sink, not against sources).
- Every `W-<n>-contract` depends on the corresponding `W-<n>-sink` (contracts describe published sinks).

---

## PLAN-EXIT validation checklist (addendum)

The AI Agent MUST pass the applicable baseline checks in [../../sdlc/templates/plan-template.md](../../sdlc/templates/plan-template.md) and checks below. Section references may resolve to valid unchanged approved plans/specs. Current work, dependency, and verification coverage remains mandatory; no section is treated as empty merely because it was inherited.

1. Current or referenced approved data architecture contains a valid data flow diagram covering applicable current and inherited `SRC-<n>`/`SNK-<n>` and affected transformations.
2. That architecture declares storage tiers, retention per tier, and a lineage-tracking strategy.
3. Current or referenced approved operations architecture declares at least one `F-SLO-<n>` per applicable `SNK-<n>` at every risk level.
4. At risk level 3 or higher, it also declares at least one `C-SLO-<n>` per applicable sink and at least one `Cost-SLO-<n>`.
5. Current §3.1 contains a `W-<n>-source` for every source whose ingestion implementation is new or changed; baseline coverage includes all sources. Verify inherited prerequisites for unchanged ingestion.
6. Current §3.1 contains a `W-<n>-sink` for every new or changed sink implementation; baseline coverage includes all sinks.
7. When formal DQ tests apply, current §3.1 has `W-<n>-dq` coverage for required new/changed test implementations and verification of affected inherited thresholds. L1 smoke-only uses normal source-to-sink verification, not an invented DQ-test work item.
8. Current §3.1 contains a `W-<n>-contract` for every new or changed published contract; baseline coverage includes all required contracts. Applicable inherited consumer-compatibility obligations still have verification coverage.
9. Current dq-items depend on current sink-items where applicable; otherwise identify verified existing sinks. Current-work dependencies form an acyclic graph.
10. Current contract-items depend on current sink-items where applicable; otherwise identify verified existing sinks. Do not add old work items to the current DAG merely to repeat completed implementation.
