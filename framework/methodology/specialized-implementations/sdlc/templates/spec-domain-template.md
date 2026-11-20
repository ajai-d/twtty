# Domain Spec Template

> Per-domain spec for a **multi-domain** iteration (hub-and-spoke, per [sdlc.md §8.2](../sdlc.md#82-domain-based-separation-of-responsibilities)). Saved to `<project-folder>/spec/domains/<domain>-<iteration-id>.md` (baseline buildout: `spec/domains/<domain>.md`) and owned by the domain's team (its `CODEOWNERS` entry).
>
> The overview [`spec-<iteration-id>.md`](spec-template.md) (the baseline's is `spec.md`) holds goals, the domain/layer map, cross-domain journeys, and whole-system foundations (data classification, plus the whole-system UX (§13) and API (§15) requirements). **This file holds only THIS domain's use cases, requirements, and acceptance criteria** — one coherent contract for the domain. A single-domain iteration does not use this template; it uses the single spec file (`spec.md` or `spec-<iteration-id>.md`) under that template's applicability rule. (Interfaces between domains are a PLAN concern, declared in `plan.md` §1.1.)
>
> IDs (`UC-<n>`, `FR-<n>`, `NFR-<n>`, `AC-<n>`) are scoped to this file. A reference from the overview or another domain MUST qualify the ID with the domain (`<domain>:FR-<n>`) and MUST go through a **dependency named in the overview's domain map** (formalized as an interface in the plan, `plan.md` §1.1) — never a raw FR-to-FR link across domains.
>
> Baseline domain specs use the complete required shape. Later iterations include only domain sections/fields needed for the approved Iteration Intent, following the [overview's applicability rule](spec-template.md#spec-exit-validation-checklist). Unchanged requirements and domain maps carry forward without restatement or N/A filler; omission does not remove them. Required metadata and applicable controls remain enforced. Replace placeholders in included content and preserve included section headings.

---

## Metadata

- **Iteration ID:** [for a later Iteration, its generated `Iteration-<YYYYMMDDTHHMMSSZ>-<token>`, which MUST equal the overview spec's Iteration ID and the `<iteration-id>` in this file's filename; for the **baseline buildout**, use `baseline` (baseline domain files are `<domain>.md`)]
- **Domain:** [name — matches the overview's domain/layer map and this domain's footprint]
- **Owner:** [team or handle — becomes the `CODEOWNERS` entry for this domain's footprint]
- **Depends on:** [other domains or layers this domain consumes, named plainly (the plan formalizes each as an interface); or `None`]

## 1. Use cases

[One H3 subsection per use case, ID-prefixed `UC-<n>`. Each MUST include all five sub-bullets.]

### 1.1 UC-1: [title]

- **Actors:** [who initiates / participates]
- **Triggers:** [what starts the flow]
- **Main flow:** [numbered steps, happy path]
- **Exceptions:** [error / alternate flows]
- **Dependencies:** [other use cases; for anything cross-domain, name the dependency on the other domain (the plan formalizes it as an interface)]

## 2. Functional requirements (FR)

[What this domain MUST do. One per line, ID-prefixed `FR-<n>`. Each FR MUST be referenced by at least one acceptance criterion in §4.]

- **FR-1:** [requirement]

## 3. Non-functional requirements (NFR)

[Qualities this domain MUST exhibit. One per line, ID-prefixed `NFR-<n>`. Each NFR MUST be referenced by at least one AC in §4. Use `None for this domain.` if there are none.]

- **NFR-1:** [requirement]

## 4. Acceptance criteria

[Objectively verifiable pass/fail conditions. One per line, ID-prefixed `AC-<n>`, each with a `Traces to:` line referencing at least one `FR-<n>`/`NFR-<n>` in this domain. For an iteration relying on an unchanged requirement, verify the trace against its approved domain spec rather than copying the requirement here. Vague terms (`fast`, `user-friendly`, `robust`, `easy`, `simple`, `intuitive`) are prohibited.]

- **AC-1:** [criterion stated as pass/fail]
  - **Traces to:** FR-1

## 5. Domain-specific UX / API (optional)

[Only this domain's screens or endpoints. Whole-system UX and API foundations live in the overview. Use `N/A` if this domain ships no UI or API of its own.]

---

## Per-domain `SPEC-EXIT` checklist

The AI Agent MUST verify the applicable checks mechanically before this domain spec contributes to `SPEC-EXIT`. Baseline domain specs satisfy the full shape. Iterations retain metadata and placeholder checks but scope content/field checks to the approved intent, verifying inherited references in their approved domain artifacts when needed. New or changed requirements still require valid acceptance coverage.

1. `## Metadata` present with `Iteration ID` (matching the overview spec's Iteration ID), `Domain`, `Owner`, and `Depends on` filled (no placeholders).
2. Baseline required sections appear in order: `## 1.` through `## 4.` (`## 5.` when the domain ships its own UI/API). Iterations include only intent-relevant sections in that order.
3. No `[bracketed placeholder]` text remains.
4. Where use cases are required, §1 contains at least one `UC-<n>`. Baseline UCs have all five sub-bullets; iteration changes may rely on unchanged fields in the approved UC.
5. Where functional requirements are required, §2 contains at least one `FR-<n>`; every FR and NFR has a unique ID within this file.
6. Every `FR-<n>` (and every `NFR-<n>`, if any) is referenced by at least one AC in §4 (no orphans).
7. New or changed requirements have an `AC-<n>` in §4; every AC has a valid `Traces to:` within this domain's current or inherited approved requirements, and contains no prohibited vague term.
8. Every cross-domain dependency in `Depends on` or a use case names a domain in the current or inherited approved overview map (formalized as an interface in the plan), not a raw ID in another domain file.
