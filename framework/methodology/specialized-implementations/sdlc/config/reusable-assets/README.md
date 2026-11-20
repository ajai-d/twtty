# Reusable assets

**Category:** `reusable-assets` · Reusable material a project pulls in — **loadable
capability** (skills now; MCP servers / hooks / prompts later) and **reference guidance**
(best-practices), **never authority**: nothing here changes a `risk-calibration` control or
any gate.

## Subfolders

| Subfolder | Holds | Status |
|-----------|-------|--------|
| `skills/` | Reusable skills loaded on demand — **library skills** (shipped or external, e.g. a UX skill) or **project-captured skills** the AI Agent authors itself (see [Project-captured skills](#project-captured-skills)) | active |
| `best-practices/` | Best-practice guidance bundles consulted at PLAN/EXECUTE — SHOULD-level craft guidance and pointers to published material (e.g. the Azure Well-Architected assessments) | active |
| `mcp-servers/` | Portable MCP server bindings (external tools / data / alternate models) | future |
| `hooks/` | Portable hooks (deterministic commands at agent-loop points) | future |
| `prompts/` | Reusable prompt files invoked as slash commands | future |

Only `skills/` is populated in the first pass; the others are reserved so the structure is
stable as portable assets are added.

## How bindings are selected

Point `runtimeconfig.md` → `reusable-assets.skills` at a **skills directory** (default: this
folder's `skills/`):

```yaml
reusable-assets:
  skills: reusable-assets/skills/   # directory; "" = no skills
```

The agent **inspects every skill file in that directory and applies the ones that are
applicable** — skills are not named individually. Each skill file describes its own capability
and when it is relevant. A skill adds **capability, never authority** — applying (or not
applying) one never changes a `risk-calibration` control or any gate — so the binding stays
**loosely coupled**: point at the directory, and the agent uses whichever skills fit the work
in scope.

`best-practices/` lives in this folder but binds through its **own** top-level
`best-practices:` key (e.g. `best-practices: reusable-assets/best-practices/bestpractices-profile1.md`);
the `reusable-assets:` map covers only the loadable surfaces (skills now; mcp-servers / hooks /
prompts later).

## Trust-boundary rule

Any asset that crosses a trust boundary (MCP servers, hooks, or a skill that fetches remote
content) MUST be **version-pinned and provenance-verified before install**, per the active
`risk-calibration` security controls. The bound `harness` documents *how* each surface is
configured; this folder holds the *portable* asset definitions.

## Project-captured skills

Skills have two origins:

- **Library skills** — shipped here or sourced externally (e.g. the UX skill
  [`skills/impeccable.md`](skills/impeccable.md)), bound as above. One that crosses a trust
  boundary (external install, remote fetch) follows the trust-boundary rule above.
- **Project-captured skills** — the AI Agent authors these itself, as it works, from prompts it
  has already run. This is how a project **grows its own** reusable prompts, so later Iterations
  and resumes reuse them instead of re-deriving the same work. A captured skill is just a
  reusable prompt for a specific recurring task.

**Where they live.** A project that captures skills points `runtimeconfig.md` →
`reusable-assets.skills` at its **own** directory under
`<project-folder>/twtty-runtime-config/reusable-assets/skills/` (the standard override
location) and the AI Agent writes captured skill files there, one `.md` per skill. They are
inspected and applied by the same loosely-coupled "inspect the directory, apply what fits" rule
as any other skill — so no new loading mechanism is introduced.

**The AI Agent decides, dynamically, what becomes a skill.** There is no per-prompt ceremony. As
it works, the AI Agent uses its own judgement to recognize when a prompt it just ran is a
reusable pattern — the same task is likely to recur on similar inputs — and only then distills
it into a skill file. One-off or highly situation-specific prompts are NOT promoted. The AI Agent
SHOULD briefly tell the Human User when it captures or refines a skill; it does not gate the
flow.

**Recommended captured-skill file shape.** Like any skill file, it describes its own capability
and when it is relevant; for a captured prompt that means, at minimum: `id`, `name`, `version`,
`status` (`active` | `deprecated`); **When to use** (the task / trigger it serves); **Applies
to** (stage and stage-task); **Inputs** (named parameters); **Prompt** (the parameterized body,
every variable a named placeholder); **Expected outputs**.

**Keep the library small and sharp — skills MUST reduce work, not add bulk.** The AI Agent MUST
refine an existing skill rather than add a near-duplicate (consolidating overlaps), promote only
prompts with demonstrated or clearly likely reuse, keep each skill to the minimal parameterized
prompt plus its metadata, and deprecate (or delete) skills that no longer apply — a deprecated
skill is not applied. The directory SHOULD stay small enough to scan in full; growth past a
handful of skills is a signal to consolidate.

**Use skills to cut work — especially on resume.** The inspect-and-apply rule above already runs
at each stage; on **resume** it is part of how the AI Agent re-establishes how recurring work is
done, so it reuses an applicable captured skill instead of re-deriving an equivalent prompt or
repeating equivalent analysis.

**No replay-log coupling.** A project-captured skill is a local prompt template that crosses no
trust boundary, so — unlike an external install under the trust-boundary rule — capturing or
using it produces **no replay-log entry**. The skills directory and its version-control history
are the record.

**Redaction.** A captured skill is a template and MUST be generic: it MUST contain no secrets or
identifiable data (names, usernames, emails, IDs, hostnames, customer/tenant identifiers, and the
like); variable content lives in parameters, never hard-coded values.

## License and disclaimer

Copyright 2026 Ajai Peddapanga. TWTTY material in this file is licensed under
[Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0); see TWTTY's
[NOTICE](https://github.com/ajai-d/twtty/blob/main/NOTICE). Independently authored
project content retains its own ownership and license. Include the license and
applicable notices when redistributing TWTTY material.

Provided "AS IS", subject to the license's warranty disclaimers and liability
limitations. AI-generated outputs may be incorrect or unsafe; validate results
before use. TWTTY does not guarantee security, regulatory compliance or production
suitability.
