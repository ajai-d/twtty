# Harness binding — GitHub Copilot

**Category:** `harness` · **Status:** reference (set active in `runtimeconfig.md`)

## What this binds

The agentic coding tool that **plays the agent roles** across SEED → SPEC → PLAN →
EXECUTE. This is the default reference harness for the baseline SDLC specialization.

## Runtime modes

| Runtime | Recommended for | Notes |
|---------|-----------------|-------|
| **[GitHub Copilot in VS Code](https://code.visualstudio.com/docs/agents/run/chat-view)** | Coding alongside the editor (recommended default) | Select **Agent** in the Chat view; review inline diffs and approve tool use alongside your code. |
| **[VS Code Agents Window](https://code.visualstudio.com/docs/agents/run/agents-window)** | Coordinating project-based agent sessions | Use a session with access to framework/project files, required tools, and approval interactions. |
| **[GitHub Copilot app](https://docs.github.com/en/copilot/concepts/copilot-surfaces/github-copilot-app)** | Desktop project sessions | Connect a repository or local folder. Required tool, approval, and review-isolation capabilities must be available; unsupported controls MUST be surfaced. |
| **[GitHub Copilot CLI](https://docs.github.com/en/copilot/concepts/copilot-surfaces/copilot-cli)** | Terminal-based coding and operations | Supports interactive and programmatic sessions; required approval and review controls still apply. |

Each agent in the pipeline is a **role** played by the chosen runtime. Context-isolation
requirements per risk level come from the active `risk-calibration` binding, not from the
harness.

## Model and model-escalation

- **Model:** the Human User selects the runtime's model during the config interview; the
  AI Agent records the choice in `runtimeconfig.md`. If unspecified, the AI Agent uses the
  runtime's current default model and notes it.
- **Model-escalation policy:** a harness MAY run a cheaper model for routine work and
  escalate to a stronger model when a gate check fails, a self-review finds a defect, or a
  task exceeds a complexity threshold. Escalation events are recorded in the replay log.
  Build-cost impact is bounded by the active build budget.
- **Routine execution profile:** within the Human User's approved model policy, the AI
  Agent SHOULD use the routine reasoning profile for bounded implementation, command
  execution, status checks, documentation, and known-error corrections. Deeper reasoning
  SHOULD be reserved for architecture decisions, unresolved ambiguity, consequential
  changes, or failed verification requiring substantive diagnosis. Profile selection
  SHOULD NOT require a separate planning turn. Where the harness cannot select profiles,
  the AI Agent MUST NOT claim that it changed them; it uses the configured runtime profile
  and surfaces any needed adjustment to the Human User. Required gate checks and review
  independence remain unchanged.

## Customization surfaces

The harness configures these on the Human User's behalf (the default agent as
orchestrator). Trust-boundary surfaces (MCP servers, hooks) MUST be **version-pinned and
provenance-verified before install** per the active `risk-calibration`'s security controls.

| Surface | When configured | Purpose |
|---------|-----------------|---------|
| **Repo-wide instructions** | Setup (iteration-level) | Always-on baseline every agent reads: TWTTY conventions, stage/gate names, replay-log rules, project context. |
| **Pattern-scoped instructions** | JIT during implementation | Instructions applied only to files matching a supported pattern. |
| **Custom agents** | Setup (predicted roles) + JIT (surprises) | Named persona with its own instructions, tools, and model; fulfills a stage-task ROLE. |
| **Skills** | JIT during EXECUTE | Reusable capability any agent loads on demand (portable skills are bound separately). |
| **MCP servers** | Setup (foundational) + JIT (iteration-scoped) | Connects agents to external tools, data, or alternate models. **Ask before configuring** — crosses a trust boundary; version-pin + provenance-verify. |
| **Prompt files** | JIT during EXECUTE | Reusable prompt invoked as a slash command. |
| **Hooks** *(advanced)* | Setup (before commits/edits) | Deterministic command at agent-loop key points (format-on-edit, block-risky-commands). **Ask before configuring** — can execute shell commands; version-pin + provenance-verify. |
| **Delegate** | — (runtime command) | Hands off a fully specified `W-<n>` to the GitHub Copilot Coding Agent (cloud, async) for branch-to-PR execution. |

Configuration specifics (file paths, frontmatter fields, feature names, settings) evolve
independently and are the AI Agent's responsibility to look up in current Copilot
documentation.

## How this harness satisfies the TWTTY contract

| Required control | How GitHub Copilot meets it | Escalate if |
|------------------|-----------------------------|-------------|
| **Attributable commits and authorization** | Native Git/platform metadata attributes actual commits; AI-executed commits are not Human-authored anchors. Autopilot evidence follows SDLC §5.1: L1 accepts the original direct native Human chat/confirmation; stronger levels/policies retain their required Human-authored commit/approval evidence. | Required approval origin, scope, current caller/context or stronger native evidence cannot be verified; obtain the permitted native confirmation, never invent a Human commit. |
| **Reviewed / isolated merge** | Reviewer role can run as a separate custom agent in an isolated context (required at L4+ by the active `risk-calibration`). | The runtime cannot provide an isolated reviewer context where the risk level requires it. |
| **Independent verification** | Reuse required native application CI/reviews and Git/platform history; inspect methodology artifacts directly, without custom validators. | Required external policy controls cannot be satisfied. |
| **Escalation destination** | Surfaces gate requests and `Escalate` in-IDE / in the PR per the `escalation` key. | No configured escalation channel is reachable. |

## Stage hooks

- **SEED / SPEC / PLAN:** plays the Seed/Spec/Planning Agent roles; produces artifacts.
- **EXECUTE:** plays implementer, code-review, code-scanning, security, and test roles
  (Sequential), or dispatches subagents (Parallel, cap from `concurrency-cap`).
