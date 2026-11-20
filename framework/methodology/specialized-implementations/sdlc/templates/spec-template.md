# Spec Template

> **Design decision — one coherent spec per domain (never split by document type).**
>
> A spec is never split by document *type* (e.g., `business-requirements.md`, `use-cases.md`, `technical-spec.md`): use cases, requirements, and acceptance criteria for a given area stay in one coherent file, because they are tightly coupled — FRs reference use cases, ACs reference FRs/NFRs, and the `SPEC-EXIT` checklist enforces that traceability.
>
> How that coherent unit is *scoped* follows the domain structure (per [sdlc.md §8.2](../sdlc.md#82-domain-based-separation-of-responsibilities)):
>
> - **Single-domain** → one spec file — `spec/spec.md` (baseline buildout) or `spec-<iteration-id>.md` (Iteration) — the full required template for a baseline, intent-relevant content for later Iterations.
> - **Multi-domain** → an overview `spec-<iteration-id>.md` (goals, domain/layer map, cross-domain journeys, links) plus one coherent file per domain at `spec/domains/<domain>-<iteration-id>.md` — see the [domain spec template](spec-domain-template.md) — holding that domain's use cases, FR, NFR, ACs. Intra-domain traceability lives in each domain file; cross-domain references are named as dependencies in the overview's domain map and formalized as **interfaces in the plan** (`plan.md` §1.1), never as raw cross-file FR references.
>
> Either way, reproducibility at the acceptance-criteria level (per [core §4.5](../../../core-twtty-methodology.md#45-rules)) depends on each spec unit being one coherent contract.
>
> Note: the [plan template](plan-template.md) follows the same shape — single `plan-<iteration-id>.md` for one domain, or an overview plus `plan/domains/<domain>-<iteration-id>.md` for many. The split is by **domain**, never by document type.

> Template for the **Technical Specification** artifact produced by stage task 1b (Draft specification) of the [SDLC implementation](../sdlc.md#32-spec). Saved by the Spec Agent to `<project-folder>/spec/spec.md` for the **baseline buildout** (unnumbered), or `<project-folder>/spec/spec-<iteration-id>.md` for a later **Iteration** (where `<iteration-id>` is its generated `Iteration-<YYYYMMDDTHHMMSSZ>-<token>`, §4.3). References to `spec-<iteration-id>.md` / `<domain>-<iteration-id>.md` denote the Iteration case; for the baseline, substitute the unnumbered form (`spec.md`, `<domain>.md`).
>
> **Baseline specs** use the full template and its applicable required sections. **Iteration specs** use it as a guide: include only sections and fields needed for the approved Iteration Intent. Unchanged requirements carry forward without being restated; omission does not remove them. Do not retain placeholders or add N/A filler for unaffected sections. Required metadata, discovery approvals, and applicable risk/security/data controls remain enforced. New or changed requirements MUST be clear, testable, and covered by acceptance criteria.
>
> All `[bracketed placeholders]` in included content MUST be replaced. Preserve the names and order of included section headings for mechanical validation. The full section-presence and N/A instructions below define the baseline shape; iteration content is governed by the applicability rule above. Section numbers `9`–`12` are reserved for specialized addendums (see [sdlc-for-agentic-apps template](../../sdlc-for-agentic-apps/templates/spec-for-agentic-apps-template.md)) and are absent from baseline SDLC specs.

---

## Metadata

[REQUIRED as the first `## H2` section of every spec. Populated during drafting (`spec/1b`) from confirmed Discovery (`spec/1a`) decisions: Specialization is the resolved active specialization from the command/project evidence or explicit confirmation per the [dispatcher](../../../../twtty.md); the other six fields are Discovery mode, UX mode, API mode, iteration ID, confirmed date and the **confirmed application-hosting outcome**. Runtime target is `N/A` when no cloud application hosting is selected, even with an Azure development-service binding; a hosting provider must match the resolved project-owned cloud selection. Provider selection alone MUST NOT enable CD. This is the canonical spec metadata section. Changing its fields after `SPEC-EXIT` requires an approved Refine cycle.]

- **Iteration ID:** [for a later Iteration, its generated `Iteration-<YYYYMMDDTHHMMSSZ>-<token>` (for example, `Iteration-20261105T230435Z-7Q2K9F`), which MUST equal the `<iteration-id>` in this spec's filename; for the **baseline buildout**, use `baseline` (the baseline spec is the unnumbered `spec.md`)]
- **Discovery mode:** [`Delegated` | `Interactive`]
- **Specialization:** [`baseline SDLC` | `sdlc-for-agentic-apps` | `dataeng`]
- **Runtime target:** the confirmed application-hosting provider (for example `azure`), matching the project's resolved local `cloud` binding, or `N/A` for no cloud application hosting. Discovery invokes the [development profile's two delivery choices](../config/development/default.md#discovery-and-configuration): local development with shared CI (default), or the same plus cloud CD. `N/A` does not disable approved Azure development services or shared CI. Validate against project-owned config, not shared-library presence. Cloud hosting selects the provider implementations of [identity controls](../sdlc.md#717-identity-and-access-controls) and [IaC/CD rules](../sdlc.md#9-execution-rules).
- **UX mode:** [`Delegated` | `Interactive` | `N/A`]
- **API mode:** [`Delegated` | `Interactive` | `N/A`]
- **Spec confirmed date:** [ISO-8601 UTC date, e.g., `2026-06-05`]

---

## 1. Goals

[What this iteration achieves. Bullet list, one goal per bullet.]

## 2. Stakeholders

[Who is affected by or accountable for this iteration. Bullet list: name/role + relationship.]

## 3. Success metrics

[How success is measured. Each metric MUST be quantified (target number, units, measurement window).]

## 4. Constraints

[Hard limits the solution MUST honor (technology, timeline, budget, compliance, integration). Use "None for this iteration." if there are no constraints.]

## 5. Domains and use cases

> **§5 diagrams (problem-space only), coloured per the shared semantic palette (see the [plan template Diagram convention](plan-template.md)). Both are rendered as styled `flowchart`s — do NOT use the experimental `C4Context` or the informal `journey` diagram types (they render poorly / unprofessionally). Sanitize labels (no `& / + ; :` or em dashes, which break Mermaid parsing).**
>
> - **System context — MUST.** A styled `flowchart` with C4 Level-1 semantics: the system in a `subgraph`, its personas/actors, and the external systems it depends on, coloured by role. MAY be minimal for a simple system.
> - **User journey — MUST when UX mode ≠ `N/A`.** A styled horizontal `flowchart` of the primary persona(s)' journey — phase `subgraph` lanes, coloured per persona. In a multi-domain overview each step names the domain(s) it touches (this is the cross-domain journey).
>
> **Design diagrams live in the plan, not the spec.** Component, sequence, ER/schema, topology, UX *flow*/sitemap, and API request/response diagrams are solution-space and belong in `plan.md`. Do not place them here.

### 5.1 Domains

[The system's domains — its areas of responsibility — derived by the AI Agent from the requirements per [sdlc.md §8.2](../sdlc.md#82-domain-based-separation-of-responsibilities) and reviewed by the Human User in plain language. One row per domain: a name and a one-line responsibility. Problem-space only — interfaces, file footprints, and ownership are declared later in `plan.md` §1.1, not here. For a single-domain iteration, replace the table with the single line `Single domain — the whole system`.]

| Domain | Responsibility |
| --- | --- |
| [name] | [one-line area of responsibility] |

> **Cross-domain journeys (multi-domain overview).** Captured visually by the user-journey diagram above (each step annotated with the domain(s) it touches); you MAY also list them textually here. Domain-local use cases move to each `spec/domains/<domain>-<iteration-id>.md`; a single-domain iteration keeps its use cases inline as §5.2+.

### 5.2 UC-1: [title]

- **Actors:** [who initiates / participates]
- **Triggers:** [what starts the flow]
- **Main flow:** [numbered steps, happy path]
- **Exceptions:** [error / alternate flows]
- **Dependencies:** [other use cases, systems, or data this depends on]
- **Domain:** [the domain from §5.1 this use case belongs to; omit for a single-domain iteration]

### 5.3 UC-2: [title]

[...repeat for each use case...]

## 6. Functional requirements (FR)

[Functional Requirements: what the system MUST do. One per line, ID-prefixed as `FR-<n>`. Each FR MUST be referenced by at least one acceptance criterion in Section 8. When §5.1 declares more than one domain, each FR MUST name the domain it belongs to via a trailing `(Domain: <name>)`; single-domain iterations omit it.]

- **FR-1:** [requirement] [`(Domain: <name>)` when multi-domain]
- **FR-2:** [requirement]

## 7. Non-functional requirements (NFR)

[Non-Functional Requirements: qualities the system MUST exhibit (performance, security, availability, accessibility, etc.). One per line, ID-prefixed as `NFR-<n>`. Each NFR MUST be referenced by at least one acceptance criterion in Section 8. When §5.1 declares more than one domain, each NFR MUST name the domain it belongs to via a trailing `(Domain: <name>)`. Use "None for this iteration." if there are no NFRs.]

- **NFR-1:** [requirement]
- **NFR-2:** [requirement]

## 8. Acceptance criteria

[Acceptance Criteria: objectively verifiable pass/fail conditions per [core §4.5](../../../core-twtty-methodology.md#45-rules). One per line, ID-prefixed as `AC-<n>`. Each AC MUST trace to one or more FR/NFR via a `Traces to:` line. Vague terms ("fast", "user-friendly", "robust") are prohibited.]

- **AC-1:** [criterion stated as pass/fail]
  - **Traces to:** FR-1
- **AC-2:** [criterion stated as pass/fail]
  - **Traces to:** FR-2, NFR-1

---

## 13. UX requirements

[Conditionally required per [SDLC §10 UX quality bar](../sdlc.md#10-ux-quality-bar). Holds the UX **requirements** only — the testable obligations the UI MUST satisfy. The UX **design** that satisfies them is produced in [plan.md §2.6](plan-template.md#26-ux-design), not here. If UX mode is `Delegated` or `Interactive`, all of §13.1–§13.4 below MUST be present and non-empty, and §13.5 MUST be present for `Delegated`. If UX mode = `N/A`, the entire §13 body MUST be `N/A per §10 (iteration ships no UI).`.]

[Section numbers 9–12 are reserved for specialized addendums (e.g., sdlc-for-agentic-apps). §13 UX requirements, §14 Data classification (always required), and §15 API requirements and contract (conditional) are the last mandatory sections.]

### 13.1 Task efficiency

[Steps from arrival to first useful action; justify any splash, welcome, confirmation, or multi-step flow with specific user benefit.]

### 13.2 Interaction

[Feedback ≤ 100 ms rule for every user action; keyboard-navigation coverage; destructive-action policy (confirmation or undo).]

### 13.3 Accessibility

[State the `UX-007` keyboard and accessible-default requirements when selected. When `UX-008` is selected, require WCAG 2.2 AA and its applicable contrast, semantic, and keyboard outcomes. When `UX-009` is selected, require automated accessibility CI. Every affected theme independently meets the selected bar.]

### 13.4 Testing

[Require fast local smoke evidence and the bound design skill's complete authored process and applicable deterministic scan. Add accessibility-compliance testing, automated accessibility CI, Nielsen review, and the lightweight study only when selected `UX-008`–`UX-010` controls require them.]

### 13.5 Delegated-mode disclosures

[Required only when UX mode = `Delegated`. Table of non-trivial UX **requirement** choices with rationale, one row per choice, IDs `U-<n>`. Design-level disclosures live in plan.md §2.6. Silent adoption is prohibited by SDLC §10.]

| # | Choice | Rationale |
| --- | --- | --- |
| U-1 | [choice] | [rationale] |

---

## 14. Data classification

[Required for baseline specs and iteration changes affecting data handling, classification, or controls, per [sdlc.md §7.1.6](../sdlc.md#716-data-controls). Declares the sensitivity of data stored, processed, or transmitted in the approved scope. If no data is handled, replace all subsections below with the single line `No data stored, processed, or transmitted by this iteration.` directly under §14; omit §14.1–§14.4, without N/A filler. An iteration with unchanged data handling may omit §14 and inherit the approved classification; introducing no new data classes is not a no-data declaration. Applicable downstream controls remain enforced per the [§7.1 Risk calibration matrix](../sdlc.md#71-risk-calibration-matrix).]

### 14.1 Data classes present in this iteration

[Required when the approved scope handles data. One row per class stored, processed, or transmitted: `public` (no protection required), `internal` (Company-only), `confidential` (need-to-know), `restricted` (regulated, PII, secrets, financial, health). Omit rows for classes not present. For genuinely no-data scopes, use the §14 declaration and omit this subsection.]

| Class | Present? | Examples in this iteration |
| --- | --- | --- |
| public | [yes/no] | [what data] |
| internal | [yes/no] | [what data] |
| confidential | [yes/no] | [what data] |
| restricted | [yes/no] | [what data, including specific PII types] |

### 14.2 PII inventory

[Required whenever any `restricted` data is present. Enumerate PII classes stored, processed, or transmitted — for example: email, phone, government identifier, IP address, geolocation, biometric, financial account, health identifier. Describe each class's storage, processing, and transmission. Only if none of these activities handles PII, use the single line `No PII stored, processed, or transmitted by this iteration.` Where neither the classification nor another active control requires this subsection, it may be omitted.]

### 14.3 Retention windows

[Required whenever any `internal`, `confidential`, or `restricted` data is present. One row per applicable class, stating maximum retention window and deletion policy. This subsection may be omitted when its classification/control triggers do not apply.]

| Class | Maximum retention | Deletion policy |
| --- | --- | --- |
| [class] | [duration] | [scheduled deletion, deletion on user request, immutable log with sunset, etc.] |

### 14.4 Regulatory scope

[Required whenever any `restricted` data is present. Named regulations that apply to this iteration (for example, GDPR, HIPAA, PCI-DSS, SOC 2, ISO 27001). Use `None` if no external regulations apply. This subsection may be omitted when its classification/control triggers do not apply. Silent adoption of regulatory obligations is prohibited.]

---

## 15. API requirements and contract

[Conditionally required per [sdlc.md §11 API quality bar](../sdlc.md#11-api-quality-bar). Holds the API **contract obligations and requirements** only — style-agnostic. The API **design** that satisfies them (style, endpoints, schemas, versioning implementation, the authored contract) is produced in [plan.md §2.7](plan-template.md#27-api-design), not here. If the confirmed API mode (recorded in the spec's meta section per sdlc.md §11) is `Delegated` or `Interactive`, all of §15.1–§15.7 below MUST be present and non-empty, and §15.8 MUST be present when the mode is `Delegated`. If API mode = `N/A`, the entire §15 body MUST be the single line `N/A per §11 (iteration ships no external API).`.]

### 15.1 Versioning strategy

[Version-identification and compatibility obligations, including how consumers are protected when versions change. Preserve any existing consumer contract or user-mandated versioning interface as a constraint. Otherwise the concrete URI/header/media-type/schema mechanism is selected in PLAN.]

### 15.2 Contract document

[At L2+, require a published machine-readable API contract under a stable repository path and CI regeneration or verification. Record the publication/verification obligations here; PLAN §2.7 selects the format/path and authors the contract, and EXECUTE implements verification. An existing or user-mandated contract location may be referenced, but a newly generated contract or exact future file path is not a SPEC-EXIT prerequisite.]

### 15.3 Breaking-change policy

[What constitutes a breaking change on this API and how breaking changes are introduced (major version bump, sunset header, deprecation notice, sunset headers on responses, etc.).]

### 15.4 Deprecation window

[Minimum notice period before a deprecated version is removed. At L3+ MUST be at least 6 months for external consumers unless an approved shorter window is recorded here with rationale.]

### 15.5 Auth and authorization

[Authentication mechanism (OAuth 2.x, mTLS, API key, signed request, or documented alternative) and authorization model (RBAC, ABAC, capability tokens, or documented alternative). At L3+ MUST also declare per-consumer rate-limit and quota policy.]

### 15.6 Error contract

[Standard error shape applied uniformly across the API surface: for HTTP APIs, status codes plus structured body; for gRPC, status codes plus details; for GraphQL, error extensions; or documented alternative.]

### 15.7 Backward-compatibility tests

[How prior public versions are covered by automated tests. At L3+ at least one test per prior public version MUST run in CI and gate merges. State `N/A — first public iteration` for an iteration with no prior public versions.]

### 15.8 Delegated-mode disclosures

[Required only when API mode = `Delegated`. Table of non-trivial API **contract** choices with rationale, one row per choice, IDs `A-<n>`. Design-level disclosures live in plan.md §2.7. Silent adoption is prohibited per sdlc.md §11 Delegated-mode rule.]

| # | Choice | Rationale |
| --- | --- | --- |
| A-1 | [choice] | [rationale] |

---

## SPEC-EXIT validation checklist

The AI Agent MUST verify the applicable checks below mechanically before requesting `SPEC-EXIT` approval (per [SDLC Section 3.2](../sdlc.md#32-spec)).

**Applicability.** Baseline specs satisfy the full required shape. For iteration specs, metadata (check 1), placeholder removal (check 3), and discovery evidence (check 17) remain required; other presence, non-empty, field, and diagram checks apply only to content needed for the approved intent. Verify inherited content or references against existing approved artifacts when needed, without copying them into this spec. New or changed requirements need valid acceptance coverage. Missing unaffected sections are not failures, and omission does not waive existing requirements or applicable controls.

**Multi-domain specs (hub-and-spoke).** In the full baseline shape, the overview holds §1–§4, the domain/layer map, cross-domain journeys and problem-space diagrams, and whole-system §13/§14/§15 foundations; domain files hold their use cases, FRs, NFRs, and ACs and use the [domain spec checklist](spec-domain-template.md). In later Iterations, create only the affected overview/domain content and inherit unchanged approved domain specs and maps. Apply checks 1–4 and 13–17 to relevant overview content and checks 4–12 to relevant domain content. Every affected domain spec MUST pass its applicable checks, and cross-domain references MUST resolve against the current or inherited approved map.

1. `## Metadata` section is present as the first `## H2` and contains all seven required fields (Iteration ID, Discovery mode, Specialization, Runtime target, UX mode, API mode, Spec confirmed date), each with a valid value: Discovery mode, Specialization, UX mode, and API mode from their declared enumerations; **Runtime target is either `N/A` or the provider identified by the resolved `cloud` selection in the project's `runtimeconfig.md`, whose config file resolves locally**; for a later Iteration the Iteration ID matches this spec's filename `<iteration-id>` and, when newly minted, matches the `Iteration-<YYYYMMDDTHHMMSSZ>-<token>` rule in core §4.3 (pre-existing legacy IDs remain valid); for the **baseline buildout** the Iteration ID is `baseline` and the spec is the unnumbered `spec.md`; and Spec confirmed date is a valid ISO-8601 UTC date. No bracketed placeholder text remains in the Metadata section.
2. Baseline specs contain the required H2 sections in order: `## Metadata`; `## 1. Goals` through `## 8. Acceptance criteria`; §13 when UX mode ≠ `N/A`; §14; and §15 when API mode ≠ `N/A`. Iteration specs retain `## Metadata` and only the intent-relevant sections, preserving their names and relative order. In a multi-domain overview, domain-local §6–8 live in domain files. Sections 9–12 are reserved for specialized addendums and, when included, appear between §8 and §13.
3. No `[bracketed placeholder]` text remains.
4. Baseline required sections 1, 2, 3, 5, 6, 8, and 14 are non-empty; sections 4 and 7 MAY be `None for this iteration.` Iteration specs populate only required intent-relevant content. Where domain structure is needed, §5.1 contains the domain table or `Single domain — the whole system`, or an iteration relies on the existing approved structure.
5. Where use cases are required, section 5 contains at least one `### 5.<n> UC-<n>:` subsection (numbered from 5.2). Multi-domain use cases, FRs, and NFRs identify a domain in the current or inherited approved domain map.
6. Baseline UCs contain Actors, Triggers, Main flow, Exceptions, and Dependencies, plus `Domain` when multi-domain. Iteration UCs include changed fields and enough context to assess the change; unchanged fields may be verified in the approved UC without restatement.
7. Where functional requirements are in scope, section 6 contains at least one FR; every FR has a unique `FR-<n>` ID.
8. Every NFR (if any) has a unique `NFR-<n>` ID.
9. Baseline section 8 contains at least one AC. Every Iteration contains at least one current AC across its overview and affected domain specs, and its current ACs collectively cover every outcome in the approved Iteration Intent. Affected inherited requirements and ACs are referenced by approved source for current re-verification rather than copied. Every current AC has a unique `AC-<n>` ID and a `Traces to:` line referencing a valid current or inherited FR or NFR.
10. Every `FR-<n>` declared in Section 6 is referenced by at least one AC in Section 8 (no orphan FRs).
11. Every `NFR-<n>` declared in Section 7 (if any) is referenced by at least one AC in Section 8 (no orphan NFRs).
12. No AC contains the prohibited vague terms `fast`, `user-friendly`, `robust`, `easy`, `simple`, `intuitive` (case-insensitive whole-word match) per [core §4.5](../../../core-twtty-methodology.md#45-rules).
13. Baseline specs with UX mode ≠ `N/A` include non-empty §13.1–§13.4 and, for Delegated mode, §13.5 with at least one `U-<n>` non-trivial choice disclosure. Iterations include the UX requirements/disclosures affected by their intent; unchanged UX obligations carry forward. Baseline UX mode `N/A` uses `N/A per §10 (iteration ships no UI).`; iterations may omit an unaffected §13.
14. §14 Data classification MUST be present for baseline specs and iteration changes affecting data handling, classification, or controls. For genuinely no-data scopes, its body is only `No data stored, processed, or transmitted by this iteration.`; §14.1–§14.4 are omitted. Otherwise §14.1 lists the classes present; §14.2 and §14.4 are required for restricted data, and §14.3 for internal/confidential/restricted data. Required subsections are non-empty, and the no-PII declaration is valid only when no PII is stored, processed, or transmitted. Other subsections may be omitted unless active controls require them. Unchanged iteration classification may carry forward without restatement; absence of new data classes is not proof of no data handling.
15. Baseline specs with API mode ≠ `N/A` include non-empty §15.1–§15.7 and, for Delegated mode, §15.8 with at least one `A-<n>` non-trivial choice disclosure. Iterations include API requirements/disclosures affected by their intent; unchanged contract obligations carry forward. Baseline API mode `N/A` uses `N/A per §11 (iteration ships no external API).`; iterations may omit an unaffected §15.
16. Baseline §5 contains a styled `flowchart` system-context diagram and, when UX mode ≠ `N/A`, a styled user-journey diagram with phase lanes and persona colouring (in the overview for hub-and-spoke specs). Iterations update only problem-space diagrams affected by their intent; unchanged approved diagrams carry forward. Included diagrams use `flowchart`, the shared palette, and sanitized labels, not `C4Context` or `journey`. Solution-space diagrams (component, sequence, ER, topology, UX flow, API) belong in the plan, not the spec.
17. **(Backstop — primary enforcement is at the front of `spec/1a`, per [SDLC §3.2](../sdlc.md#32-spec).)** The `spec/1a` Discovery record (the discovery transcript and/or the `spec/1a` replay-log entry) shows that the three upfront questions (Discovery mode, UX mode, API mode) were **put to the Human User** and the Human User's answers — an explicit "you decide" counting as the Delegated selection. A recorded mode value with no evidence it was asked (a silent default) fails this check.
