# Development and delivery profile

**Category:** `development`; **Status:** default SDLC profile, inherited by its agentic/data extensions

This project-owned profile configures execution and repository assets; it is not an application implementation or permission to mutate infrastructure. Copy it with the complete config tree during Discovery. Existing projects adopt it only through an approved configuration update, never silent fallback.

```yaml
local-execution: native
ci: required
cd: disabled
integration-branch: main
infra-root: infra/environments
local-environment: local
cloud-environments: []
local-compose: infra/environments/local/compose.yaml
container-checkpoint: when-container-delivery-applies
evaluation-recipe: shared-application-engine
```

Values are defaults, not immutable prescriptions. Resolve approved project choices in the copied profile, keep `runtimeconfig.md` pointing at it, and record changes in `meta/config`. Repository paths above resolve from the product root; they are not configuration-file fallbacks. Record the actual versioned recipe paths/inputs when authored during EXECUTE. A referenced recipe must exist and pass its own checks before use; a configuration placeholder is not working tooling.

`local-compose` is the conventional location when Compose services are needed, not an instruction to create them. Resolve it to `none` when the approved plan needs no services. Record container-checkpoint applicability from the approved scope, not from cloud-hosting selection alone. Do not omit explicitly requested emulator/container checks or add unnecessary ones. Listing an environment/path does not create resources or prove a recipe exists.

`evaluation-recipe` identifies the shared engine only when formal evaluations are
selected or required by the active risk/policy controls. Its presence does not opt L1
into an evaluation harness, dataset, scoring report or extra install.

## Policy ownership

