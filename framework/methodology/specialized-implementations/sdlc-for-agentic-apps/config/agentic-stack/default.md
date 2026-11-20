# Agentic stack binding — Microsoft Agent Framework with Azure model access

**Category:** `agentic-stack` · **Status:** default (confirm per iteration during Architecture `2a`, recorded in `plan.md §1.5`)

## What this binds

The **agentic runtime stack** for an `sdlc-for-agentic-apps` project: the agent
framework/SDK, the model platform, the default model, the orchestration pattern,
the tool/integration ecosystem, and tracing/guardrail tooling. This is the
*agentic* counterpart to the baseline [`cloud`](../../../sdlc/config/cloud/) binding
(which maps identity/IaC/registry/deploy). The `cloud` binding still governs **how**
the model endpoint is provisioned and authenticated (developer Entra locally, Managed Identity when hosted; no keys);
this binding governs **what** agent framework, platform, and model are used.

The AI Agent MUST verify current product names, SDK packages, and versions in
Microsoft documentation at adoption time (the currency rule in
[sdlc.md §3.3](../../../sdlc/sdlc.md#33-plan) / [sdlc-for-agentic-apps.md §3.2](../../sdlc-for-agentic-apps.md#32-plan-delta-plan2a-plan2c));
the mappings below name the chosen products, not pinned versions.

**Version & API-surface drift is a deploy-time risk, not only a PLAN-time one.** A bound
model *version* can be **deprecated for new deployments** between authoring and deploy, and
the framework's **client/agent construction API can change** across SDK releases. The AI
Agent MUST therefore use the actual approved dependency set and provider feedback during
setup/deployment, reusing valid compatibility information rather than a blanket preflight:

- **Preserve the approved model/version/region.** Query missing capability information only
  when needed, or diagnose an actual provider failure. If the approved deployment is
  unavailable, propose a compatible replacement and surface material model/version,
  behavior or cost changes for the existing approval/refinement process once. Do not
  silently repin or rebuild PLAN for an in-scope API/parameter-representation correction.
- **The installed SDK's client/agent API matches the code**, and the dependency set
  **resolves** within approved manifests/locks. Select only the core and chosen-provider
  packages needed by the app, not an all-provider umbrella/meta-package. Verify the actual
  installed API when implementing it; SDK construction is not a model-provisioning
  prerequisite. A material dependency change needs its applicable approval.

Prefer compatible existing model access before creating infrastructure. For simple
inference, default to local agent orchestration with a direct Azure OpenAI resource client;
use the appropriate Foundry client when reusing an approved project endpoint or when
project-scoped features are actually needed. Do not create a new resource merely to
preserve a default client choice. Do not select project/hosted-agent creation skills or
their full starter workflows solely because the app uses AI. Confirm capability, identity
and data requirements in PLAN; select the concrete compatible endpoint/client at infra
kickoff within that approved design. Existing adopted choices require approved refinement,
not silent migration or model substitution.

## Stack mapping (capability → choice)

| Agentic capability | Default choice |
|--------------------|----------------|
| Agent framework / SDK | **Microsoft Agent Framework** (the unified Microsoft agent SDK for Python/.NET; supersedes and converges Semantic Kernel + AutoGen) |
| Model platform / hosting | **Azure model deployment with direct resource-level inference by default**; reuse a compatible Foundry project when selected, and add project/managed-agent infrastructure only for approved features that need it |
| Default model | **`gpt-4.1-mini`** (a Foundry / Azure OpenAI model deployment) — confirm per project and **verify the specific version is currently deployable in the target region** (model versions deprecate); swap for a larger model when quality requires |
| Orchestration pattern | **Single-agent** by default; multi-agent / workflow orchestration via Microsoft Agent Framework when the iteration needs it |
| Tool / integration ecosystem | **In-process function tools** for local app data where sufficient; **MCP** integrations only when required and approved |
| Tracing / observability | **OpenTelemetry/application usage evidence**, with privacy filtering; provision a remote tracing backend only when required |
| Guardrails / safety | **Application validation and framework middleware**, plus applicable provider controls, realizing §12; an additional safety service needs an approved requirement |

## How this satisfies the TWTTY contract

| Required control | How this stack meets it | Escalate if |
|------------------|-------------------------|-------------|
| App-runtime model auth with no keys | The shared client uses developer Entra locally and **Managed Identity** when hosted per [`cloud/azure.md`](../../../sdlc/config/cloud/azure.md); no API keys | Required token audience/scope, permissions or endpoint access cannot be verified |
| Evaluation of non-deterministic behavior | L1 normal-app smoke by default; required/selected formal evaluations implement §10 through an applicable harness/provider, with actual evidence | The bound tooling cannot produce the evidence required by the level/approved scope |
| Cost metering | Framework/Foundry token-usage telemetry feeds the `spec.md §11` cost budget and usage-evidence artifact | Token usage cannot be measured for the §11 budget |

## Stage hooks

- **PLAN (2a Architecture):** the agentic technology proposal
  ([sdlc-for-agentic-apps.md §3.2](../../sdlc-for-agentic-apps.md#32-plan-delta-plan2a-plan2c))
  **starts from this bound stack**; the Architecture Agent confirms the framework,
  platform, and model with the Human User (who may override), and records the
  resolved stack in `plan.md §1.5`.
- **EXECUTE:** agent behavior is built on the bound framework; the model is accessed
  through its Foundry/AOAI deployment using developer Entra locally or hosted Managed Identity (no keys), per
  the `cloud` binding; tracing and guardrails are wired per the mapping above.
