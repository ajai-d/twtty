# Domain Plan Template

> Per-domain plan for a **multi-domain** iteration (hub-and-spoke, per [sdlc.md §8.2](../sdlc.md#82-domain-based-separation-of-responsibilities)). Saved to `<project-folder>/plan/domains/<domain>-<iteration-id>.md` (baseline buildout: `plan/domains/<domain>.md`) and owned by the domain's team (its `CODEOWNERS` entry).
>
> The overview [`plan-<iteration-id>.md`](plan-template.md) (the baseline's is `plan.md`) holds cross-cutting architecture, the domain/layer map, the interfaces and domain diagram, the **global work-item index**, the **DAG**, and the **execution-pattern selection**. **This file holds only THIS domain's components, design, work items, and file footprint.** A single-domain scope uses the single plan template. Baselines use its complete required shape; later Iterations include current work and affected design, referencing valid unchanged approved content.
>
> IDs (`C-<n>`, `D-<n>`, `W-<n>`) are scoped to this file; the overview's global work-item index qualifies each with the domain (`<domain>:W-<n>`). Replace placeholders in included content and preserve included headings. Iterations need no N/A filler or copies of unchanged components/design; metadata, current work items, traceability, and isolation checks remain required.

---

## Metadata

- **Iteration ID:** [for a later Iteration, its generated `Iteration-<YYYYMMDDTHHMMSSZ>-<token>`, which MUST equal the overview plan's Iteration ID and the `<iteration-id>` in this file's filename; for the **baseline buildout**, use `baseline` (baseline domain files are `<domain>.md`)]
- **Domain:** [name — matches the overview's domain/layer map and this domain's spec]
- **Owner:** [team or handle — becomes the `CODEOWNERS` entry for the footprint below]
- **File footprint:** [the globs this domain owns, e.g. `src/billing/**`. MUST be **disjoint** from every other domain and layer footprint. Every work item below MUST stay within this footprint.]
- **Depends on:** [other domains/layers this consumes, via the plan overview's interfaces (`plan.md` §1.1); or `None`. Dependencies flow downward only (business domain → app platform → infra) and MUST NOT form a cycle.]

## 1. Components

[This domain's components and their responsibilities. Each MUST have a unique ID prefixed `C-<n>`.]

- **C-1:** [component name] — [responsibility]

## 2. Design

[Interfaces, contracts, and internal structure refining §1. Each design item MUST have a unique `D-<n>` ID and a `Refines:` line referencing a `C-<n>`. Use `None for this domain.` if no further refinement is needed.]

- **D-1:** [design item]
  - **Refines:** C-1

## 3. Work items

[The atomic work items delivering this domain. Each MUST have a unique `W-<n>` ID, a title, a one-paragraph description, an **expected file footprint** that is a **subset of the domain footprint** in Metadata, and a `Traces to:` line referencing a current `AC-<n>` plus a `C-<n>` in this file or an `FR-<n>`/`NFR-<n>` in this domain's spec. Affected inherited ACs include their approved source. These items feed the overview's global work-item index, DAG, and execution-pattern selection.]

Apply the [parallelism-aware breakdown rule](../sdlc.md#33-plan) within this
domain: maximize meaningful independent work with disjoint sub-footprints,
retain real prerequisites, and expose concurrency and integration requirements
in the overview's Team collaboration section.

| ID | Title | Description | Expected file footprint | Traces to |
|----|-------|-------------|-------------------------|-----------|
| W-1 | [title] | [description] | `src/<domain>/...` | AC-1, C-1, FR-1 |

---

## Per-domain `PLAN-EXIT` checklist

The AI Agent MUST verify applicable checks mechanically before this domain plan contributes to `PLAN-EXIT`. Baselines use the full required shape. Iterations retain metadata, current work items, footprint/dependency checks, and valid traces; unchanged design/components/maps may be referenced in approved artifacts after verifying applicability.

1. `## Metadata` present with `Iteration ID` (matching the overview plan's Iteration ID), `Domain`, `Owner`, a non-empty `File footprint`, and `Depends on` (no placeholders).
2. This domain's `File footprint` is **disjoint** from every other domain's and layer's footprint (checked against the overview's domain/layer map).
3. Baselines contain `## 1. Components`, `## 2. Design`, and `## 3. Work items` in order. Iterations include affected component/design sections and current `## 3. Work items`, preserving relative order.
4. No `[bracketed placeholder]` text remains.
5. Baseline §1 contains at least one uniquely identified `C-<n>`. Iterations may reference unchanged components in this domain's approved plan.
6. Every current `D-<n>` (if any) has a `Refines:` referencing a valid current or inherited approved `C-<n>` in this domain.
7. Current §3 contains at least one `W-<n>`; every item has a unique ID, title, description, and expected footprint within the domain footprint. `Traces to:` identifies at least one current AC plus a valid current or inherited approved component/requirement in this domain. Every affected inherited AC includes its approved source for current re-verification.
8. Every entry in `Depends on` names a domain/layer in the current or inherited approved overview and respects the downward-only, acyclic dependency rule.
9. Infrastructure design, recipe/apply references and work footprints agree with the overview's environment ownership and [PLAN check 22](plan-template.md#plan-exit-validation-checklist). Newly owned local-development cloud dependencies stay in the local environment; existing references do not transfer ownership. Review affected domain plans as well as the overview.
