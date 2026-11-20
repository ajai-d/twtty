# Plan Template

> **Design decision — one coherent plan per domain (never split by document type).**
>
> A plan is never split by document *type* (Architecture / Design / Orchestration in separate files): they are tightly coupled — Design refines Architecture, work items trace to Architecture or to spec FR/NFR — and the `PLAN-EXIT` checklist enforces that traceability.
>
> How the coherent unit is *scoped* follows the domain structure (per [sdlc.md §8.2](../sdlc.md#82-domain-based-separation-of-responsibilities)):
>
> - **Single-domain** → one plan file — `plan/plan.md` (baseline buildout) or `plan-<iteration-id>.md` (Iteration) — the full required template for a baseline, intent-relevant changes and current work items for later Iterations.
> - **Multi-domain** → an overview `plan-<iteration-id>.md` (cross-cutting architecture, domain/layer map, interfaces, domain diagram, global work-item index, dependency table, Team collaboration guidance, and execution-pattern selection) plus one file per domain at `plan/domains/<domain>-<iteration-id>.md` — see the [domain plan template](plan-domain-template.md) — holding its components, design, work items, and file footprint.
>
> This mirrors the [spec template](spec-template.md); the split is by **domain**, never by document type.

> Template for the **Plan** artifact produced by stage tasks 2a, 2b, and 2c of the [SDLC implementation](../sdlc.md#33-plan). Saved by the Architecture / Design / Planning agents to `<project-folder>/plan/plan.md` for the **baseline buildout** (unnumbered), or `<project-folder>/plan/plan-<iteration-id>.md` for a later **Iteration** (where `<iteration-id>` is its generated `Iteration-<YYYYMMDDTHHMMSSZ>-<token>`, §4.3). References to `plan-<iteration-id>.md` / `<domain>-<iteration-id>.md` denote the Iteration case; for the baseline, substitute the unnumbered form (`plan.md`, `<domain>.md`).
>
> **Iteration applicability.** Baselines use the complete required template. Later Iterations include only intent-relevant architecture/design changes and the current work breakdown, dependencies, Team collaboration guidance, and execution controls. Reference unchanged approved plans and diagrams after verifying their continued applicability; do not copy them or add N/A filler. Inherited content remains subject to current risk, policy, environment, and impact checks. Required metadata, current work-item traces/footprints/DAG, execution-pattern selection, approvals, and applicable controls remain enforced.
>
> Replace `[bracketed placeholders]` in included content. Preserve included section names and relative order. The full section-presence instructions below describe the baseline shape; iteration content follows the applicability rule above.

> **Diagram convention.** Mermaid is the standard diagramming format for the plan, and diagrams are first-class deliverables — expert, specific to this system, detailed, and **easy to understand** (never generic placeholders). For baselines, diagrams are **required** for §1.1, §1.3, §1.5, §1.6, §2.1, and — when it lists dependencies — §3.2; **conditional** for every other sub-section whenever it is not `None`/`N/A`. Iterations update affected diagrams and reference valid unchanged approved diagrams; absence of a copied block is not a failure. A changed current work-item DAG must still be shown where dependencies exist. `PLAN-EXIT` check 19 enforces this.
>
> **Diagram types.** Apply **C4 model *semantics*** for architecture (Context / Container / Component levels) but render them as **styled `flowchart`s** with `subgraph` boundaries — avoid the experimental `C4Context`/`C4Container` blocks, which lay out poorly. Use `sequenceDiagram` for §2.1/§2.4/§2.7 flows; `erDiagram` for schemas (§1.2/§2.2); `stateDiagram-v2` for stateful UI (§2.6); a `graph` DAG for §3.2. Do NOT use the informal `journey` type — render user flows/journeys as styled `flowchart`s. **Sanitize labels** (no `& / + ; :` or em dashes, which break Mermaid parsing).
>
> **Colour — semantic, not decorative.** Diagrams that depict boundaries, layers, or distinct element roles MUST apply the standard palette below via `classDef` (colour carries meaning); trivial diagrams (a few nodes, no distinct roles) MAY omit colour. Use `subgraph` to draw trust/environment boundaries and consistent node shapes per role.
>
> | Role | `classDef` | fill / stroke |
> |---|---|---|
> | External actor / user | `actor` | `#E3F2FD` / `#1565C0` |
> | Trust boundary / environment | `boundary` | `#FFF8E1` / `#F9A825` |
> | Compute / service | `compute` | `#E8F5E9` / `#2E7D32` |
> | Data store | `data` | `#F3E5F5` / `#6A1B9A` |
> | Identity / security | `identity` | `#FFEBEE` / `#C62828` |
> | CI/CD / pipeline | `cicd` | `#ECEFF1` / `#455A64` |
>
> Example: `classDef data fill:#F3E5F5,stroke:#6A1B9A,color:#111;`
>
> **Rendering (tiers).** **Tier 1 (default, all levels):** native fenced ` ```mermaid ` blocks — GitHub renders them inline, zero toolchain. **Tier 2 (opt-in; recommended at L4+ or on Human User request):** a Mermaid-CLI (`mmdc`) render step in CI (wired at 3g CI/CD) produces themed SVGs (custom theme/CSS/fonts, beyond GitHub's strict native renderer) committed alongside the fenced source, which still previews inline; the fenced source stays the diffable master and the SVG is a derived artifact. A non-Mermaid tool (D2, PlantUML/C4-PlantUML, etc.) is NOT a project default — it is permitted only as a justified per-diagram exception under the fallback clause.
>
> **Fallback.** ASCII art or a non-Mermaid tool is permitted only where Mermaid genuinely cannot express the intent, with a one-line justification in the sub-section.

---

## Metadata

[REQUIRED as the first `## H2` section of every plan. The **Iteration ID** identifies which Iteration this plan belongs to and MUST equal the `<iteration-id>` in this plan's filename and in the corresponding spec's `## Metadata`. The remaining iteration parameters (Specialization, Runtime target, UX mode, API mode, Discovery mode) live in the corresponding spec's `## Metadata` and are NOT restated here.]

- **Iteration ID:** [for a later Iteration, its generated `Iteration-<YYYYMMDDTHHMMSSZ>-<token>` (for example, `Iteration-20261105T230435Z-7Q2K9F`), which MUST equal the Iteration ID in the corresponding spec's `## Metadata` and the `<iteration-id>` in this plan's filename; for the **baseline buildout**, use `baseline` (the baseline plan is the unnumbered `plan.md`)]
- **Plan confirmed date:** [ISO-8601 UTC date, e.g., `2026-06-05`]

---

## 1. Architecture

### 1.1 Domains and application architecture

[Required. Opens with the **domain structure** per [sdlc.md §8.2](../sdlc.md#82-domain-based-separation-of-responsibilities) — the areas of responsibility carried over from `spec.md` §5.1, now given solution structure — followed by the components within them. Build this architecture from the bound [`best-practices/`](../config/reusable-assets/best-practices/) and [`technical-stack/`](../config/technical-stack/) guidance where present (noting how the design applies or deviates from it); otherwise propose current industry standards per [sdlc.md §6](../sdlc.md#6-guardrails-profile).

**Domains.** One row per domain: name, responsibility, its **file footprint** (the globs it owns), and (at L3+) its owner. Domain footprints MUST be mutually disjoint. When there is more than one domain, also declare the **interface** between each pair of interacting domains and include a **domain diagram** (a Mermaid graph of domains and their interfaces). For a single-domain iteration, replace the domain table with the single line `Single domain — the whole system` and omit the interfaces and diagram. Plan domains trace back to `spec.md` §5.1; record any merge or split with a one-line rationale.

| Domain | Responsibility | File footprint (globs) | Owner (L3+) |
| --- | --- | --- | --- |
| [name] | [one line] | `src/<area>/**`, ... | [owner] |

Interfaces (only when more than one domain):

- [Domain A] → [Domain B]: [what crosses the boundary, in plain terms]

Domain diagram (only when more than one domain):

```mermaid
graph LR
  A[Domain A] --> B[Domain B]
```

**Components.** The system's components, their responsibilities, and how they interact. MUST include a **Mermaid** application-architecture diagram (a `flowchart`/`graph` component view showing the components and how they interact) and a component table. Each component MUST have a unique ID prefixed `C-<n>`; when there is more than one domain, each component names the domain it belongs to.]

- **C-1:** [component name] — [responsibility] [(Domain: <name>) when multi-domain]
- **C-2:** [component name] — [responsibility]

### 1.2 Data architecture

[Optional by default; conditionally required per the current or inherited approved data classification and [sdlc.md §7.1.6](../sdlc.md#716-data-controls): if any `confidential` or `restricted` data class is declared at risk level 3 or higher, this sub-section MUST include a data flow diagram. Otherwise: data stores, schemas, ownership, retention, and data flow. Use "None for this iteration." only when no data classification triggers apply; omission of §14 from an iteration spec does not establish that. When this sub-section is not `None`, include a **Mermaid** data-flow diagram (`flowchart`: sources → stores → consumers), and a `erDiagram` when schemas are described.]

### 1.3 Infrastructure architecture

[Required. Hosting, networking, environments, and deployment topology. For a cloud Runtime target, declare separate infrastructure and application CD paths: responsibilities, triggers, resource ownership, non-secret handoff and compatibility requirements, and shared environment deployment locking, per [sdlc.md §3.4](../sdlc.md#34-execute). MUST include a **Mermaid** infrastructure/topology diagram (a `flowchart` using subgraphs for environments and trust boundaries, showing nodes and networking); show the local development and target environments where applicable. For localhost-only or CLI-only iterations, the diagram MAY be minimal (single node) but MUST be present. At risk level 3 or higher, this section MUST also declare the deployment strategy (blue/green, canary, rolling, or documented alternative) and the rollback plan (trigger conditions, automation, and manual fallback), per [sdlc.md §7.1.4](../sdlc.md#714-deployment-and-operations-controls).]

**Environment ownership.**

[When infrastructure dependencies are in scope, declare one row per owned entry point or existing resource reference under the bound profile's [environment-purpose rule](../config/development/default.md#environment-iac-and-resource-ownership). `Ownership` is `owned` or `reference`. For `owned`, `IaC path` is the product-root-relative entry point and `Apply route` is `local-service`, `developer-iac` or `infra-cd`. For `reference`, record the existing owner in `Dependency`, use `IaC path: none` and `Apply route: reuse`, and identify the authorized reference/access evidence in the design. No new dependency means no filler table; inherited unchanged rows require explicit approved-source references.]

| Dependency | Environment | Ownership | IaC path | Apply route |
|------------|-------------|-----------|----------|-------------|
| [dependency or existing owner/reference] | [local or cloud/stage] | [owned or reference] | [entry point or none] | [local-service, developer-iac, infra-cd or reuse] |

Approved legacy layout or bootstrap/break-glass exceptions must identify their existing approval and ownership; a new plan's incorrect path is not an exception. This table is PLAN's ownership contract, not a second deployment manifest.

Describe required services and the allowed reuse-or-create path without assuming new
resources or demanding endpoint values at PLAN-EXIT. Record this app's configuration
approach (path, key names and startup loader where known) under the profile's
[connection-settings policy](../config/development/default.md#application-connection-settings).
Include necessary configuration writes in the infra work footprint. Instance selection,
capture and preparation follow the profile's
[infra-kickoff procedure](../config/development/default.md#development-infrastructure-first),
not a repeated procedure in the generated plan.

Identify each affected environment in the design, work footprints and apply recipes so ownership is unambiguous. Review their consistency with effective configuration; do not add parser-specific declarations or a separate infrastructure-validation gate. Infrastructure files and executable recipes are authored during EXECUTE, not required to exist at PLAN.

For existing plans, reference approved ownership evidence relevant to current work and preserve unchanged historical artifacts/layouts. Do not require format migrations. Native operations, recovery and preview requirements are defined by the bound development profile and provider, not restated here.

**Inner-loop development.**

[Required. Reference the bound [development policy](../config/development/default.md#policy-ownership); do not copy its setup instructions. Record this app's native build/test/run approach, expected feedback, required services/emulators, container applicability, necessity/identity/data/cost boundaries, required CI/merge checks and selected CD. Identify local verification gaps in §1.6. Reference existing applicable recipes; new application commands/scripts are EXECUTE outputs, not PLAN prerequisites. Non-runnable scopes explain applicability.]

### 1.4 Security architecture

[Optional at L1 only when neither cloud access nor data controls require it; REQUIRED at L2+ and for applicable cloud/data access per [identity controls](../sdlc.md#717-identity-and-access-controls) and [data controls](../sdlc.md#716-data-controls). Declare only the identity patterns actually needed: (a) approved developer Entra for local app/evaluation cloud access; (b) workload identity for cloud-hosted app access; (c) short-lived pipeline federation/credentials when CI/CD actually accesses cloud services/resources, including real-cloud CI evaluations without CD; (d) approved bootstrap when necessary trust is not already reusable. Native local execution and offline-only CI MUST NOT require unrelated hosting identities or CI federation. No long-lived credentials in app config or CI. Determine data-classification triggers from the current spec together with unchanged classification carried forward from approved specs, not from current-section presence alone: if any `internal`, `confidential`, or `restricted` data class is declared, MUST declare encryption-in-transit controls for data that crosses a network boundary (local-only or loopback traffic that crosses no network boundary MAY be documented as N/A); if any `confidential` or `restricted` data class is declared at L2+, MUST also declare encryption-at-rest controls. Include trust boundaries, authorization model, secrets management, and threat-model summary. Use "None for this iteration." only when neither cloud nor data triggers apply. When this sub-section is not `None`, include the required **Mermaid** diagram of applicable identity flows/trust boundaries: local developer, hosted workload identity and pipeline federation only where used.]

### 1.5 Technology choices

[Required. Languages, frameworks, runtimes, libraries, and services chosen. Per [sdlc.md §3.3](../sdlc.md#33-plan), these MUST be proposed from **current sources looked up at plan time** (not assumed from memory) and reconciled with the Human User's stated preferences. Each choice MUST state the reason in one sentence. Also record: (a) a **Currency** note — that the options were looked up at plan time, with the source(s) consulted; and (b) the **Human User preferences** — preferred frameworks/technologies as elicited, or `None stated`. The plan **MUST include** a **Mermaid** stack/layering diagram (`flowchart`/`graph`) mapping the chosen technologies to layers (client → host/edge → API → data → CI/CD → infra).]

- **Currency:** [options looked up at plan time; source(s) consulted]
- **Human User preferences:** [preferred frameworks/technologies as stated, or `None stated`]
- [technology] — [reason]
- [technology] — [reason]

### 1.6 Test architecture

[Conditionally required: if the corresponding `spec.md` Section 8 contains at least one AC, this sub-section MUST be non-empty. Apply the level's [verification contract](../config/risk-calibration/default.md#level-1-verification): L1 describes the basic happy-path smoke, real-service gaps and evidence, not an unselected test/eval suite. At other levels or with selected formal tests, describe the applicable test pyramid, locations, environments and coverage. Distinguish offline, development-cloud and hosted acceptance, with pass criteria and evidence. Use "None for this iteration." only when Section 8 is empty. Include a proportionate **Mermaid** verification-flow diagram for smoke-only work, or a test-pyramid diagram mapping required test levels to CI.]

### 1.7 Operations architecture

[Conditionally required at risk level 3 or higher per [sdlc.md §7.1.4](../sdlc.md#714-deployment-and-operations-controls). Declares the operational envelope of the iteration: SLOs (availability, latency, error rate), alerting approach, on-call model, incident-response entry point, and error-budget policy. SLOs declared here are the source of truth that every alert configured at `execute/3k` Monitoring MUST trace to. For risk levels 1 and 2, this sub-section MAY be `None for this iteration.`. When not `None`, include a **Mermaid** diagram of the SLO → alert → on-call / incident-response flow (`flowchart`).]

- **SLO-1:** [name] — [metric], [target], [measurement window]
- **SLO-2:** [name] — [metric], [target], [measurement window]

## 2. Design

[Sections 2.1 through 2.4 refine the corresponding §1 sub-sections and §2.5 refines §1.6; each such design item MUST trace to its §1 source via a `Refines:` line. Sections 2.6 (UX design) and 2.7 (API design) realize the spec's UX (§13) and API (§15) requirements. §2.1 is required; §2.2–§2.5 are optional — use "None for this iteration." when the corresponding §1 sub-section is also "None for this iteration." or needs no further refinement. §2.6 is required when the spec records UX mode ≠ `N/A`; §2.7 is required when the spec records API mode ≠ `N/A`.]

### 2.1 Application design

[Required. Interfaces, contracts, sequence flows, and component-internal structure refining §1.1. MUST include a **Mermaid** `sequenceDiagram` for each primary use case's happy path (at minimum one per UC declared in `spec.md` §5). Apply the bound [`best-practices/`](../config/reusable-assets/best-practices/) (for example its API design section) where present, noting any deviation.]

- **D-1:** [design item]
  - **Refines:** C-1

### 2.2 Data design

[Optional. Concrete schemas, indexes, migrations, and data contracts refining §1.2. When not `None`, the plan **MUST include** a **Mermaid** `erDiagram` of the concrete schema.]

### 2.3 Infrastructure design

[Required when current work creates/changes infrastructure or its apply recipes; otherwise reference valid inherited design or state non-applicability. Refine §1.3's environment ownership into concrete entry points, environment-local inputs/modules, authorized existing references and apply/CI routes. No shared/cross-environment IaC module dependencies. Paths must agree with effective configuration and current work footprints. When not `None`, include the **Mermaid** flowchart of applicable module composition and apply/pipeline stages; local developer IaC is not hosting CD.]

### 2.4 Security design

[Optional. Concrete identity, secrets, key-rotation, and authorization rules refining §1.4. When not `None`, the plan **MUST include** a **Mermaid** `sequenceDiagram` of the concrete identity/authorization flow and/or a `flowchart` of role assignments.]

### 2.5 Test design

[Optional. Concrete test frameworks, fixtures, mocking strategy, test-data approach, and CI wiring refining §1.6. When not `None`, the plan **MUST include** a **Mermaid** `flowchart` of the CI test-job pipeline.]

- **D-2:** [test design item]
  - **Refines:** §1.6

### 2.6 UX design

[Conditionally required: MUST be non-empty when the corresponding `spec.md` records UX mode ≠ `N/A` (per [SDLC §10](../sdlc.md#10-ux-quality-bar)); otherwise the single line `N/A per spec §13 (iteration ships no UI).`. Apply universal `UX-*` controls and every selected level-sensitive `UX-*` control. Document the named design system and tokens, information architecture, content voice, applicable scan and accessibility results, and approved rendered evidence. Store baseline skill-produced wireframes and interactive prototypes per [UX-003](../config/risk-calibration/default.md#718-ux-controls) under `plan/wireframes/`. For every later UI-affecting Iteration, create incremental wireframes and prototypes for all affected surfaces under `plan/wireframes/<iteration-id>/`; prior artifacts MAY be inputs but MUST NOT be overwritten. Reference unchanged surfaces with the [SDLC §10 impact rationale](../sdlc.md#ux-impact-analysis). In Delegated mode, disclose non-trivial choices with rationale. Include a proportionate **Mermaid** user-flow / information-architecture diagram and add `stateDiagram-v2` only for materially stateful UI.]

**Prototype preview.** Record the current entry point, prototype startup instructions,
preview URL and the primary journeys actually exercised in a browser before PLAN-EXIT.
Provide coherent context for those journeys, reusing unchanged screens/assets where
applicable rather than rebuilding the whole UI. Screenshots supplement this demonstration;
they do not replace it. These are prototype instructions, not application run recipes.

### 2.7 API design

[Conditionally required: MUST be non-empty when the corresponding `spec.md` records API mode ≠ `N/A` (per [sdlc.md §11](../sdlc.md#11-api-quality-bar)); otherwise the single line `N/A per spec §15 (iteration ships no external API).`. The API **solution** that satisfies the spec's §15 contract obligations: the chosen API style; endpoint/resource/operation design and request/response schemas; status semantics; and the concrete versioning mechanism. Select and record the machine-readable contract format and repository path here and author the contract, honoring existing or user-mandated locations in SPEC. In Delegated API mode, non-trivial design choices are disclosed here with rationale. The plan **MUST include** a **Mermaid** `sequenceDiagram` of the request/response including error paths, and (optionally) a `classDiagram`/`erDiagram` of the request and response schemas.]

## 3. Orchestration

### 3.1 Work breakdown

[Required. Decompose by domain first, then into cohesive outcomes that are independently testable, reviewable, and mergeable. Within one domain, prefer disjoint sub-footprints; isolate genuinely shared contracts as prerequisites and prefer fan-out/fan-in over unnecessary chains or all-to-all dependencies. Never add a dependency merely because one item appears earlier. Each item MUST have a unique `W-<n>` ID, title, description, domain, expected file footprint, and `Traces to:` identifying current ACs plus the current or inherited component/requirement it implements. A footprint MUST stay inside its domain; if implementation must leave it, Refine the plan first. Affected inherited ACs MUST include their approved source.]

Maximize meaningful parallel-executable work items across and within domains,
even if the selected execution pattern is Sequential. Apply
[the parallelism-aware breakdown rule](../sdlc.md#33-plan): retain real
dependencies, avoid artificial task inflation, and show available concurrency
and unavoidable serial bottlenecks in §3.3.

| ID | Domain | Title | Description | Expected file footprint | Traces to |
|----|--------|-------|-------------|-------------------------|-----------|
| W-1 | [domain] | [title] | [description] | `src/auth/**`, `package.json` | AC-1, C-1, FR-1 |
| W-2 | [domain] | [title] | [description] | `src/reports/**` | AC-2, C-2, NFR-1 |
| W-3 | [domain] | [title] | [description] | `src/ui/**` | AC-3, C-3, FR-2 |
| W-4 | [domain] | [title] | [description] | `tests/integration/**` | AC-4, C-4, FR-3 |

### 3.2 Sequencing and dependencies

[The table is authoritative for this app's work dependencies. Include each work item once; use `—` for no prerequisite. Express real dependencies that satisfy the bound [development procedure](../config/development/default.md#developer-workstation-inner-loop) and applicable [hosting prerequisites](../sdlc.md#34-execute); do not copy either procedure or invent setup work. Show an acyclic DAG with Mermaid when dependencies exist.]

| Work item | Depends on | Reason |
|---|---|---|
| W-1 | — | Independent foundation |
| W-2 | W-1 | Consumes the approved contract |
| W-3 | W-1 | Consumes the approved contract |
| W-4 | W-2, W-3 | Integrates both changes |

### 3.3 Team collaboration

[Required and assignment-neutral. Record this app's groups, actual shared prerequisites, receiving targets and integration requirements under [SDLC §5.1](../sdlc.md#51-execution-mode-and-execution-pattern) and the profile's [worker-preparation policy](../config/development/default.md#parallel-setup). Reuse the Human's existing Discovery pattern answer rather than asking twice. Select `Sequential`, `Concurrent`, or `Mixed` as guidance, not a second pattern authorization. Include each work item once; concurrent groups must be independent and footprint-disjoint. Do not reproduce generic setup/branching instructions.]

- **Delivery approach:** [Sequential | Concurrent | Mixed]

| Group | Domain | Work items | Relationship | Integration requirement |
|---|---|---|---|---|
| T-1 | [domain] | W-1 | Foundation | Verify before dependent work; no per-item PR |
| T-2 | [domain] | W-2 | Concurrent with T-3 only if authorized | Isolated worker branch; merge into recorded working target |
| T-3 | [domain] | W-3 | Concurrent with T-2 only if authorized | Separate worker branch/worktree; coordinator integrates serially |
| T-4 | [domain] | W-4 | After T-2 and T-3 | Combined local verification, then required domain/scope publication |

---

## PLAN-EXIT validation checklist

The AI Agent MUST verify the applicable checks below mechanically before requesting `PLAN-EXIT` approval (per [SDLC Section 3.3](../sdlc.md#33-plan)).

**Applicability.** Baselines satisfy the complete required shape. Iterations retain metadata (checks 1/20), placeholder removal (2), and current work-item, footprint, DAG, traceability, and control checks, but need only changed architecture/design content. Section references below may resolve to explicitly referenced approved plans/specs when the content is unchanged and still applicable; verify that source rather than requiring a copied section. Current work items and execution-pattern selection must be recorded for this iteration. Unresolved inheritance or changed assumptions must be addressed before approval, not treated as an exemption.

**Multi-domain plans (hub-and-spoke).** The overview holds the current global work-item index, DAG, execution-pattern selection, and relevant cross-domain changes. Baselines include every required domain plan; iterations include affected domain plans and reference valid unchanged approved maps/plans. Validate affected files with the [domain plan checklist](plan-domain-template.md). All effective domain/layer footprints MUST remain mutually disjoint, and every current work item MUST map to one domain and stay within its footprint.

1. `## Metadata` is the first `## H2`. Baselines contain `## 1. Architecture`, `## 2. Design`, and `## 3. Orchestration` in order. Iterations preserve included section names/order and contain current §3.1 Work breakdown, §3.2 Sequencing and dependencies, and §3.3 Team collaboration.
2. No `[bracketed placeholder]` text remains.
3. Baseline required sub-sections are non-empty: §1.1, §1.3, §1.5, §2.1, §3.1, §3.2, and §3.3. Iterations populate changed design/architecture and current §3.1–§3.3; unchanged content may be referenced in approved plans.
4. Conditional sub-section §1.6: if the corresponding `spec.md` Section 8 contains at least one AC, §1.6 MUST be non-empty (not `None for this iteration.`).
5. Baseline optional sub-sections are present with content or `None for this iteration.`: §1.2, §1.4, §1.7, §2.2, §2.3, §2.4, §2.5. Iterations omit unaffected sections without N/A filler; applicable requirements still need current or valid inherited coverage.
6. Baseline §1.1 declares domain structure per [sdlc.md §8.2](../sdlc.md#82-domain-based-separation-of-responsibilities): a domain table with footprints or `Single domain — the whole system`, plus at least one uniquely identified `C-<n>` component; multiple domains also require per-pair interfaces and a domain diagram. Iterations may inherit this structure, updating affected components/interfaces/footprints. Effective footprints remain mutually disjoint.
7. Section 1.5 contains at least one technology choice with a stated reason.
8. Every current design item in §2.1–§2.4 (if any) has a unique `D-<n>` ID and a `Refines:` line referencing a valid `C-<n>` in current §1 or a referenced approved plan.
9. Every design item in §2.5 (if any) has a unique `D-<n>` ID and a `Refines:` line referencing `§1.6`.
10. Current §3.1 contains at least one work item; every item has a unique `W-<n>` ID, title, description, a domain in the current or inherited approved map, and a non-empty Expected file footprint within that domain's footprint. `Traces to:` identifies at least one current `AC-<n>` plus a valid current or inherited approved `C-<n>`/`FR-<n>`/`NFR-<n>`. Every affected inherited AC is also listed with its approved source for current re-verification.
11. Section 3.2 contains every current `W-<n>` exactly once. Each `Depends on` cell is `—` or references existing work-item IDs, every dependency has a non-empty reason, no dependency exists solely because one item appears earlier, and the resulting graph has no cycles.
12. Every new or changed `C-<n>` in current §1.1 is referenced by a current §3.1 work item (no orphan components). Unchanged inherited components need not acquire new implementation work solely to repeat prior coverage.
13. At risk level 3 or higher: §1.3 Infrastructure architecture MUST declare the deployment strategy and the rollback plan (per [sdlc.md §7.1.4](../sdlc.md#714-deployment-and-operations-controls)); §1.7 Operations architecture MUST be non-empty and MUST declare at least one SLO (identified by prefix `SLO-<n>`).
14. Data controls per [sdlc.md §7.1.6](../sdlc.md#716-data-controls) based on the current or inherited approved data classification. Apply current approved changes together with unchanged classification from approved specs; reference the source in existing gate evidence without restating it. Omission of the current spec's §14 is not a no-data declaration. If the applicable classification cannot be established, resolve it before `PLAN-EXIT`. Apply the following conditions to that classification:
    - If any `internal`, `confidential`, or `restricted` data class is declared: §1.4 Security architecture MUST declare encryption-in-transit controls for data that crosses a network boundary (§1.4 MUST NOT be `None for this iteration.`); local-only or loopback traffic that crosses no network boundary MAY be documented as N/A in §1.4.
    - If any `confidential` or `restricted` data class is declared at risk level 2 or higher: §1.4 MUST also declare encryption-at-rest controls.
    - If any `confidential` or `restricted` data class is declared at risk level 3 or higher: §1.2 Data architecture MUST include a data flow diagram (§1.2 MUST NOT be `None for this iteration.`).
15. Identity and access per [sdlc.md §7.1.7](../sdlc.md#717-identity-and-access-controls), using the actual local, hosted and pipeline access contexts, not provider binding alone:
    - §1.4 MUST declare approved developer Entra for local cloud-service access, workload identity when the app is cloud-hosted, and short-lived authentication when pipelines actually access cloud, including real-cloud CI evaluations. Offline-only CI/local execution does not require unrelated federation/hosting identities. No long-lived credentials in app config or CI.
    - Document any necessary trust/bootstrap and scoped RBAC or verified authorized reuse; local developer permissions are independent from pipeline identity. Minimal local-development IaC may precede the dependent app merge or unrelated hosting bootstrap.
    - §3.2 MUST sequence applicable identity verification/bootstrap before the work that actually depends on it. Required hosted/pipeline trust may be satisfied by verified reusable trust; do not create duplicate identities or grant access merely because a provider is selected.
16. UX design per [SDLC §10](../sdlc.md#10-ux-quality-bar): if the corresponding `spec.md` records UX mode ≠ `N/A`, §2.6 UX design MUST be present and non-empty at every level with a named design system, information architecture, skill-produced wireframes and an interactive prototype per UX-003, its entry point/startup/URL and actual browser demonstration of the agreed primary journeys, clean design-quality scan where the skill provides one, and approved rendered evidence under UX-005 (Human, or explicitly delegated L1 Autopilot AI review, attributed truthfully). A later UI-affecting Iteration MUST have current artifacts for every affected surface under `plan/wireframes/<iteration-id>/`; unchanged surfaces require the recorded impact rationale, and prior approved artifacts remain unmodified. If UX mode = `N/A`, §2.6 MUST be the single line `N/A per spec §13 (iteration ships no UI).`.
17. API design per [sdlc.md §11](../sdlc.md#11-api-quality-bar): if the corresponding `spec.md` records API mode ≠ `N/A`, §2.7 API design MUST be present and non-empty (API style, endpoint/schema design, versioning mechanism, and the authored contract at the format/path recorded in §2.7, respecting any SPEC-mandated location). If API mode = `N/A`, §2.7 MUST be the single line `N/A per spec §15 (iteration ships no external API).`.
18. Technology currency per [sdlc.md §3.3](../sdlc.md#33-plan): §1.5 records a **Currency** note (options looked up at plan time, with source(s)) and a **Human User preferences** line (stated preferences or `None stated`), in addition to at least one technology choice with a stated reason (check 7).
19. Diagrams follow the diagram convention. Baselines require literal `mermaid` blocks in §1.1, §1.3, §1.5, §1.6 when applicable, §2.1 for each primary UC, §3.2 when dependencies exist, and applicable conditional sections. Iterations supply affected diagrams and the current dependency DAG where required; unchanged diagrams may be referenced in approved artifacts. Inspect each required current or inherited diagram and verify its continued applicability, rather than asserting presence or demanding a copied block. Architecture/topology/security diagrams use the semantic-colour palette via `classDef` unless trivial. ASCII or another tool requires the existing one-line justification; missing applicable diagrams fail the gate.
20. `## Metadata` is present as the first `## H2` and contains an **Iteration ID** equal to the corresponding spec's ID and, when newly minted, matching the `Iteration-<YYYYMMDDTHHMMSSZ>-<token>` rule in core §4.3 (pre-existing legacy IDs remain valid), plus a **Plan confirmed date** (valid ISO-8601 UTC date); no bracketed placeholder text remains in the Metadata section.
21. For a cloud Runtime target, §1.3 declares separate infrastructure/application CD paths with responsibilities, triggers, resource ownership, handoff/compatibility requirements, and shared environment locking. §3.2 sequences CI promotion checks before target provisioning/app deployment and infrastructure CD before app deployment when both change, per [sdlc.md §3.4](../sdlc.md#34-execute).
22. §1.3 defines or references the approved inner-loop approach, service/emulator/container applicability, development dependencies, boundaries and local-verification gaps; §1.6 gives their checks/pass criteria/evidence. Review environment ownership against effective configuration, hosting metadata, §2.3 design, overview/domain work footprints and recipe/CI/apply paths. Newly owned local-development Azure IaC and Compose use `infra/environments/local/`; selected shared cloud stages use `infra/environments/cloud/<stage>/`. Existing references never duplicate ownership; adopted-layout/route exceptions need explicit applicable approval. No cross-environment modules or implicit cloud-stage/CD selection from Azure usage. Resolve missing/conflicting requirements before `PLAN-EXIT`; no custom infrastructure validator or executable IaC is required at this stage.
23. §3.3 records `Sequential`, `Concurrent`, or `Mixed`; assigns every current `W-<n>` to exactly one assignment-neutral group; names no individual developer; and gives each group a domain, relationship, and integration requirement. It shows available concurrency across and within domains and explains unavoidable serial bottlenecks, without inflating task count or dropping real dependencies. Any concurrent groups are DAG-independent and footprint-disjoint; overlaps are ordered or reconciled by an explicit integration work item/checkpoint.
