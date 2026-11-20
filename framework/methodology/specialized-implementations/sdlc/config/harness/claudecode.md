# Harness binding — Claude Code

**Category:** `harness` · **Status:** reference (set active in `runtimeconfig.md`)

## What this binds

An alternative agentic coding harness that plays the agent roles across SEED → SPEC → PLAN
→ EXECUTE. Swapping `harness: harness/claudecode.md` into `runtimeconfig.md` runs the same
methodology on Claude Code instead of GitHub Copilot.

## Runtime modes

| Runtime | Recommended for | Notes |
|---------|-----------------|-------|
| **Claude Code (terminal)** | Code-heavy and ops work | Agentic terminal; strong multi-file editing and tool use. |
| **IDE integration** | In-editor review flow | Inline diffs and approvals where supported. |

Each agent in the pipeline is a role played by the chosen runtime. Context-isolation
requirements per risk level come from the active `risk-calibration` binding.

## Model and model-escalation

- **Model:** selected during the config interview and recorded in `runtimeconfig.md`;
  defaults to the runtime's current default model if unspecified.
- **Model-escalation:** MAY run a cheaper model for routine work and escalate to a stronger
  model on gate-check failure, self-review defect, or complexity threshold; escalations are
  logged and bounded by the active build budget.

## Customization surfaces

Claude Code exposes its own equivalents of the TWTTY-used surfaces — project/system
instructions, subagents, skills, MCP servers, slash-command prompts, and hooks. The AI
Agent maps the generic surfaces to the harness's current mechanism (look up current Claude
Code documentation). Trust-boundary surfaces (MCP servers, hooks) MUST be version-pinned
and provenance-verified before install per the active `risk-calibration`.

## How this harness satisfies the TWTTY contract

| Required control | How Claude Code meets it | Escalate if |
|------------------|--------------------------|-------------|
| **Attributable commits and authorization** | Native Git attributes actual commits; AI-executed commits are not Human-authored anchors. Follow SDLC §5.1: original direct native Human approval at L1; required Human-authored commit/approval evidence at stronger levels/policies. | Required native approval origin, scope or current-context applicability cannot be verified; never fabricate a Human anchor |
| **Reviewed / isolated merge** | Reviewer role runs as a separate subagent in an isolated context (required at L4+) | No isolated reviewer context where the risk level requires it |
| **Independent verification** | Reuse required native application CI/reviews and Git/platform history; inspect methodology artifacts directly, without custom validators | Required external policy controls cannot be satisfied |
| **Escalation destination** | Surfaces gate requests / `Escalate` per the `escalation` key | No configured escalation channel reachable |

## Stage hooks

- **SEED/SPEC/PLAN:** plays the Seed/Spec/Planning Agent roles; produces artifacts.
- **EXECUTE:** plays implementer/review/scan/security/test roles (Sequential) or dispatches
  subagents (Parallel, cap from `concurrency-cap`).
