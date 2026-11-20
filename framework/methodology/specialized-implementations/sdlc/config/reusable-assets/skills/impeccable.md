# Skill — Impeccable (UX / UI)

**Category:** `reusable-assets/skills` · **Status:** reference (present in the bound `reusable-assets.skills` directory) · **Source:** [impeccable.style](https://impeccable.style) · [`pbakaus/impeccable`](https://github.com/pbakaus/impeccable)

## What this binds

[Impeccable](https://impeccable.style) — an external, harness-installed **design skill** for AI
coding agents (one skill, `/impeccable <command>` commands, plus deterministic frontend
detector rules). It gives the agent a shared UI/UX design vocabulary and objective
design-quality checks. Unlike a self-contained local skill, this file is a **pointer to an
external toolset**: the capability is installed into the bound harness from npm, not stored
here. It supports common harnesses (GitHub Copilot, Claude, Cursor, Gemini).

## When it loads (UI work only)

Applies only when UX/UI is in scope (spec UX mode ≠ `N/A`):

- **PLAN UX design** — `/impeccable init` (one-time: record durable product truth in
  `PRODUCT.md`; `/impeccable document` captures an existing design system in `DESIGN.md`) and
  `/impeccable shape` (plan UX/UI before code).
- **EXECUTE UI** — `/impeccable craft` (shape-then-build with visual iteration), then
  `/impeccable polish`, `/impeccable critique` (UX review), and `/impeccable audit`
  (accessibility / performance / responsive checks) to keep the build aligned with the chosen
  design system and the spec's accessibility target.

## Install (trust-boundary surface — consent + provenance + version-pin REQUIRED)

Impeccable installs an external package that writes command/skill files into the bound harness,
so it **crosses a trust boundary**. The active `risk-calibration` security controls require any
trust-boundary customization surface to be **version-pinned and provenance-verified before
install**. Accordingly, before installing it the AI Agent MUST **ask the Human User**, MUST
**pin a specific reviewed version**, and MUST record the install (package + version) in the
replay-execution log.

1. From the project root, install a pinned version — look up the current version first (e.g.
   `npm view impeccable version`): `npx impeccable@<pinned-version> install`
   (optionally `--providers=<harness> --scope=project`).
2. Initialize once: `/impeccable init` (writes `PRODUCT.md`).
3. Requires Node.js 18+.

(Exact commands and provider flags evolve upstream; the agent looks them up in the current
[Impeccable docs](https://impeccable.style) rather than relying on fixed values here.)

## Contract notes

- A skill adds **capability, not authority**: Impeccable does not change any `risk-calibration`
  control or any gate. UX obligations still come from the spec's UX requirements and the plan's
  UX design — Impeccable helps the agent *meet* them, it never relaxes them.
- **Deterministic detectors are verifiable evidence.** Impeccable's detector rules run via its
  CLI/extension with **no LLM and no API key**, so the agent MAY run them as objective,
  repeatable design-quality checks (e.g. within `/impeccable audit`) and cite the output as a
  build-time-verifiable signal rather than a subjective claim.
- If the harness cannot install or run it, the agent proposes another Human-approved,
  version-pinned, provenance-verified design skill that satisfies the selected UX controls.
  If no bound skill can satisfy them, `Escalate`; do not silently replace the required
  authored skill process with an unbound design-system proposal.

## How the AI Agent uses this file

Inspecting the bound `reusable-assets.skills` directory, the agent finds this pointer and —
only when UI work is in scope and after Human-User consent — installs pinned Impeccable, runs
`/impeccable init`, and applies the stage-mapped commands above. Absent any UX scope, it skips
the skill. Without consent or runtime support, follow the alternative-skill or `Escalate`
path above; do not substitute an unbound design-system proposal.