This profile is the authoritative reusable development procedure, selected through the
existing `development` binding. SDLC retains lifecycle/task contracts, gates and
[branching/concurrency safeguards](../../sdlc.md#51-execution-mode-and-execution-pattern);
this profile cannot waive them or grant permission.
PLAN references the bound profile and records app-specific technologies, services,
configuration approach, work dependencies and collaboration groups, not a copy of this
procedure. Defaults here are conventions; concrete paths/designs must agree with the
effective project configuration. Native manifests/locks and existing setup/run recipes
hold the implemented requirements. Do not add a separate requirements inventory,
setup-state file or connection-settings area to TWTTY configuration.
Runtime uses the approved project-owned profile, not newer shared-library defaults.

## Discovery and configuration

In the existing SPEC Discovery/config interview for a new development project, explain:

| User-facing outcome | Contract |
|---|---|
| **Develop and test locally, with CI protecting main** (default) | Native inner loop, project-owned services, applicable scans/tests/evaluations and container checks; shared CI/review before normal merge; no application CD |
| **Develop locally and deploy to cloud through CI/CD** | The same local work and CI, plus approved infrastructure/application CD and deployed acceptance |

Confirm already-clear intent briefly rather than repeating the interview. New iterations revisit only missing/changed delivery requirements; Resume and team clones reuse valid settings. Azure services used by a local app do not imply cloud application hosting. Read-only assessment has no application deployment choice.

Resolve three independent decisions during Discovery: the provider/services the app needs; where the application runs; and which environment owns each infrastructure change. Disclose proposed local substitutes, real-service dependencies, emulator/container applicability and ownership in either Discovery mode. Record the approved outcome in project-owned configuration and SPEC; PLAN supplies concrete infrastructure paths and work. `Runtime target: N/A` means no cloud application hosting, not the `cloud: none` service binding. `cloud-environments` lists only selected shared cloud stages, never a stage inferred merely from an Azure dependency.

Prefer credible local substitutes only where they satisfy the approved scope; do not
invent elaborate emulation or new abstraction layers to avoid every cloud dependency.
A development-cloud dependency needs a necessity rationale and explicit current-scope
approval: isolated development resources, least-privilege access, non-production data
and cost limits or an explicit no-cap decision.

CI is configured/reused once per development repository with owner authorization. The workflow's actual required check names, branch protection/rulesets and review controls must agree; a pipeline alone does not protect main. CI may run without CD. Local work and PR creation remain possible during setup, but normal merge waits for required checks. CI-free merge is an explicit policy-permitted exception, not the default; never disable protections or report nonexistent checks as green.

CD stays disabled unless requested/configured. Offer cloud CD at verified local-delivery closeout when absent and appropriate, not at every developer invocation. Reuse existing CI. Extending active work requires applicable SPEC/PLAN refinement; adding delivery after a closed scope is a new iteration. Handoff remains a separate optional operation, not a reason to create another development iteration.

Personal secrets, identities, ports/project-instance values and credentials stay in ignored local settings/approved stores. Shared CI/CD settings change only as part of approved work, not merely because someone runs locally.

Branch topology, pattern authorization and worker integration follow
[SDLC §5.1](../../sdlc.md#51-execution-mode-and-execution-pattern), not work-item count.
Required CI/review controls still apply to publication; this is not a CI-free merge exception.

## Developer workstation inner loop

Use repository-native recipes and existing stage tasks:

1. Reuse the authorized working context; domain or parallel branches follow SDLC §5.1, not work-item count. Shared contributor pickup retains its visible claim.
2. Identify required software/packages from the selected task's project files and approved plan under [requirements and dependencies](#requirements-and-dependencies).
3. Reuse compatible installed tools; prepare only the missing approved tools/packages needed by the next operation. Infra/emulator prerequisites come before those services; app-only restores come before app work, not before unrelated provisioning.
4. Complete [development infrastructure first](#development-infrastructure-first), sequentially after dependency setup and before app/evaluation-harness implementation. Reuse ready services; create/start only needed dependencies and save app connection settings.
5. Prepare only required/selected verification and safety assets or source/sink contracts, then implement the app. Use edit -> applicable build/verification -> local run/debug -> repeat with native hot reload.
6. Run the normal app against its selected services for real connection evidence and complete applicable functional/integration, quality, safety and evaluation checks. Do not substitute mocks for a required real-service path.
7. Build/scan/run/test the container image before the PR or when packaging/runtime changes, **only where containerized delivery applies**.
8. Review and publish through the authorized direct or domain/scope PR process; required shared CI/review gates integration. Worker branches merge back to their working target, not directly to protected main.

Independent checks can run concurrently. Do not rebuild an image or run every full suite on every edit; complete due broader gates and reuse evidence only while its effective inputs match.

### Requirements and dependencies

For new work, Resume and each isolated worker, use this same sequence once for the
selected task, refreshing only affected inputs when they change:

1. Read relevant manifests/lockfiles, runtime/package-manager version declarations and
   existing setup/run recipes. CI and Dockerfiles supply additional execution-context
   requirements. Use the approved plan/config for intended choices or when a new app has
   no manifests yet; do not infer requirements from a prior conversation or a full machine
   inventory. Conflicting declarations require one focused resolution, not guessed versions.
2. For a new app, author minimal approved manifests/version declarations, then let the
   native package manager generate locks during its initial resolve/restore. Do not
   handwrite lockfiles or add a redundant lock-only/install cycle. This is `3a` setup
   support, not feature or eval-harness implementation or another planning stage.
   Existing apps keep their approved manifests/locks and use the native locked restore.
   Resolve only the immediate operation's dependencies here; do not put the entire app,
   frontend, browser or evaluation toolchain on the infrastructure critical path.
3. Compare those requirements with tools, packages and supported caches in the actual
   execution context. Reuse compatible tools and valid covering approvals. Use native
   package managers to restore missing locked packages; obtain required approval only
   for uncovered installs/downloads. A missing checkout environment does not mean Python,
   Node or other machine tools need reinstalling.
4. Continue to infrastructure preparation only after its required tools/packages are
   available. Defer unrelated app-only restores until before app/worker work. Do not
   require an app build, test suite, app CI or evaluation harness as
   proof of dependency readiness. Normal package-manager results and required version
   checks suffice; do not generate a dependency-detector or validation script.

On Resume, unchanged applicable declarations, inventory, grants, services and config are
reused. Prepare only missing inputs for the selected next task; do not repeat Discovery,
recreate infrastructure or restore packages after every edit. Actual access/feed/TLS
failures follow bounded recovery, not an assumption that software is absent.
PLAN's interactive UI prototype may need its own approved design/runtime packages earlier;
that stage-specific preparation does not authorize app feature implementation.

### Development infrastructure first

After PLAN approval and required dependency preparation, prepare development infrastructure
sequentially before app/evaluation-harness implementation. "Infra first" means before app
implementation, not before required software/packages. App build/tests/CI are not infra
prerequisites. This ordering also applies when Parallel was selected for later app work.

Perform initial infra preparation and save connection settings in the
[common working context](../../sdlc.md#51-execution-mode-and-execution-pattern).
Only afterward derive needed app-domain/parallel branches from that prepared base.

For local emulators/databases/queues, reuse project-owned settings/instances or prepare
only the approved support services using installed software or approved prebuilt images.
Do not build the unfinished app, invent emulators, replace required real services or
recreate existing data/volumes. Independent approved local preparation need not wait for
an unrelated Azure selection. Save local URLs by the same app-config rule.

For each required Azure service, follow this order at EXECUTE infra kickoff, before
creation-specific IaC or any create/apply command. This is not a Discovery prerequisite
or a separate gate. Reuse valid previously selected services/bindings/answers on Resume;
do not repeat this interview for unchanged dependencies.

1. **Discover and offer reuse.** List the needed service capabilities from the approved
   design, not a full provider stack inferred from "AI." Reuse the authorized RG/subscription
   context; collect missing scope/consent once. Discover only relevant resource types,
   present a short candidate set and inspect necessary details of selected candidates.
   Do not expand an RG lookup to the subscription without authorization or audit every
   account/model/region. Label unverified compatibility. Ask which candidates the Human
   wants to reuse; login or visibility is not a reuse decision. Reuse transfers no ownership
   and authorizes no implicit modification/redeclaration.
2. **Offer manual configuration.** For dependencies not selected for reuse, offer the Human
   a way to configure an existing service manually, including an authorized service outside
   discovery visibility. Capture endpoint/connection URLs, deployment/model names and only
   other non-secret settings the app needs under [application connection settings](#application-connection-settings).
   Never ask for credentials or credential-bearing URLs in chat. Credential-bearing
   connection strings must be entered through approved secure local input/secret storage,
   referenced by app configuration, not copied into TWTTY profiles or evidence. Manual
   configuration does not waive identity/no-key policy. Denied/ambiguous discovery or
   invalid/unusable manual settings are blocked/unknown, not proof of absence and not
   permission to create replacements.
3. **Create only the remainder.** Only after reuse and manual configuration are declined
   or genuinely unavailable, propose the minimum missing services. Review the concrete
   target/change; author and review the environment-owned IaC, then obtain the required
   provisioning consent covering identity, data and usage/cost once. Actually execute
   the bound provider's native apply/deployment command and wait for its terminal result;
   writing IaC or recommending a command is not provisioning. Keep concrete commands in
   the provider binding. Use reviewed IaC and the bound provider's native route;
   choose a matching minimal workflow rather than
   importing a project/hosting starter and its unrelated prerequisites. Resolve only missing
   inputs; no blanket policy/quota/RBAC/network preflight or question per CLI read. An
   instance choice within the approved design does not restart PLAN; material architecture,
   permission or cost changes require approval. Capture the native result/output.
   Save returned bindings after native success
   by the same app rule, before dependent app work.
   Do not wait for app work, an eval harness, app CI or an infrastructure PR merge.
4. **Continue on native success.** Use the native install/start/create/apply outcome and returned
   outputs, record the result once in existing work-item evidence using logical aliases
   and safe references rather than raw target parameters/provider-output blocks, then begin app
   development. Any retained target/binding/provider/error text goes through core §2's
   shared privacy utility before the evidence write; pass known operation identifiers
   privately, without discovering extra data or changing actual service/IaC inputs.
   No separate infra smoke test, model call or connectivity gate. The normal
   first app run supplies real connection evidence; until then do not claim data-plane
   access or app quality was verified. Reuse valid unchanged services.

**No additional local-infra checks.** For new isolated development resources, no
standalone preflight, build/validate/what-if chain, validation wrapper or dedicated
infrastructure-validation CI job is required.
Do not generate wrappers, Python source-string tests, folder/schema/ownership checkers
or custom infra validators. Map native results to applicable resource ACs in existing
evidence; perform its existing privacy review before persistence/publication.
Use preview/native plan when modifying shared/production resources, deleting/replacing
resources, or when target policy requires it. Other providers retain mandatory native
steps (for example Terraform initialization/plan/apply); do not duplicate them in custom
framework scripts.

Inspect real errors and only affected partial state; correct and retry within the unchanged
approved boundary and existing finite recovery limits. Do not restart PLAN, add a recovery
test suite or ask for the same valid authorization solely because a command failed.
An actual Escalate, changed resource/permission/cost boundary, destructive action or native
approval still needs its required Human decision. Never blindly replay a partially applied
deployment or silently change the approved model/region.

This is the default development-dependency sequence, not a new lifecycle stage or gate.
Existing corporate/repository policies and scoped access/spending approvals remain.
Cloud hosting stays CD-owned with its applicable promotion checks; do not provision
hosting merely to satisfy development readiness.

If service access is blocked, report the exact missing readiness and next authorized
action. Independent/offline work may proceed only under an explicitly approved plan
deferral, not an invented substitute. Native provisioning success proves resource
creation only; actual app/service/model acceptance remains pending until the normal
app journey succeeds at its required gate. Demo output or offline CI cannot clear it.

### Application connection settings

- **Location.** Reuse the app's existing runtime-config file, key names and loading
  convention. Do not move working settings or add a competing file. For a new app with
  no established convention, use one ignored `.env.local` at the product repository root
  (not under `twtty/`, `twtty-runtime-config/` or the IaC folder). A stack's established
  native convention takes precedence; record the actual choice, not multiple alternatives.
- **Contents.** Save only required non-secret bindings, such as service URLs and deployment
  names, from either reused services or native provisioning outputs. Preserve unrelated
  settings. Ensure a new local file is ignored before writing actual values. Credentials,
  tokens and credential-bearing URLs use the approved identity/secret store, not this file,
  source or replay evidence.
- **Consumption.** The app's normal launcher/framework configuration MUST load the chosen
  file and use those exact keys. `.env.local` is not automatically loaded by every stack;
  wire it into normal app startup using the stack's supported mechanism, not a validation
  wrapper. Document the relative file path, required key names and normal launch command
  in the existing app README. Do not mark the connection verified until the normal app
  request actually reaches the selected service; missing settings must not silently select
  mocks, another service or a hidden default.
- **Same checkout.** Initial infra setup and Sequential app development use this same
  local file. No copy, handoff step, repeated reuse question or reprovisioning is needed.
  Switching branches in the same checkout does not itself require another config file.
- **Separate checkout only.** If domain/parallel work actually creates another worktree
  or clone, make the approved non-secret bindings available through its existing loader
  or local config before running the app there. Do not copy the whole environment file
  or credentials; preserve the destination's own instance overrides and use its authorized
  identity. Record only the safe config path/key names and outcome in ordinary evidence,
  never actual connection values. This exception adds no config layer, script or gate.

### Tooling readiness and reuse

Before a restore, installation or executable download, inspect only the tools and inputs needed by the next approved task. Use the approved plan, manifests/locks, package-manager metadata and the actual execution context to establish compatibility. A tool installed on the host is not automatically available in a container, remote worker or CI job. Reuse still-valid inventory; refresh affected checks when versions, paths or execution context change.

Distinguish these cases in plain language:

| Status | Meaning and next action |
|--------|-------------------------|
| Available and compatible | The required tool/runtime or cache entry is already usable here. Reuse it; do not reinstall or request another install approval. |
| Project dependency restore | This checkout/worktree needs its locked packages or virtual environment. Use the existing machine tools and approved package-manager caches; explain that this is not reinstalling Python, Node or the workstation. |
| Missing or incompatible version | The required version/browser revision is unavailable here. Show the required and available versions, source, install/cache destination, download purpose and material effects before requesting any required approval. |
| Access or restore failure | Report the actual error and supported next action. Denied access, feed/TLS failures or unusable cache entries are not proof that a tool is absent. Follow existing bounded recovery rules. |

During technology selection, prefer supported installed versions when they satisfy the requirements. Once versions/locks are approved, do not downgrade, repin or switch browser executables merely to avoid a download. A general system browser or another project's dependencies do not automatically satisfy the selected test runtime. Inspect the supported shared browser/package cache before proposing another download; use package-manager integrity/version verification rather than copying another worktree's `node_modules`, virtual environment or credentials. Do not purge shared caches or alter machine-wide settings without applicable approval.

Check for an existing explicit approval before asking again. It must apply to the current Human User and execution context, exact action/version or approved range, source/destination and trust/cost scope, and remain unrevoked. Reuse a verified covering grant only where the core, policy and harness permit it; prior app builds, another developer's grant, approval for an unrelated package and general Autopilot are not installation consent. If coverage is missing or ambiguous, ask one focused question for the actual missing action. Do not suppress native permission prompts or treat plan approval alone as permission to download executables.

Keep the prompt proportionate: for a missing test browser, explain that the project needs a particular browser version for its declared tests, whether compatible cached versions exist, and that the action is a cache download rather than a system-browser reinstall. Do not couple this prerequisite question to downgrading the app to mocks, abandoning real-model acceptance or repeating the entire lifecycle. Preserve the approved app/test scope; run independent approved work while the specific prerequisite waits when possible. After an approved restore/install, verify the selected version and actual task readiness, then record the result in the existing setup/work-item evidence without adding another gate or per-tool log entry.

### Parallel setup

The coordinator prepares shared manifests/locks, machine tools, initial services and app
bindings in the common working context before dispatching app workers. Only one owner
changes shared manifests/locks or machine-wide tools; workers must not race to install
the same tool or reprovision the initial services.
This shared base does not make app-only package restores a prerequisite of unrelated
service creation; prepare each operation's requirements when needed.

After that prepared base is available, each concurrent writer gets a separate branch
and worktree/clone. Before its app work, it reads the relevant inherited declarations,
reuses the installed compatible tools and restores only its missing checkout packages.
Independent per-checkout restores may run concurrently using package-manager-supported
shared caches. Never share/copy `node_modules`, virtual environments or credentials.
Separate containers/remote workers use their own actual context, not assumed host tools.

Make approved non-secret app bindings available under the connection-settings rule;
each context uses its own authorized identity and instance settings. Reuse the initial
services where approved, with isolated test data when needed; do not create a service
stack per worker by default. Serialize conflicting service/data mutations. A genuinely
required isolated service instance follows the same dependency -> service -> app order
within that approved worker scope. Cover routine worker setup in the original dispatch
approval where permitted; do not repeat unchanged questions or add setup gates/logs.
Record results in existing setup/work-item evidence. Sequential work needs none of
this worker machinery, and concurrent writers never share a branch or checkout.

### Local runtime and containers

Start/reuse one app instance for app-backed tests/evaluations and interactive use. Unit/direct evaluations can run in-process without an app server. Restart only when actual changes or lifecycle isolation require it. Keep the verified app available when requested; distinguish retained services from temporary test processes. Recipes stop only their own identified processes.

Local Docker services are **project-owned**, not recreated per test. Persist a stable unique Compose project name in ignored instance settings and pass it in every start/stop process. Verify own volumes and reserved ports; retain data. Do not attach another checkout's volumes, stop unrelated apps or change machine-wide settings to resolve conflicts.

Use the shared Dockerfile and app/evaluation code. Local images are candidates, not release artifacts. Verify authentication/DNS/network access inside a container; host `az login` is not automatically available. Use approved developer authentication without baking credentials/tool caches into images. Production Managed Identity must not depend on developer CLI login.

## Environment IaC and resource ownership

```text
infra/
  environments/
    local/
      compose.yaml
      modules/
    cloud/
      dev/modules/
      qa/modules/
      uat/modules/
      preprod/modules/
      prod/modules/
```

Each selected environment has self-contained IaC and inputs: no shared infrastructure-module folder or cross-environment module dependency. Include only needed cloud stages, not five mandatory deployments. Existing alternate layouts/owners are preserved until an approved migration; never move data/resources merely for folder consistency.

**Place IaC by environment purpose and deployment ownership, not physical resource location.** The `local/` environment owns local support-service/Compose definitions and newly owned Azure dependencies supporting local development, including model deployments, identity/RBAC, parameters and modules. The `cloud/<stage>/` environment owns infrastructure for that selected shared cloud stage. A locally running app's new development model belongs under `infra/environments/local/`, even though inference runs in Azure; it does not create a `cloud/dev/` environment.

Consuming an authorized existing resource does not transfer ownership. A local app may reference a cloud-stage-owned model without redeclaring it in `local/`, moving its IaC or making `local/` import that stage's modules. New owned resources follow the placement rule; mistaken paths in a newly generated plan are not approved legacy layouts. An existing project's adopted layout is reused until an explicit approved migration.

PLAN §1.3 records ownership using the [environment ownership table](../../templates/plan-template.md#13-infrastructure-architecture); §2.3 and work-item footprints must agree. Bind recipes, CI validation, apply inputs and Handoff instructions to those approved entry points. Shared cloud infrastructure CD must not apply developer-owned `local/` IaC; developer CLI preparation must not apply shared cloud-stage IaC except its approved identity-bootstrap/break-glass procedure.

Application, adapters, tests, evaluator engine, datasets, thresholds, report schema, Dockerfile and reusable scripts remain shared outside this hierarchy. Select environment values rather than fork implementation. A resource has one declared deployment owner; reference authorized shared existing services without takeover/competing declarations.

The [Azure binding](../cloud/azure.md) owns the approved **developer Azure CLI** route for necessary local-development cloud dependencies. Shared cloud-environment resources and application release remain pipeline-owned. Do not create a full hosting stack just to run locally.

## Shared CI and CD

CI is required; application CD is opt-in. The integration/release branch defaults to
`main`; preserve the project's authorized selection and protection rules.
For hosting delivery, follow [SDLC's CI/CD contract](../../sdlc.md#34-execute).
That section owns the mandatory hosting contract; provider bindings supply only its
platform-specific implementation.

- CI invokes the same versioned build/scan/test/evaluation logic as local verification, using safe execution configuration. PR code gets no production/deployment credentials.
- Hosted runtime uses real cloud services, never emulator fallback, and supported workload identity. Pipeline auth uses approved federation; developer auth is separate.
- Shared outer automation is repository-owned. No per-developer cloud-hosting sandbox option is introduced.

## Evaluation and evidence contract

Keep one application/agent implementation across native, applicable container and cloud
execution. When formal evaluations/tests apply, share their engine, fixtures/datasets,
thresholds and report shape too; do not invent an unselected L1 harness. Thin launch/
identity wrappers may differ, not the underlying behavior. Use direct invocation where
appropriate; an API/UI is added only when project requirements call for it.

Developer Entra authentication is used locally; supported cloud hosting uses Managed Identity. Verify deployment/endpoint compatibility, token audience/scope, permissions and reachability. No fetched service keys or copied credentials.

Distinguish offline/mock readiness, real-model quality and deployed integration. Health/configured flags, offline abstention or another app's passing result do not prove inference. Use approved synthetic/public setup/eval inputs and billable-call consent. Preserve citations where required, measured scores/tokens/cost, revisions, versions, N/K/seed and statistical limits without secrets/sensitive infrastructure identifiers. Nondeterministic answers/latency need not be identical across runs.

Respect stricter policy/risk controls, corporate TLS/package restrictions and existing bounded failure rules. Missing inputs/access/evidence are explicit blockers, not successful reduced-function fallback.

## Resume preparation

This procedure applies only to local setup/run selected during Resume under
[SDLC §3.6](../../sdlc.md#36-existing-project-preparation). Start project and later
Iterations keep their existing EXECUTE setup procedure; do not route them here.
Other Resume actions prepare only their own missing prerequisites, not the whole app.
Preserve the existing app, approved design, selected context and adopted configuration;
do not restart the lifecycle, reopen completed work or create another iteration.

The AI Agent MUST perform authorized setup through available tools rather than hand
the Human commands to execute. Reuse valid current-context approvals; setup/run selection
alone does not authorize installations, discovery/access, provisioning, RBAC changes or
additional costs. Pause for uncovered approvals, Human authentication or actual
input/access/policy/tool blockers, explain the exact gap, and continue when native
results are available. Manual execution is only for a Human-selected route or a concrete
execution limitation. Never transfer another Human's credentials or authorization.

1. **Prepare missing tools.** Read the selected app's manifests/locks, version declarations,
   native recipes and relevant approved plan/config. Follow
   [requirements and dependencies](#requirements-and-dependencies) and
   [tooling readiness and reuse](#tooling-readiness-and-reuse) for needed restores or
   approved installs. Reuse compatible installed tools; do not repeat Discovery or CI setup.
2. **Initiate required sign-in.** For Azure dependencies, inspect the current developer
   context with `az account show`. Reuse a usable applicable login. If authentication
   is missing/expired, ask to initiate native sign-in and scoped resource discovery;
   obtain the missing consent and have the AI Agent launch `az login` in the actual
   execution environment (`az login --use-device-code` when appropriate for a supported
   headless/remote context). The Human completes browser authentication while the
   native process remains available; wait for its result before dependent Azure lookups.
   Never request credentials in chat; credentials and device codes stay in the native
   terminal/authentication surface, not app settings or replay evidence. Report actual
   network/policy/tool errors rather than assuming every failure requires login.
   If the harness cannot support native sign-in, explain that limitation and guide only
   the necessary Human step. Other providers use their bound native identity mechanism.
3. **Discover before asking for endpoints.** For missing service bindings, confirm the
   authorized subscription/resource-group scope once. If needed and authorized, use
   `az account list` to present subscription choices; do not assume the default/first
   account. Run `az account set --subscription "<approved-subscription>"` when needed
   and confirm the context with `az account show`. Discover only required service types
   and relevant model deployments using native tools. Do not broaden an RG lookup to
   the subscription without authorization or audit unrelated services/models/regions.
   Missing local settings are not a reason to begin with a manual endpoint questionnaire.
4. **Select reuse and save bindings.** Present discovered candidates and ask which to
   reuse; login/visibility alone is not a selection or permission to modify a resource.
   Reuse valid existing selections without asking again. Retrieve selected endpoints,
   deployment/model names and other required non-secret settings through native tools,
   rather than asking the Human to transcribe discoverable values. Save them under
   [application connection settings](#application-connection-settings), preserving the
   app's loader, ignored-file convention and unrelated settings. Reuse ready bindings
   without rediscovering/reconfiguring unchanged services or taking over their ownership.
5. **Offer manual configuration when needed.** If discovery is declined/unavailable or
   no candidate is selected, offer manual existing-service configuration or waiting.
   Ask only for required non-secret settings; credential-bearing values use approved
   secure input/storage, never chat. Manual settings do not bypass required app
   authentication. Denied/ambiguous access or invalid settings are blockers, not proof
   that a service is absent or permission to create replacements.
6. **Provision only an approved remainder.** Only after reuse and manual configuration
   are declined or genuinely unavailable, propose the minimum missing services within
   the approved design. Preserve existing resource ownership/layout. Author/review the
   environment-owned IaC, obtain uncovered target/identity/RBAC/data/usage-cost consent,
   then execute the bound provider's native apply and wait for its terminal result.
   Save returned bindings through the same app-config rule. No raw-create, service-key,
   ownership-takeover or implicit hosting/CI-federation path is authorized. Material
   design/permission/cost changes retain their required approval/refinement.
7. **Run and verify the actual app.** Use the native launcher and selected normal-app
   journey with approved safe inputs and billable-call consent where required, including
   actual service/model access when applicable. UI/startup/health success alone is partial
   readiness, not full functional verification; do not substitute samples/mocks or
   silently downgrade to a UI-only run. If blocked, report the exact missing readiness.
   Keep the verified app available when requested. Record results/gaps under §3.6's
   existing setup/work-item evidence, not a new gate/log; apply the existing privacy rules.
