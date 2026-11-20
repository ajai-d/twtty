<!-- TWTTY template license notice: retain when reusing template material.
Copyright 2026 Ajai Peddapanga.
Licensed under Apache License 2.0: https://www.apache.org/licenses/LICENSE-2.0
Attribution: https://github.com/ajai-d/twtty/blob/main/NOTICE
This notice applies only to TWTTY template material, not independently authored
project content or the assessed system. Include the license and applicable
notices when redistributing TWTTY material.
Provided "AS IS", subject to Apache 2.0 warranty disclaimers and liability limits.
AI-generated outputs need validation; TWTTY does not guarantee security,
regulatory compliance or production suitability.
-->

# [Target name] Assessment

> Copy this file to `<project-folder>/assessment/README.md`. Replace every
> bracketed placeholder. Keep this file as the canonical entry point and link
> every assessment document, including any approved split documents.

- **Target:** [name]
- **Iteration:** [Iteration-<YYYYMMDDTHHMMSSZ>-<token>]
- **Target revision:** [commit/version/snapshot]
- **Depth:** [1 | 2 | 3]
- **Evidence cutoff:** [UTC timestamp]

## Executive summary

- What the target is
- Who it serves and the problems it solves
- Primary runtime and deployment shape
- Current maturity and material caveats
- Highest-priority findings and unknowns

## Scope and limitations

[Included and excluded target areas, evidence cutoff, access limitations, and
whether `agentic.md` applies.]

## High-level system view

[Evidence-backed context diagram and short explanation.]

## Reading paths

| Audience | Start with | Then read |
|----------|------------|-----------|
| [audience] | [document] | [documents] |

## Assessment contents

- [Product](product.md)
- [Derived spec and use cases](spec-and-use-cases.md)
- [User guide](user-guide.md)
- [Architecture](architecture.md)
- [Design](design.md)
- [Engineering](engineering.md)
- [Build and run](build-and-run.md)
- [Operations](operations.md)
- Agentic and AI behavior: [agentic.md](agentic.md) when the target is agentic;
  otherwise replace this bullet with `Agentic and AI behavior: N/A - [reason]`
  and do not create the file (a missing file must never be linked).
- [Findings](findings.md)
- [Backlog and next release](backlog.md)
- [Evidence](evidence.md), including the question-closure table for every `Q-<n>`

## Prior iterations

[Current iteration ID and links to any superseded assessments archived under
`history/<prior-iteration-id>/`. Omit for the baseline buildout.]

## Claim states

[Verified, Inferred, Contradicted, Unknown, and Proposed legend with a link to
`evidence.md`.]
