# TWTTY command dispatcher

A thin, uniform entry point for intent-driven TWTTY work. This file defines a small **command grammar** and maps each command to the matching flow in [`methodology/core-twtty-methodology.md`](./methodology/core-twtty-methodology.md). It is a **convention you paste into a fresh chat**, not an executable — there is no `twtty` binary.

## How to invoke

In a fresh session with your AI coding assistant, give it access to the
framework and project folders, then paste one line:

```text
Read "<full-path-to-twtty.md>" and run: <command>
```

Replace `<full-path-to-twtty.md>` with the absolute path to this `twtty.md`
file, including the filename, not just the repository or `framework` folder.
Keep the path in quotes, including when it contains spaces.

For example, with Windows paths:

```text
Read "C:\projects\twtty\framework\twtty.md" and run: twtty start project type=sdlc project="C:\projects\my-app"
```

## What the AI Agent MUST do on any `twtty` command

1. Read this dispatcher and the complete [`methodology/core-twtty-methodology.md`](./methodology/core-twtty-methodology.md) in full from the explicitly selected bootstrap tree and act strictly as the **AI Agent** it defines. For an existing project, perform only the bounded read-only lookup needed to identify its active specialization, then read that specialization and every methodology it explicitly inherits in full. At first contact, resolve the specialization from the supplied `type=` or obtain the missing Human selection before loading its complete methodology chain. Do not decide the command outcome or begin execution until this reading is complete.

   Read the required methodology files in full on every invocation. Truncated output, summaries, path resolution and prior-session memory do not satisfy this requirement. If required content cannot be read, report the blocker rather than proceeding from assumptions.

   In the normal opening response, identify the methodology files actually read, the selected framework source, its actual revision and any local modifications (or report revision unavailable). Use that framework tree throughout the invocation; do not substitute another checkout. Read applicable project-owned profiles and artifact templates when their procedures require them. Loading the framework does not upgrade the project's adopted configuration snapshots.

   On every command, treat the selected framework checkout as read-only during application work, per [core §4.5](./methodology/core-twtty-methodology.md#45-rules). Only an explicit Human User request for framework maintenance authorizes scoped changes to it; application approvals and Autopilot grants do not. Project-owned configuration and approved Handoff exports remain governed by their existing approvals.
2. Parse the whole command before mutation; accept exactly the four commands below, with no aliases or additional entrypoints. Reject unknown/duplicate keys, empty values, malformed quotes, unsupported commands and conflicting parameters with an actionable explanation pointing to the appropriate supported command. Reject removed spellings before mutation; do not silently normalize them into a supported command.
3. Resolve `type=<specialization>` (when present) to the specialization document at `methodology/specialized-implementations/<specialization>/<specialization>.md` and treat it as the **Active specialization**.
4. Treat `project=<path>` as the product repository root. Resolve the actual artifact root below; Core/specialization `<project-folder>` means that artifact root, not a second product root. New **non-execution TWTTY artifacts** — `seed/`, `spec/`, `plan/`, `replay-execution/`, and `twtty-runtime-config/` — normally go under **`<project>/twtty/`**. Preserve an existing project's actual artifact/config layout; onboarding is not permission to move it. EXECUTE-stage outputs (source, infrastructure, tests, CI config) go to their **natural repository locations outside `twtty/`**, regardless of artifact-root nesting.
5. Enter the mapped core procedure below. Resume enters **§4.1**, including operational preparation under §4.1.1 when needed; Handoff enters **§4.1.1**, not lifecycle continuation. Obtain every required Human User confirmation; skip no Approval Gate. `start project` establishes the first TWTTY baseline from an approved Project Seed, either for new software or an explicitly approved existing-code refactoring goal. Preserve existing source and do not reset an existing TWTTY lifecycle. Ordinary `start iteration` requires that Project Seed and verified completion of the initial baseline; no initial lifecycle may be skipped. An explicit production-incident request through that command uses the controlled incident routing below before ordinary Iteration creation, never a new Iteration ID or an invented completed baseline.

## Artifact-root resolution

The default root is `<project>/twtty/`; named lifecycles may use
`<project>/twtty/<specialization>/`. Preserve a verified legacy root in place.

1. Use explicit/current verified project references and bounded inspection of default,
   named and referenced legacy roots for seed/spec/log evidence. Recover each candidate's
   specialization from its own approved evidence. Normalize metadata `baseline SDLC`
   to `sdlc` for routing only; it is not an accepted command value. A named folder and
   recorded specialization must agree; conflicting evidence requires clarification.
2. Filter by supplied `type=` when accepted by the command, then use the exact root
   identified by consistent current branch/scope evidence or the sole compatible root.
   If several remain, ask for the exact artifact root; never choose the newest.
   An unclassified seed-only root can be confirmed at first contact, not silently
   assigned to an existing lifecycle. A supplied type cannot change an existing scope.
3. Only an explicit `start project` for a confirmed first baseline may establish a new
   root: use the default when no lifecycle exists, or an approved unused named root
   for an additional lifecycle. Missing logs on Resume never create a new baseline.
   Missing/ambiguous evidence on other lifecycle commands requires targeted recovery.
4. Announce product and selected artifact roots; keep them stable, never move artifacts,
   append `twtty/` again, reset lifecycle state or refill project config from shared defaults.

Handoff still does not accept `type=`. Preserve §4.1.1's explicitly approved source/history
selection, resolving each included root rather than silently narrowing a multi-root export.

## Commands

| Command | Purpose | Maps to | Required | Optional (default) |
|---|---|---|---|---|
| `twtty start project` | Begin the first TWTTY baseline from a Project Seed, building new software or refactoring existing code | core §4.2 | Resolve project and specialization before mutation | `project=`, `type=` |
| `twtty resume` | Continue or join an existing project, regardless of creator | core §4.1; SDLC §3.6 when preparation is needed | Resolve existing project | `project=`, `type=` |
| `twtty start iteration` | Begin a new feature, fix or improvement | core §4.3 | Resolve existing project | `project=`, `type=` |
| `twtty handoff` | Prepare an approved independent delivery | core §4.1.1 + SDLC §3.7 | Resolve source project | `project=` |

These are the **only four commands**. Team work pickup and production-incident handling
are intent-driven procedures within Resume and Start iteration, not extra commands or
parameters. No `deploy` or `checkpoint` argument is accepted.

Resume uses current branch/worktree and directly relevant saved progress. If the requested work is unclear, ask once; **do not automatically scan/rank all iterations, branches or PRs to infer a developer's assignment**. Work-pickup discovery below runs only when explicitly requested in the accompanying natural-language intent, for example "Find and recommend ready, unclaimed work for me." An existing selected assignment is continued by ordinary Resume, not replaced by discovery. Handoff and application preparation are supported by SDLC and its agentic/data extensions; Reverse Engineering keeps the investigated target read-only and reports unsupported operations.

## Parameters

- **`type=<specialization>`** — one of the shipped specialization slugs, each the folder name under `methodology/specialized-implementations/`: `sdlc`, `sdlc-for-agentic-apps`, `dataeng`, `reverse-engineering`. Resolve before `start project` mutates anything; ask if unresolved. For `start iteration` and `resume` recover it from the relevant project evidence per core §4.1; a supplied value MUST match. Handoff recovers it and does not accept `type=`.
- **`project=<path>`** — the **product root** itself (for example `my-app`). **Do NOT append `twtty/`.** Use an unambiguous supplied/current project context; otherwise ask before mutation. Quoted paths may contain spaces. New process artifacts use `<project>/twtty/` per [core §2](./methodology/core-twtty-methodology.md#2-artifacts-and-formats); preserve existing layouts. **EXECUTE** code, infrastructure, tests, and CI config remain at their natural repository locations.
- **Work-pickup scope is natural-language intent, not extra keys.** With an explicit Resume pickup request, the Human may name an existing Iteration or domain in the accompanying text. Apply those constraints before proposing eligible work; do not accept `iteration=` or `domain=` command parameters.
- **Seeds and intents are not command arguments.** Resolve paths from the **actual artifact root**, preserving existing layouts; `<project>/twtty/` is the default for new projects only. Every first TWTTY baseline requires `<artifact-root>/seed/seed.md`, including a baseline refactoring existing code. Every later Iteration reuses that approved Project Seed and requires its own approved Iteration Intent; neither can substitute for the other. Operational Resume preparation does not establish lifecycle approval. Verify initial baseline completion before generating an Iteration ID and writing `<artifact-root>/seed/intent-<iteration-id>.md`. Hotfix details are elicited by its controlled procedure, not command arguments.

## Explicit work pickup during Resume

Only when the Human explicitly requests finding/recommending unclaimed work with
`twtty resume`, the AI Agent MUST:

1. Recover project state and the active specialization per core §4.1. This
   procedure joins existing planned work; it MUST NOT create an Iteration or
   replace an existing assignment without explicit Human direction.
2. Verify that the specialization defines work items and a work-pickup flow.
   The shipped `sdlc` specialization and implementations extending it support
   this command; unsupported specializations stop with an explanation.
3. Find open Iterations whose `PLAN-EXIT` is approved and whose `EXECUTE-EXIT`
   is not approved, then apply any Iteration/domain constraints from the explicit
   request before reading candidate plans.
4. Read each candidate plan's work breakdown, dependency table, and Team
   collaboration guidance together with current state, replay evidence, branch
   logs, and remote pull requests, including the specialization's shared
   hotfix pause evidence. Use the state index and relevant tails; batch
   candidate reads and share the specialization's boundary-scoped metadata
   snapshot rather than repeat resolution or scan unrelated history.
5. Exclude paused Iterations and completed, already claimed, blocked, or
   footprint-colliding work. Identify each item and claim by
   `(Iteration ID, domain, work-item ID)`, including every item in a bundle.
   Rank the remaining work by satisfied dependencies, critical-path value,
   work unblocked, footprint isolation, independent testability, reviewable
   scope, and any Human User domain preference.
6. Present clickable choices with the recommended work item or coherent bundle
   first, alternatives grouped by domain, and a concise rationale for every
   proposal. If none is eligible, explain the blockers and create no branch.
7. Require the Human User to select the work, even under Autopilot. Immediately
   before claiming it, refresh remote state and re-check eligibility.
8. Delegate the selected claim to the specialization's branch topology:
   reuse an exclusive domain context for sequential work, and isolate concurrent
   contributors on separate branches/worktrees. No branch per work item.
   Shared contributor pickup publishes a draft change request as the claim;
   its body and branch-opening entry agree on scope, domain, items, branch log
   and receiving working target. Internal orchestrated workers may reuse the
   parent claim with recorded dispatch; routine worker merges need no extra
   approval/PR where target policy permits. Never run concurrent writers on
   one branch or checkout or bypass protected-target controls. After opening
   it, refresh remote claims and pauses; if another claim won
   the race, close the later claim using the specialization's abandonment
   procedure and refresh the proposals. If the scope became paused, report it
   and do not begin work. Waiting for eligibility or another developer MUST
   NOT become an unbounded polling loop; remote failures use existing finite
   retries, then Escalate with the next required action.

## Production-incident routing on Start iteration

When `twtty start iteration` is accompanied by an explicit urgent production-incident
request, route before ordinary Iteration creation. Do not generate an Iteration ID,
create its intent or reset existing work. The AI Agent MUST:

1. Recover the project state, active specialization, inherited risk level, and
   active Iteration per core §4.1.
2. Verify that the active specialization defines a Hotfix path. The shipped
   `sdlc` specialization defines it at
   [SDLC §3.5](./methodology/specialized-implementations/sdlc/sdlc.md#35-hotfix-path-production-incident-fast-path);
   `sdlc-for-agentic-apps` inherits that path. If the active specialization does
   not define one, stop and explain that the command is unsupported.
3. Interactively collect the production environment, observed symptom, and
   urgency, then verify that the request is a confirmed production incident
   rather than ordinary feature or fix work.
4. Request explicit Human User approval to open the Hotfix Scope, even under
   Autopilot. Only after approval may the AI Agent create the specialization's
   incident/log/pause artifacts in one commit and publish the draft hotfix PR
   indexing that approval evidence. Opening completes only when both are
   remotely discoverable. A partial opening MUST Escalate rather than resume
   the Iteration.

Ordinary feature/fix intent continues through core §4.3's full lifecycle.
Ambiguous incident intent needs clarification, not an automatic fast path. Existing
Hotfix Scopes continue through ordinary Resume with their pause/recovery safeguards;
removing a command never renames their IDs, rewrites history or abandons a pause.

## Notes

- This grammar is **sugar over the bootstrap prompt** core §4.1 already defines ("point the AI Agent at this document, name the project folder, and state the intent"). It changes no stage, gate, or approval rule.
- `twtty resume` normally continues the work already active in the named branch or worktree. It discovers new planned work only on an explicit pickup request; after a successful claim, later sessions resume that selected context without reacquiring work.
- Specialization is selected by `type=`, not by a Discovery-time routing question. The Spec Agent still records the resolved specialization in the spec's `## Metadata` `Specialization` field exactly as the active specialization document requires.
- Every iteration — including the baseline one created by `start project` — runs the full `SEED → SPEC → PLAN → EXECUTE` loop; `SEED` stays Interactive.
