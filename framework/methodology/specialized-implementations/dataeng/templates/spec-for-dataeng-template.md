# Spec Addendum (For Data Engineering)

> This file is a strict addendum to the baseline SDLC spec template at [../../sdlc/templates/spec-template.md](../../sdlc/templates/spec-template.md).
>
> **Baseline shape — do not duplicate baseline sections here.** The composed baseline spec MUST contain, in order: (1) the baseline `## Metadata` block plus `## 1.`–`## 8.` from the baseline template; (2) Sections 9-12 from this addendum inserted between §8 and §13; (3) the baseline `## 13. UX requirements` (typically `N/A per §10 (iteration ships no UI).` for pure data-eng iterations), `## 14. Data classification` (always required and load-bearing here), and `## 15. API requirements and contract` (typically `N/A per §11 (iteration ships no external API).` unless the pipeline exposes a metadata / query API). The spec's metadata MUST record `Specialization: dataeng`.
>
> **Iteration applicability.** Follow the baseline template's intent-focused rule. Include only affected source, sink, quality, contract, and other requirements/fields; unchanged approved content carries forward without restatement or N/A filler. Required metadata, valid data classification, acceptance coverage, and active data controls remain enforced.
>
> **Multi-domain (hub-and-spoke) iteration.** In a multi-domain iteration the overview `spec-<iteration-id>.md` carries no §6–8 (each domain's use cases, FR, NFR, ACs live in `spec/domains/<domain>-<iteration-id>.md` per [sdlc.md §8.2](../../sdlc/sdlc.md#82-domain-based-separation-of-responsibilities)), so "between §8 and §13" does not apply to the overview. Sections 9–12 are whole-system addendum foundations and live in the **overview `spec-<iteration-id>.md`** alongside §1–§4 and §13–§15. A §9–12 concern specific to one domain (for example, a source, sink, quality dimension, or contract owned solely by that domain) MAY instead live in that domain's `spec/domains/<domain>-<iteration-id>.md`. A single-domain iteration keeps §9–12 inline between §8 and §13 as described above.
>
> All `[bracketed placeholders]` MUST be replaced. Section headings MUST be preserved verbatim for mechanical validation.

---

## 9. Data sources

[One H3 subsection per source. ID prefix: `SRC-<n>`.]

### 9.1 SRC-1: [source name]

- **Owner:** [team or system responsible for producing this data]
- **Producer team / system:** [where the data originates]
- **Data format:** [Parquet, JSON, CSV, Avro, Protobuf, database rows, event stream, etc.]
- **Access mechanism:** [connection URI, credentials location (Vault path, KMS key), network path (VPC / peering / public / privatelink)]
- **Cadence:** [batch: cron schedule; streaming: emit rate + partitioning]
- **Schema location:** [path to canonical schema, e.g., `contracts/src-1/v1.yaml`, or documented inline below]
- **PII columns:** [enumerate PII columns; must align with `## 14. Data classification` PII inventory]
- **Retention on source side:** [how long the producer retains the data before rotation / deletion]
- **Contract commitment level:** [informal / documented / signed — required at L3+ per §6.1]
- **Escalation path:** [what to do when source fails or violates cadence; who owns the incident]

## 10. Data sinks

[One H3 subsection per sink. ID prefix: `SNK-<n>`.]

### 10.1 SNK-1: [sink name]

- **Consumers:** [teams / systems / dashboards / models that read this sink]
- **Storage location:** [warehouse.schema.table, S3 path, Iceberg table URI, etc.]
- **Data format:** [Parquet, Iceberg, Delta, warehouse-native table, materialized view, etc.]
- **Cadence:** [batch: emit schedule; streaming: emit rate + partitioning]
- **Schema location:** [path to published contract, e.g., `contracts/snk-1/v2.yaml`; ties to §12]
- **PII columns and masking strategy:** [enumerate; describe masking / tokenization / row-level security applied]
- **Freshness commitment:** [max lag from source event time to sink availability; ties to plan §1.7 F-SLO-<n>]
- **Retention on sink side:** [max age of rows; deletion policy]
- **Consumer notification protocol:** [how consumers are told about schema changes — email list, Slack channel, changelog file]

## 11. Data quality rubric

[One H3 subsection per data quality dimension. ID prefix: `DQ-<n>`. Common dimensions: Completeness, Uniqueness, Validity, Consistency, Timeliness, Accuracy. Each dimension MUST be measurable and gate a sink write when it fails at L3+.]

### 11.1 DQ-1: [dimension name, e.g., Completeness]

- **Definition:** [what this dimension measures]
- **Scope:** [which sinks and which columns this dimension applies to]
- **Metric formula:** [precise formula, e.g., `null-rate = count(WHERE col IS NULL) / count(*)`]
- **Comparator:** [`>=` | `<=` | `==` | `range`]
- **Threshold:** [numeric threshold + units]
- **Aggregation:** [per-column / per-partition / per-run / rolling window]
- **Measurement window:** [single run, last 24h, last 7d, etc.]
- **Fail behavior:** [`block sink write` (default at L3+ per §7 rule 2) | `warn only` (requires SPEC-time approval)]
- **Verification approach:** [L1: actual source-to-sink smoke/inspection; formal DQ suites only when selected/required. At other levels, applicable automated tests/reports. Concrete paths/invocations are PLAN/EXECUTE outputs.]
- **Baseline approach/reference:** [how the baseline will be established, or an applicable existing measured reference; new numeric values are recorded during EXECUTE]

### 11.2 DQ-2: [next dimension]

[...repeat for each dimension...]

## 12. Data contracts

[One H3 subsection per data contract. Every `SNK-<n>` declared in §10 whose consumers include external / cross-team readers MUST have a contract here at L2+. ID prefix: `DC-<n>`.]

### 12.1 DC-1: [contract for SNK-1]

- **Sink covered:** [`SNK-<n>` reference]
- **Contract path:** [`contracts/snk-1/v1.yaml`, `contracts/snk-1/v1.proto`, or equivalent]
- **Current version:** [semver `major.minor.patch`, dated `YYYY-MM-DD`, or documented alternative]
- **Version scheme:** [semver / dated / both]
- **Consumers explicitly notified:** [list teams and systems that receive change notices]
- **Breaking-change policy:** [major-version bump plan; dual-write window if applicable; sunset notice format]
- **Deprecation window:** [minimum notice period for breaking changes; MUST be ≥ 90 days for external consumers at L3+ per §6.5]
- **Consumer notification protocol:** [email list, Slack channel, changelog file — how consumers are told]
- **Backward-compatibility test coverage:** [which prior versions have automated compat tests; path under `tests/dq/compat/`]

### 12.2 DC-2: [next contract]

[...repeat for each sink that requires a contract...]

---

## SPEC-EXIT validation checklist (addendum)

The AI Agent MUST pass the applicable baseline checks in [../../sdlc/templates/spec-template.md](../../sdlc/templates/spec-template.md) and applicable checks below. Baselines satisfy the full shape. Iterations scope section/field presence checks to the approved intent and verify inherited sources, sinks, quality rules, contracts, and classification in their approved artifacts when needed. Unchanged sections need not be repeated; metadata and active risk/data controls still apply.

1. `## Metadata` records `Specialization: dataeng`.
2. `## 14. Data classification` is NOT the "No data stored, processed, or transmitted by this iteration." line — data-eng iterations handle data by definition.
3. Section 9 contains at least one `### 9.<n> SRC-<n>:` subsection with all 10 required fields non-empty.
4. Section 10 contains at least one `### 10.<n> SNK-<n>:` subsection with all 10 required fields non-empty.
5. Every source cadence and every sink cadence is declared (no missing cadence).
6. Section 11 contains at least one `### 11.<n> DQ-<n>:` subsection with metric, comparator, threshold, aggregation, window, fail behavior, verification approach, and baseline approach/reference. New test artifacts and measured baseline values are not SPEC-EXIT prerequisites.
7. Every `SNK-<n>` in Section 10 is referenced by at least one `DQ-<n>` in Section 11 (no orphan sinks).
8. Section 12 contains one `### 12.<n> DC-<n>:` subsection per `SNK-<n>` declared in Section 10 whose consumers include external / cross-team readers.
9. Every `DC-<n>` in Section 12 has a versioned contract path (not `[bracketed placeholder]`).
10. Every column flagged PII in Section 9 or Section 10 is also flagged in `## 14. Data classification` (PII inventory in §14.2).
11. At risk level 3 or higher: every `DC-<n>` declares a deprecation window ≥ 90 days for external consumers.
12. Baseline `## 13. UX requirements` is `N/A per §10 (iteration ships no UI).` unless the iteration also ships UI (rare for pure data-eng iterations; if UI is shipped, baseline §13 rules apply in full).
13. Baseline `## 15. API requirements and contract` is either `N/A per §11 (iteration ships no external API).` or fully populated per baseline §15 rules (some data-eng iterations expose a metadata/query API — treat that surface under baseline §11 API quality bar).
