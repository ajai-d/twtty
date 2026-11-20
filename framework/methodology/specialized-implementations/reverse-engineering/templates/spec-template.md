# Reverse Engineering Spec Template

> Save as `<project-folder>/spec/spec.md` for the **baseline buildout** (unnumbered), or
> `<project-folder>/spec/spec-<iteration-id>.md` for a later **Iteration**. Replace every bracketed
> placeholder. This template defines an investigation contract, not a software
> product specification.

> **Applicability.** Baseline specs use the complete required template. Later Iterations include only sections/fields needed for the approved Iteration Intent; unchanged approved questions, outputs, and evidence requirements carry forward without restatement or N/A filler. Metadata and read-only/access/data/safety controls remain required. New or changed questions/outputs require acceptance coverage. Replace placeholders in included content; omission does not remove an existing obligation.

## Metadata

- **Iteration ID:** [`baseline` for the baseline buildout, or the iteration's `Iteration-<YYYYMMDDTHHMMSSZ>-<token>`]
- **Specialization:** reverse-engineering
- **Depth level:** [1 | 2 | 3]
- **Discovery mode:** [Delegated | Interactive]
- **Target root:** [absolute or workspace-relative read root]
- **Artifact root:** [project folder that receives generated artifacts]
- **Target writable:** No (writes only to an approved nested artifact subtree, if any)
- **Remote operations:** [Prohibited | Read-only]
- **Confirmed date:** [YYYY-MM-DD]

## 1. Objective

[Why the target must be understood, which decisions the assessment must enable,
and what is explicitly not being implemented.]

## 2. Audiences and stakeholders

| ID | Audience or stakeholder | Need | Decision or task enabled |
|----|-------------------------|------|--------------------------|
| A-1 | [role] | [knowledge need] | [decision or task] |

## 3. Target and scope

### 3.1 In scope

- [repository, module, runtime, history range, documentation set, environment]

### 3.2 Out of scope

- [implementation, deployment, live data, inaccessible systems, unrelated area]

### 3.3 Target boundaries

List one row per target. A multi-repository or multi-service system has one row
per repository or service, each with its own revision and access. Record each
target's revision in the metadata or evidence so citations stay unambiguous.

| Target ID | Location | Revision | Access | Notes |
|-----------|----------|----------|--------|-------|
| T-1 | [path/URL] | [commit/version] | Read-only | [notes] |
| Generated artifacts | [path] | n/a | Read/write | [artifact root] |

## 4. Questions to answer

Each question MUST be answered by the assessment or explicitly closed as
Unknown.

- **Q-1:** [question]
- **Q-2:** [question]

## 5. Evidence contract

### 5.1 Evidence sources

| ID | Source | Scope | Access | Reliability considerations |
|----|--------|-------|--------|----------------------------|
| E-1 | [source] | [scope] | [read/static/runtime] | [staleness, completeness, provenance] |
| E-2 | Issue tracker / backlog (roadmap docs, `TODO`/`FIXME`, stubs, issues) | Planned / in-progress work | Read-only (authorize if remote) | May be inaccessible |

### 5.2 Claim states

| State | Required evidence |
|-------|-------------------|
| Verified | At least one primary citation. A runtime-behavior claim needs execution evidence; a static-only observation supports Verified only for the narrower static fact, with the behavioral claim recorded as Inferred or Unknown |
| Inferred | At least two independent evidence points and rationale |
| Contradicted | Citations to each conflicting source and impact |
| Unknown | Search scope, missing evidence, and resolution question |
| Proposed | Evidence, expected value, affected area, dependency, and risk |

### 5.3 Citation format

Cite with **repo-relative Markdown links** so they resolve in a viewer: display
`path:line`, target `<relative-path>#L<line>` (for example
`[src/app.go:42](../../src/app.go#L42)`; a range is `#L16-L42`). Use the path
relative to the assessment file — never an absolute filesystem path. Commit refs
use the short SHA; supplement unstable line numbers with a symbol name.
[Add any command-output, URL, or artifact citation conventions here.]

### 5.4 Sampling

| Area | Population | Sample rule | Minimum coverage | Exclusions |
|------|------------|-------------|------------------|------------|
| [history/tests/features/commands] | [population] | [selection method] | [number or percentage] | [exclusions] |

## 6. Access, data, and safety constraints

- **Allowed commands:** [read-only and isolated-copy command classes]
- **Prohibited commands/actions:** [target writes, remote writes, live data, destructive actions]
- **Network policy:** [prohibited/read-only/approval-gated destinations]
- **Data classes:** [public/internal/confidential/restricted]
- **PII/secrets handling:** [redaction and blocking rules]
- **Isolated validation strategy:** [throwaway copy/clone/container/none]
- **Retention:** [artifact retention and deletion]

## 7. Required outputs

| ID | Output | Canonical path | Required depth |
|----|--------|----------------|----------------|
| O-1 | Assessment entry point | `assessment/README.md` | [contents] |
| O-2 | Product assessment | `assessment/product.md` | [contents] |
| O-3 | Derived spec and use cases | `assessment/spec-and-use-cases.md` | [contents] |
| O-4 | User guide | `assessment/user-guide.md` | [contents] |
| O-5 | Architecture assessment | `assessment/architecture.md` | [contents] |
| O-6 | Design assessment | `assessment/design.md` | [contents] |
| O-7 | Engineering assessment | `assessment/engineering.md` | [contents] |
| O-8 | Build and run | `assessment/build-and-run.md` | [contents] |
| O-9 | Operations assessment | `assessment/operations.md` | [contents] |
| O-10 | Agentic assessment | `assessment/agentic.md` or N/A with rationale | [contents] |
| O-11 | Findings | `assessment/findings.md` | [contents] |
| O-12 | Backlog and next iteration | `assessment/backlog.md` | [contents] |
| O-13 | Evidence | `assessment/evidence.md` | [contents] |

## 8. Acceptance criteria

- **AC-1:** [criterion]
  - **Traces to:** [Q-<n>, O-<n>]
  - **Assessment method:** [method]
  - **Required evidence:** [artifact, command, sample, review]
  - **Pass condition:** [objective threshold]

---

## SPEC-EXIT validation checklist

For baselines, apply the full required shape. For later Iterations, retain metadata, boundary/safety, placeholder, and acceptance checks, but apply content-presence checks only to the approved intent. Verify inherited claim definitions, questions, outputs, or references in their approved artifacts when needed rather than copying them.

1. Metadata contains all nine fields; for a later Iteration the iteration ID matches the filename `<iteration-id>` and, when newly minted, matches the `Iteration-<YYYYMMDDTHHMMSSZ>-<token>` rule in core §4.3 (pre-existing legacy IDs remain valid); for the baseline buildout the Iteration ID is `baseline` and the spec is the unnumbered `spec.md`.
2. Target root and artifact root are distinct or an approved isolated
   subfolder is declared.
3. Baseline sections 1-8 are present and non-empty. Iteration specs populate only intent-relevant sections/fields.
4. Every question has a unique `Q-<n>` ID.
5. Every evidence source has a unique `E-<n>` ID.
6. All five claim states are defined.
7. Sampling states a numeric minimum or explicitly says exhaustive.
8. Read-only target confirmation, remote policy, network policy, data handling,
   and isolated validation are explicit.
9. Every output has a unique `O-<n>` ID and canonical location.
10. Every AC has a unique ID, valid traces, assessment method, evidence, and
    objective pass condition.
11. Every `Q-<n>` and `O-<n>` is traced by at least one AC.
12. No template placeholder remains.
13. The discovery transcript shows that Delegated/Interactive was put to the Human User and their explicit answer was recorded before Round 1. Metadata matches that answer; a silent default or Autopilot grant alone does not satisfy Discovery-mode selection.
