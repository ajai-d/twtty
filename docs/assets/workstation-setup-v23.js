(() => {
  "use strict";
  const root = document.querySelector("[data-workstation-setup]");
  if (!root) return;

  const commands = {
    new: { name: "Start a new project", label: "Start project", verb: "start project", description: "Begin the first TWTTY baseline.", icon: '<path d="M4 5h6l2 3h8v11H4z"/><path d="M12 11v5m-2.5-2.5h5"/>' },
    resume: { name: "Resume or join a project", label: "Resume", verb: "resume", description: "Continue or join an existing project.", icon: '<circle cx="12" cy="12" r="8"/><path d="m10 8 6 4-6 4z"/>' },
    iteration: { name: "Start a new iteration", label: "Start iteration", verb: "start iteration", description: "Add a new feature or fix an issue.", icon: '<path d="M20 5v5h-5M4 19v-5h5"/><path d="M19 10a7 7 0 0 0-12-5M5 14a7 7 0 0 0 12 5"/>' },
    handoff: { name: "Hand off to another team or customer", label: "Handoff", verb: "handoff", description: "Hand off to another team or customer.", icon: '<path d="M10 5H4v15h15v-6M13 4h7v7M20 4l-9 9"/>' }
  };
  const types = {
    sdlc: "Software app",
    "sdlc-for-agentic-apps": "AI / agentic app",
    dataeng: "Data engineering",
    "reverse-engineering": "Reverse Engineering"
  };
  const profiles = {
    local: { name: "Local Development", caption: "Develop and verify locally, with required CI and reviews. No cloud application deployment." },
    shared: { name: "Local Development + Cloud Delivery", caption: "Develop locally, then use approved CI/CD workflows to build and deploy." }
  };
  const defaults = { command: "new", kind: "sdlc", profile: null };
  let state = { ...defaults };
  let opener = null;
  let draftKey = "";
  const drafts = new Map();
  const assessment = () => state.kind === "reverse-engineering";
  const agentic = () => state.kind === "sdlc-for-agentic-apps";
  const isResume = () => state.command === "resume";
  const isHandoff = () => state.command === "handoff";
  const canSelectProfile = () => !assessment() && !isResume() && !isHandoff();
  const guideUrl = () => new URL(root.dataset.workstationGuide, location.href);
  const overviewUrl = () => new URL(root.dataset.workstationOverview, location.href);
  const arrow = '<div class="arrow" aria-hidden="true"></div>';
  const seedExamples = {
    sdlc: { build: "A web application for submitting and tracking team work requests.", done: ["Users can submit a request with a title and description", "Users can view requests and update their status", "All tests pass", "Anyone can clone and run it locally"] },
    "sdlc-for-agentic-apps": { build: "An assistant that helps users find answers in approved help documents.", done: ["Answers cite the documents that support them", "When the documents do not contain the answer, the assistant says so instead of inventing one", "Representative questions and safety checks meet the agreed acceptance criteria", "Anyone with the required approved service access can run and verify it locally"] },
    dataeng: { build: "A daily pipeline that turns order records into a sales summary for analysts.", done: ["Valid records appear in the summary with the expected totals", "Invalid records are reported with a reason", "Rerunning the same input does not duplicate results", "Documented data-quality tests pass"] },
    "reverse-engineering": { build: "I want to reverse engineer the following repository: my-app\n\nAudience: developers joining the project\n\nPurpose: understand the system and identify where future changes belong", done: ["The audience has a reliable, evidence-based understanding of the repository, sufficient to accomplish the stated purpose", "Verified facts, inferences and unknowns are clearly distinguished", "The target's code and configuration remain unchanged outside the approved TWTTY artifact folder"] }
  };
  const iterationExamples = {
    sdlc: { build: "Add a CSV download of the results already displayed by the application.", done: ["The downloaded rows and columns match the displayed results", "Existing viewing behavior remains unchanged", "Tests cover the download and any affected existing behavior"] },
    "sdlc-for-agentic-apps": { build: "Improve document citations in the existing assistant's answers.", done: ["Answers link to the specific documents supporting their claims", "The approved quality, safety and cost requirements remain satisfied", "Current evaluation evidence covers the changed behavior"] },
    dataeng: { build: "Add a rejected-record report to the existing order pipeline.", done: ["Each rejected record has an actionable reason", "Valid-record processing and existing data contracts remain unchanged", "Tests cover the new report and affected pipeline behavior"] },
    "reverse-engineering": { build: "Extend the existing assessment to explain one previously undocumented integration.", done: ["The integration's purpose, data flow and dependencies are supported by evidence", "Unknowns and contradictions are recorded rather than guessed away", "The investigation does not change the target's implementation"] }
  };
  function exampleSeed() {
    const iteration = state.command === "iteration";
    const example = (iteration ? iterationExamples : seedExamples)[state.kind];
    return `## ${iteration ? "What This Iteration Changes" : "What I Want To Build"}\n\n${example.build}\n\n## Done Looks Like\n\n${example.done.map(item => "- " + item).join("\n")}\n`;
  }

  const activities = [
    { id: "seed", region: "human", commands: ["new", "iteration"], title: () => state.command === "iteration" ? "SEED - confirm the change" : "SEED - prepare the intent", caption: () => state.command === "new" ? "High-level description of what you want to build and what done looks like. Click + for an example." : "High-level description of what you want to change and what done looks like. Click + for an example.", detail: "Define the outcome and acceptance boundaries. Start project establishes the first TWTTY baseline for new software, an explicitly approved existing-code goal, or a read-only assessment. Preserve existing source and lifecycles. A later Iteration reuses the approved Project Seed, requires verified initial baseline completion and adds its own approved Iteration Intent. SEED and SEED-EXIT stay Interactive.", section: "seed", seed: true, stage: "01" },
    { id: "access", region: "human", commands: ["resume", "handoff"], title: "Confirm project and access", caption: "Confirm the existing project and your access. Click + for details.", detail: "Use the shared or delivered repository and the current developer/customer's credentials. Preserve valid code and project context. Repository ownership, infrastructure ownership and setup depth are independent; do not inherit another user's claim or deployment authority.", section: "connections", stage: "01" },
    { id: "entry", region: "human", title: () => ({ new: "New project", iteration: "New iteration", resume: "Resume", handoff: "Handoff" })[state.command] + " - start the workflow", caption: () => isResume() ? "Continue the TWTTY workflow with a simple prompt. Click + for the command." : isHandoff() ? "Hand off to another team or customer. Click + for the command." : "Start the TWTTY workflow with a simple prompt. Click + for the command.", detail: "Start the selected workflow in an AI agent with access to the project and framework folders.", section: "flow", entry: true, stage: "02" },
    { id: "handoff-scope", region: "guided", commands: ["handoff"], title: "Confirm the handoff boundary", caption: "Source, history, destination and access.", detail: "Approve the source snapshot, included files and history, private repository destination and recipient access. Include the selected project-owned TWTTY configuration and records, not just the latest Iteration. Handoff does not start a baseline or Iteration, continue implementation or authorize deployment.", section: "customer-handoff" },
    { id: "handoff-export", region: "guided", commands: ["handoff"], title: "Prepare sanitized export copies", caption: "Preserve the source. Exclude personal state.", detail: "Freeze the approved snapshot and work in isolated export copies. Include the approved tracked and non-ignored untracked working files, honoring working deletions, required licenses and safe history. Resolve required LFS, submodule and link content. Scan selected files and history, sanitize only the export copies and exclude credentials, private caches, local images and application data. Never copy source .git administration or rewrite source history.", section: "customer-handoff" },
    { id: "handoff-verify", region: "guided", commands: ["handoff"], title: "Verify the repository and ZIP", caption: "Matching content, safe extraction and recipient instructions.", detail: "Prepare the private export repository and matching ZIP from the same sanitized snapshot/history. Verify parity, safe extraction, required content and applicable checks. Include HANDOFF.md with verified prerequisites, locked restore/run recipes, actual artifact roots and remaining gaps. Keep receipts and checksums outside source and payload. Missing content or failed checks blocks publication.", section: "customer-handoff" },
    { id: "handoff-publish", region: "guided", commands: ["handoff"], title: "Publish the approved handoff", caption: "Recheck the source and verify private access.", detail: "Recheck source HEAD, remotes, status and raw file hashes before publication; invalidate the export if the input snapshot changed. Obtain specific destination/publication/access approval, then publish the private GitHub repository and matching ZIP and verify final parity and recipient access. Do not treat successful publication as verified recipient or cloud readiness.", section: "customer-handoff" },
    { id: "handoff-end", region: "finish", commands: ["handoff"], title: "Continue with the recipient's identity", caption: "Clone or extract, then Resume.", detail: "Recipients use twtty resume with their own identity, credentials and approved services, referencing the current separate authorized framework. Recover responsibility and choose the permitted action; selected setup/run restores only missing locked inputs and builds images where applicable. Do not transfer the sender's active work claim, credentials or Autopilot authority, and do not invent lifecycle approvals.", section: "receiving-project" },
    { id: "recover", region: "guided", commands: ["iteration", "resume"], title: "Read Saved Project Progress", caption: "Use recorded decisions, configuration and repository history.", detail: "Recover the selected scope from the current branch/worktree, consistent state summary, relevant replay evidence and actual artifacts; do not reconstruct unrelated history or infer an assignment from Git's last author. Recover specialization, risk, approvals and matching pauses. Read the selected framework's complete dispatcher, core and active methodology chain on every invocation; this does not upgrade project-owned configuration. Resume prepares only the selected action's missing prerequisites, with the current Human's own authority.", section: "resume-flow" },
    { id: "resume-route", region: "guided", commands: ["resume"], title: "Reconcile the recorded work and approvals", caption: "Determine the real stage/task before deciding what to run.", detail: "TWTTY recovers the active scope and next unfinished task from the project's replay evidence, branch/worktree and Git history, checking the current artifacts. Reuse a consistent state summary and relevant log tails; do not rebuild unrelated history. Missing or conflicting evidence must be surfaced, not guessed.", section: "resume-flow" },
    { id: "pickup", region: "guided", commands: ["resume"], title: "Determine the next permitted action", caption: "Recover responsibility, then confirm the applicable action.", detail: "For unfinished SDLC work, verify the original Human's responsibility or an approved successor assignment before offering continuation; a contributor continues only their verified claim or parent dispatch. A different Human without that assignment is offered applicable local setup/run, an approved handover or an eligible separate Iteration, never automatic takeover. Completed scopes can offer setup/run, a new Iteration or both without proposing new intent. Preserve pauses and baseline prerequisites. Ordinary Resume never scans/ranks global assignments: only an explicit request to find unclaimed work enables discovery, followed by Human selection even under Autopilot and a fresh eligibility check before publishing the shared claim. Assessment retains its own read-only continuation rules.", section: "resume-flow" },
    { id: "discovery", region: "guided", commands: ["new", "iteration"], title: "Discovery Interview", caption: () => assessment() ? "Audience, target, evidence boundaries and success." : state.kind === "dataeng" ? "Sources, sinks, ownership and delivery intent." : "Required questions, configuration and delivery intent.", detail: () => assessment() ? "Read the approved seed/intent, then explicitly ask for Delegated or Interactive Discovery before any elicitation or drafting. Complete all four adapted rounds: surface, deep dive, edge cases and acceptance. Record audience, target boundaries, remote-read policy, evidence access, sensitivity and success. Do not apply SDLC's UX/API interview, app configuration, cloud delivery or provisioning procedure to the read-only investigation." : "After reading the approved seed/intent, obtain the independent Discovery, UX and API mode answers before eliciting or drafting requirements. Complete all four rounds and the applicable config interview; show actual effective settings and offer Use these settings / Customize settings before meta/config, using the current approval mode and any covering Autopilot grant. Reuse valid project choices, resolve only changed or missing settings, and record the transcript. Capture Sequential/Parallel once and reuse that answer at PLAN. Discovery is part of SPEC, not a fifth stage.", section: "discovery-interview" },
    { id: "spec", region: "guided", commands: ["new", "iteration"], title: "SPEC - draft specification", caption: () => state.kind === "dataeng" ? "Source/sink contracts, data-quality rubric and acceptance." : assessment() ? "Investigation scope, evidence coverage and acceptance." : "Testable requirements and acceptance criteria.", detail: "Draft and mechanically check the applicable requirements. Reuse unchanged approved context for an iteration; obtain the required SPEC approval. Data engineering includes sources/sinks, measurable quality and versioned contracts; assessment retains a read-only target and approved artifact subtree. Develop the applicable functional and non-functional requirements, use cases, UX/API requirements and acceptance criteria from the discovery results.", section: "spec", stage: "02" },
    { id: "plan", region: "guided", commands: ["new", "iteration"], title: () => assessment() ? "PLAN - investigation plan" : "PLAN - architecture, design and orchestration", caption: () => state.kind === "dataeng" ? "Pipeline design, lineage, SLOs and backfill verification." : assessment() ? "Read-only investigation, sampling and evidence verification." : "Design, dependencies, environments and controls.", detail: "Plan only the approved scope and applicable verification. At PLAN entry, offer Interactive, Autopilot - EXECUTE only, and Autopilot - all remaining stages; reuse an earlier valid covering grant. SDLC reuses the recorded Sequential/Parallel answer, validating actual dependencies, footprints, targets and cap before dispatch. Research applicable technologies, reuse known preferences and honor the approval mode. Reference the bound development procedure; record app-specific design, services, ownership, gaps and work, not a duplicate setup procedure. Initial development services precede app/evaluation-harness implementation; required eval assets precede affected LLM behavior. Assessment plans read-only investigation, not app delivery.", section: "plan", stage: "03" },
    { id: "execute", region: "guided", commands: ["new", "iteration"], title: () => assessment() ? "EXECUTE - investigate and verify" : "EXECUTE - implement and verify", caption: () => assessment() ? "Read-only investigation, evidence and reports." : "Approved scope, applicable reviews and evidence.", detail: "Execute only the approved scope under the active specialization. Workstation inner loops and delivery outer loops are activities within the workflow, not additional lifecycle stages.", section: "execute", stage: "04" },
    { id: "claim", region: "app", commands: ["new", "iteration"], title: "Use the Right Branch and Working Folder", caption: "Create separate branches only when the work or repository rules require them.", detail: "Prepare initial infrastructure and save app connection settings in the common authorized context first. Single-domain Sequential work reuses it with no extra branch when direct development is permitted. Otherwise use the policy-required scope branch/PR; derive affected app-domain branches from the prepared base and reuse them for sequential items. Each concurrent writer needs an exclusive branch and worktree/clone. Shared contributor pickup publishes its draft-PR claim; internal workers may reuse the parent claim and integrate serially under approved dispatch where policy permits. Never bypass required protected-target PR/CI/reviews.", section: "collaboration" },
    { id: "prepare", region: "preparation", title: () => isResume() ? "Restore Missing Tools and Packages" : "Install or Reuse Required Tools", caption: "Use approved runtimes, tools and locked package versions.", detail: "Use the approved plan, package manifests, lockfiles and existing setup commands to identify what the next operation needs. Reuse compatible installed tools and cached packages; request any installation approval not already granted. Prepare infrastructure tools before services; restore app-only packages when app work needs them. Save initial service connection settings before creating app-domain or parallel-worker branches. Each working folder restores only its missing packages, using the developer's own identity and ignored local settings. Resume prepares only the selected action; recovering SPEC/PLAN does not require full app setup.", section: "inner-loop" },
    { id: "eval-ready", region: "app", commands: ["new", "iteration"], when: agentic, title: "Prepare Required AI Evaluation Tests", caption: "L2+ or explicitly required; L1 normally uses a real-model smoke test.", detail: "After required dependency/service preparation, verify or reuse required datasets, evaluators, safety fixtures and thresholds before affected LLM behavior is implemented. L1 defaults to a normal-app live-model smoke, not an evaluation harness, scored dataset or safety-test suite; broader verification needs explicit Human selection or stricter policy, not a general Autopilot grant. Required safe behavior, runtime guards and approved budgets remain. Another app's results are not this app's passing evidence.", section: "evaluations" },
    { id: "data-contracts", region: "app", commands: ["new", "iteration"], when: () => state.kind === "dataeng", title: "Confirm pipeline contracts and prerequisites", caption: "Current and applicable inherited source/sink requirements.", detail: "Resolve the approved source/sink contracts, classification, quality dimensions, schemas and real dependencies before affected pipeline changes. Reuse still-valid assets; do not recreate unchanged implementation just to populate the flow.", section: "data-flow" },
    { id: "implement", region: "app", commands: ["new", "iteration"], title: "Implement the approved work", caption: "Scoped changes and risk-appropriate verification.", detail: "Use the authorized working context, approved inputs and applicable inherited requirements. Do not expand infrastructure or deployment scope merely because a category is selected. Preserve native development, runtime safety and the current verification contract; selecting an AI/data project type does not itself opt L1 into formal suites.", section: "execute" },
    { id: "native", region: "app", title: () => state.kind === "dataeng" ? "Run and Debug the Pipeline" : "Run and Debug Locally", caption: "Edit -> build/test -> run/debug -> repeat.", detail: "Run the normal app/pipeline journey with representative safe inputs and actual required services. Health flags, samples and mocks do not establish required model/service behavior. Use native execution and hot reload. Applicable functional tests and app-backed evaluations reuse the app; direct evaluations need no server. Restart only when required. Apply risk-selected scans/tests/evals and, where containerized delivery applies, its image checkpoint rather than rebuilding after every edit. Keep the verified app available when requested and record actual results/gaps.", section: "inner-loop" },
    { id: "data", region: "app", when: () => state.kind === "dataeng", title: "Verify data quality and contract compatibility", caption: "Current evidence for affected outputs and inherited obligations.", detail: "At L1 smoke-only, inspect an actual safe source-to-sink journey against approved expectations without inventing a DQ suite/report. At L2+ or when explicitly selected/required, run applicable DQ-referenced automated tests and retain their results. Verify affected current and inherited contracts, thresholds, versioning and backfill semantics; report failures explicitly. Existing approved formal requirements are not discarded by calling work a smoke.", section: "data-flow" },
    { id: "data-operations", region: "app", when: () => state.kind === "dataeng", title: "Verify applicable SLOs and lineage", caption: "Freshness, completeness, cost, observability and backfill evidence.", detail: "Apply the active data-engineering/risk requirements and approved source/sink obligations. Verify relevant lineage, schema evolution, freshness/completeness/cost SLOs and backfill behavior; reuse valid unchanged evidence only when its inputs/assumptions remain applicable. Local fixtures do not replace required real-service evidence.", section: "data-flow" },
    { id: "eval", region: "app", when: agentic, title: "Verify model behavior and safety", caption: "L1 live-model smoke; formal evaluations when applicable.", detail: "Use the actual approved model in the normal app journey with safe inputs and required billable-call consent. At L1 smoke-only, record observed behavior and actual available usage, with unavailable measurements stated explicitly; claim no statistical quality or repeatability. When formal verification applies, reuse one evaluation engine, datasets, thresholds and report schema across local/cloud runs and satisfy the approved N/pass rule, safety and budget controls. Direct evaluations need no server; app-backed evaluations reuse the app. Mocks, health flags and failed inference never prove required live-model acceptance.", section: "evaluations" },
    { id: "container", region: "app", title: "Build and Test the Container (If Needed)", caption: "Only for containerized delivery; run the required scans and tests.", detail: "Only where containerized delivery applies, build/scan/run/test a local candidate before the PR or when packaging/runtime changes, following the active risk/policy controls. Use the shared Dockerfile and applicable local Compose services; no unnecessary Docker/emulator requirement is added to a non-container scope. Keep ports/data isolated and verify identity/connectivity inside the container through normal app checks. Host sign-in is not automatically available there. Local images are candidates, not release artifacts; reuse valid builds and do not rebuild after every edit.", section: "container-checkpoint" },
    { id: "pr", region: "app", title: "Review and Integrate Changes", caption: "Run required checks and follow the repository's merge rules.", detail: "Apply active risk/specialization requirements, required CI and target publication controls. Use the authorized direct integration or required domain/scope PR; do not invent a branch/PR per sequential item or duplicate a shared claim. Internal worker results integrate serially under approved dispatch where target policy permits. Keep application CI, development provisioning and application CD separately scoped. Local completion is not cloud deployment or permission to bypass protected-target reviews.", section: "delivery" },
    { id: "emulators", region: "preparation", title: "Start Required Local Services", caption: "Reuse configured services; use containers or emulators only when needed.", detail: "After their tool prerequisites, create/start or reuse only approved local support services using native tooling or approved prebuilt images. Do not build the unfinished app or invent an emulator for a required real service. Use the adopted layout; new local Compose definitions conventionally live under infra/environments/local/. Keep project-owned volumes/data and unique instance names; never stop unrelated apps. Save connection settings through the app's existing ignored configuration and loader.", section: "environments" },
    { id: "cloud-dev", region: "preparation", title: "Connect to Existing Cloud Services", caption: "Find approved services, choose one or enter its connection settings.", detail: "Reuse the developer's valid login and selected cloud services. If sign-in is needed, request any missing approval and start the provider's normal sign-in process; the Human signs in outside chat. Find only required service types and model deployments within the approved account and resource scope. Offer candidates, then retrieve the chosen service's non-secret connection settings with the provider's tools instead of asking the Human to retype them. If discovery/reuse is declined or unavailable, offer manual existing-service configuration or waiting. Denied access is not absence or permission to create replacements. A login alone does not authorize service use, changes or cost.", section: "connections" },
    { id: "new-service", region: "preparation", title: "Create Missing Cloud Services (If Needed)", caption: "Review the infrastructure code, approve creation and save connection settings.", detail: "Only after reuse and manual configuration are declined or genuinely unavailable, propose the minimum missing services. Obtain any target, identity, data or cost approvals not already granted. Review infrastructure as code (IaC) and use the selected cloud provider's approved tools and workflow, such as Azure CLI with Bicep or an approved Terraform workflow. Wait for the deployment command to finish and save non-secret connection settings through the app's normal configuration loader. New isolated development resources need no extra preflight, separate validation/what-if chain, infrastructure smoke/model-call gate or app-CI prerequisite. Keep required provider steps and previews for shared/production changes, destructive changes or policy-required targets. Creation is not proof of working model access: the normal first app run verifies that. Continuing independent/offline work with blocked required access needs an explicitly approved plan deferral.", section: "local-cloud-services" },
    { id: "local-end", region: "finish", when: () => state.profile === "local" && !isResume(), title: "Verify development outcome", caption: "Integrated app and required dependencies; no application release.", detail: "Record actual readiness. This category is a stopping point, not a rewrite of the project's approved Runtime target. Keep the verified local app available as requested, record remaining cloud-specific gaps and preserve shared delivery obligations.", section: "inner-loop" },
    { id: "recover-end", region: "finish", commands: ["resume"], title: "Record Progress and Next Steps", caption: "Record actual results, approvals and remaining limitations.", detail: "Keep records accurate without claiming checks that did not run. Resuming a stage does not mean the whole iteration is complete. A developer's local completion does not cancel the project's shared release obligations or another person's work claim.", section: "resume-flow" },
    { id: "pending", region: "finish", when: () => canSelectProfile() && !state.profile, title: "Resolve delivery context before continuing", caption: "No runtime preparation, provisioning or release is assumed.", detail: "The delivery context is missing or not yet recovered. Startup asks or recovers existing context. Do not silently choose local, reuse another command's selection or claim the requested outcome is verified. Delivery intent is not an extra command argument.", section: "workstation-model" }
  ];
  const outer = [
    { id: "ci", title: "Run Continuous Integration (CI) Checks", caption: "Build, scan and run the required tests and AI evaluations.", detail: "Use the same repository-native verification recipes as local development. PRs validate untrusted changes without granting production credentials. Required CI provides authoritative evidence; cloud-dependent gates run only with authorized inputs and at the required stage.", section: "delivery" },
    { id: "image", title: "Build the Release Package or Image", caption: "Trusted CI creates the release; reuse it across environments.", detail: "After protected merge, trusted CI builds/tests and publishes the authoritative immutable artifact, such as a container image when applicable. Local images are candidates, not release artifacts. Promote the same verified digest across selected cloud stages, never rebuild per environment. Infra-only changes reuse a still-valid app artifact rather than forcing a new build.", section: "delivery" },
    { id: "infra-cd", title: "Deploy Approved Infrastructure Changes", caption: "Run required CI checks; reuse unchanged cloud infrastructure.", detail: "Keep hosting infrastructure CD and application CD in separate independently triggerable workflow definitions. Infra CD applies approved changes/relevant drift only after applicable CI promotion checks, preserving app-owned state. App-only changes reuse unchanged compatible infra. Development-service creation is not subject to the app-CI prerequisite and is never taken over by hosting CD. Use the approved branch and environment locks; do not turn routine app deployment into an infra reapply.", section: "environments" },
    { id: "app-cd", title: "Deploy the Application", caption: "Use the verified release, compatible infrastructure and required approvals.", detail: "Application CD consumes the trusted immutable artifact and waits for the required compatible infra revision under environment locking/coordination rules. Promote the same digest with environment-specific configuration and approved runtime identity. Replace all runtime emulators with approved real services. Do not silently provision prerequisites, invoke infra CD routinely or fall back to mocks. Merge alone is not release authorization.", section: "delivery" },
    { id: "acceptance", title: "Verify Deployment and Promote the Release", caption: "Check real service behavior; keep required approvals and rollback.", detail: "Cloud checks establish deployed identity, private networking, service behavior and production-like acceptance that local execution cannot prove. Promotion respects each selected environment's approvals and policy. Merge alone does not authorize production; failed checks block release.", section: "delivery" }
  ];
  root.innerHTML = `
    <div class="intro"><div><p class="eyebrow">Scalable. Repeatable. Built for team development.</p><h2>Choose your next step.</h2><p>A shared engineering process for individual contributions and coordinated team delivery. Start, continue, extend or hand off work with consistent controls.</p></div></div>
    <div class="canvas">
      <section class="decision" aria-labelledby="command-title"><div class="decision-title" id="command-title">Where Are You Starting?</div>
        <div class="choices" role="group" aria-label="Workflow command">${Object.entries(commands).map(([key, value]) => `<button class="choice command-option" type="button" data-command="${key}" aria-pressed="false"><span class="command-top" aria-hidden="true"><span class="command-symbol"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">${value.icon}</svg></span><span class="command-selected"><svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="m4 8 2.5 2.5L12 5"/></svg></span></span><span class="command-name">${value.label}</span><span class="command-description">${value.description}</span><code class="command-code" translate="no">twtty ${value.verb}</code></button>`).join("")}</div>
        <p class="scenario" data-flow-status role="status" aria-live="polite"></p>
        <fieldset class="project-kind-controls"><legend>Project Type</legend><div class="project-kind-options">${Object.entries(types).map(([key, value]) => `<label class="project-kind-option" for="kind-${key}"><input id="kind-${key}" type="radio" name="project-type" value="${key}" autocomplete="off"><span>${value}</span></label>`).join("")}</div></fieldset>
        <p class="command-note">Existing-project commands recover the project's recorded specialization and configuration.</p>
      </section>
      <div data-delivery-choice>${arrow}
      <section class="decision" aria-labelledby="outcome-title"><h3 id="outcome-title">Project Delivery Intent</h3>
        <div class="ws-options" role="group" aria-label="Project delivery intent">${Object.entries(profiles).map(([key, value]) => `<button class="ws-option" data-profile="${key}" type="button" aria-pressed="false"><strong>${value.name}</strong><span>${value.caption}</span></button>`).join("")}</div>
        <p class="command-note" id="profile-note"></p>
      </section></div>
      ${arrow}<div data-diagram></div>
    </div>`;

  const panel = document.createElement("dialog");
  panel.id = "info";
  panel.setAttribute("aria-labelledby", "info-title");
  panel.innerHTML = `<div class="dialog-top"><div><span class="pill" id="info-state">Workflow details</span><h2 id="info-title"></h2></div><button class="close" id="close-info" type="button" aria-label="Close workflow details">&times;</button></div><div id="info-body"></div><section id="seed-box" aria-labelledby="seed-title" hidden><h3 id="seed-title">Example project seed</h3><p id="seed-help"></p><label for="seed-text">Edit the example before copying</label><textarea id="seed-text" name="seed-example" rows="12" spellcheck="false" autocomplete="off" translate="no"></textarea><button id="copy-seed" type="button">Copy seed</button><p class="status" id="seed-status" role="status" aria-live="polite"></p></section><div class="prompt" id="prompt-box" hidden><pre id="prompt-text" translate="no"></pre><button id="copy-prompt" type="button">Copy command</button><p class="status" id="prompt-status" role="status" aria-live="polite"></p></div><a class="source" id="info-source" data-setup-reference>Read the detailed reference</a>`;
  document.body.append(panel);
  function matches(item) {
    if (isHandoff() && item.id !== "entry" && !item.commands?.includes("handoff")) return false;
    return (!item.commands || item.commands.includes(state.command)) && (!item.when || item.when());
  }
  function node(item) {
    const title = typeof item.title === "function" ? item.title() : item.title;
    const caption = typeof item.caption === "function" ? item.caption() : item.caption;
    const stage = typeof item.stage === "function" ? item.stage() : item.stage;
    return `<button class="node ${stage ? "" : "tiny"}" type="button" data-activity="${item.id}" aria-expanded="false" aria-controls="info" aria-haspopup="dialog">${stage ? `<span class="number">${stage}</span>` : ""}<span class="text"><strong>${title}</strong><small>${caption}</small></span><span class="more" aria-hidden="true">+</span></button>`;
  }
  const spine = items => items.map(node).join(arrow);
  function stateUrl(base, command = state.command, kind = state.kind) {
    const url = new URL(base);
    for (const key of ["setup", "deploy", "checkpoint", "example", "journey", "entry", "ai", "app", "loop"]) url.searchParams.delete(key);
    url.searchParams.set("workflow", command);
    url.searchParams.set("project-type", kind);
    if (command === state.command && canSelectProfile() && kind !== "reverse-engineering" && state.profile) url.searchParams.set("loop", state.profile);
    return url;
  }
  function updateLinks() {
    const guide = guideUrl(), overview = overviewUrl();
    document.querySelectorAll("a[href]").forEach(link => {
      const url = new URL(link.getAttribute("href"), location.href);
      if (url.origin !== guide.origin || ![guide.pathname, overview.pathname].includes(url.pathname)) return;
      const receiving = link.hasAttribute("data-receiving-link");
      const command = receiving ? "resume" : link.dataset.workflowLink || state.command;
      const kind = Object.hasOwn(types, link.dataset.projectType) ? link.dataset.projectType : state.kind;
      link.href = stateUrl(url, Object.hasOwn(commands, command) ? command : state.command, kind).href;
    });
  }
  function closeInfo(restore = true) {
    const button = opener;
    if (button) {
      button.setAttribute("aria-expanded", "false");
      button.querySelector(".more").textContent = "+";
    }
    opener = null;
    if (panel.open) panel.close();
    if (restore && button?.getClientRects().length) button.focus({ preventScroll: true });
  }
  panel.addEventListener("close", () => {
    if (!panel.open && opener) closeInfo();
  });
  function positionHumanInfo() {
    const a = opener.querySelector(".more").getBoundingClientRect();
    const width = document.documentElement.clientWidth, height = document.documentElement.clientHeight;
    if (a.bottom <= 0 || a.top >= height) {
      closeInfo(false);
      return false;
    }
    const gap = 12, edge = 12, min = Math.min(280, width - 24);
    const right = width - a.right - gap - edge, left = a.left - gap - edge;
    let w, x, top, bottom, max;
    if (right >= min || left >= min) {
      const onRight = right >= min;
      w = Math.min(460, onRight ? right : left);
      x = onRight ? a.right + gap : a.left - gap - w;
      top = "12px";
      bottom = "auto";
      max = height - 24;
    } else {
      w = Math.min(460, width - 24);
      x = Math.max(edge, Math.min(a.right - w, width - edge - w));
      const below = height - a.bottom - gap - edge, above = a.top - gap - edge;
      const onBottom = below >= above;
      top = onBottom ? a.bottom + gap + "px" : "auto";
      bottom = onBottom ? "auto" : height - a.top + gap + "px";
      max = onBottom ? below : above;
    }
    Object.assign(panel.style, { left: x + "px", right: "auto", width: w + "px", top, bottom, maxHeight: max + "px" });
    return true;
  }
  function startup() {
    if (state.command !== "new") return `<p>Open the existing project folder in an AI agent with access to the selected framework. Use your own identity; transferred history grants no work assignment or Autopilot authority.</p><p>Paste the command into the agent, not a terminal. The agent reads the complete applicable framework, recovers the selected scope and confirms the permitted action before acting. Start iteration requires the approved original Project Seed and completed baseline; incident requests use their controlled exception.</p>${isResume() && !assessment() ? "<p>Ordinary Resume does not search for assignments. For SDLC and its extensions, request pickup explicitly by adding: <strong>Find and recommend ready, unclaimed work for me.</strong> You still select the work before any shared claim is created.</p>" : ""}`;
    const seed = assessment() ? "framework/methodology/specialized-implementations/reverse-engineering/templates/seed-template.md" : "framework/templates/seed-prompt-template.md";
    const seedUrl = new URL(seed, new URL("../", overviewUrl())).href;
    return `<ol><li><strong>Get TWTTY</strong> or reuse your authorized framework copy. If authentication is required, sign in with your own account, for example with <code>gh auth login</code>.<pre translate="no">git clone https://github.com/ajai-d/twtty.git &lt;framework-folder&gt;</pre></li><li>${assessment() ? "<strong>Use the existing target repository.</strong> Do not create a blank application to assess. Only the approved TWTTY artifact subtree may be written; keep the investigated implementation unchanged." : "<strong>Create the product folder or confirm an existing-code baseline goal.</strong> Keep it separate from the framework. Preserve existing source, history and remotes; use Resume, not Start project, for an existing TWTTY lifecycle."}</li><li><strong>Prepare the Project Seed</strong>: the intended outcome and done criteria. New projects normally use <code>&lt;project-folder&gt;\\twtty\\seed\\seed.md</code>; preserve an existing adopted artifact root. Use the <a href="${seedUrl}">matching seed template</a>. Confirm risk and approve SEED-EXIT interactively.</li><li><strong>Choose the project type</strong> in the diagram. The selected type is <code>${state.kind}</code>${assessment() ? "; the investigated target is read-only" : ""}.</li><li><strong>Open your AI agent</strong> on the project folder and allow framework access; in VS Code use Copilot Agent mode.</li><li><strong>Paste the bootstrap prompt below</strong>, replacing both placeholders with full paths. The project path does not include its <code>twtty</code> subfolder. The agent must read the complete applicable framework on every invocation.</li><li><strong>Optional workspace:</strong> File &gt; Open Folder for the project, Add Folder to Workspace for the framework, then Save Workspace As. Folder access is required; a workspace is not.</li></ol>`;
  }
  function openInfo(button) {
    if (panel.open && opener === button) {
      closeInfo();
      return;
    }
    const item = [...activities, ...outer, { id: "assessment", title: "Verify assessment outputs", detail: "Verify investigation outputs against approved evidence/coverage requirements. The target implementation stays read-only outside the authorized TWTTY artifact subtree. Builds/tests that would write into the target require an isolated throwaway copy, not a target-mutating worktree. Implementation or deployment requires a separate approved scope.", section: "assessment-flow" }].find(value => value.id === button.dataset.activity);
    if (!item) throw new Error("Unknown workflow activity.");
    closeInfo(false);
    const human = item.region === "human";
    panel.removeAttribute("style");
    panel.dataset.popupLayout = human ? "anchored" : "modal";
    panel.setAttribute("aria-modal", String(!human));
    panel.querySelector("#close-info").textContent = human ? "-" : "\u00d7";
    panel.querySelectorAll(".ws-availability").forEach(note => note.remove());
    opener = button;
    opener.setAttribute("aria-expanded", "true");
    opener.querySelector(".more").textContent = "-";
    panel.querySelector("#info-title").textContent = typeof item.title === "function" ? item.title() : item.title;
    const assessmentDetail = {
      pickup: "Recover the selected assessment's actual task, recorded mode, evidence policy, approvals and matching pauses. Continue only the read-only investigation and authorized artifact writes. Work pickup, Handoff, app provisioning and implementation are unsupported. Missing approval or ambiguous evidence requires direction, not a guessed assignment or invented baseline.",
      plan: "Plan the approved read-only questions, sampling, evidence access, verification and allowed artifact writes. At PLAN entry offer the core execution-mode choices unless a valid covering grant applies. Sequential is the default; Parallel requires disjoint artifact footprints, safe non-mutating reads, no dependency in the PLAN DAG, a current-approver-approved cap and consistent returned citations/claim classifications. Do not import SDLC app-worker branches, CI, provisioning or app/evaluation-harness preparation."
    };
    const detail = assessment() && Object.hasOwn(assessmentDetail, item.id) ? assessmentDetail[item.id] : typeof item.detail === "function" ? item.detail() : item.detail;
    if (human) panel.querySelector("#info-body").innerHTML = `<p>${detail}</p>` + (item.entry ? startup() : "");
    else panel.querySelector("#info-body").textContent = detail;
    const showSeed = ["new", "iteration"].includes(state.command) && (item.seed || item.entry);
    panel.querySelector("#seed-box").hidden = !showSeed;
    draftKey = state.command + ":" + state.kind;
    if (showSeed) {
      const iteration = state.command === "iteration";
      panel.querySelector("#seed-title").textContent = iteration ? "Example Iteration Intent" : "Example project seed";
      panel.querySelector("#seed-help").textContent = iteration ? "Use this in the iteration's SEED discussion. The agent preserves the actual artifact root and writes a new intent (normally <project>\\twtty\\seed\\intent-<iteration-id>.md); never overwrite the approved Project Seed." : "Copy and customize this example. A new default layout uses <project>\\twtty\\seed\\seed.md; preserve an existing adopted artifact root. Follow the selected specialization's seed format.";
      panel.querySelector("#seed-text").value = drafts.get(draftKey) ?? exampleSeed();
      panel.querySelector("#copy-seed").textContent = iteration ? "Copy intent" : "Copy seed";
    }
    const type = state.command === "new" ? ` type=${state.kind}` : "";
    panel.querySelector("#prompt-box").hidden = !item.entry;
    panel.querySelector("#prompt-text").textContent = `Read "<full-path-to-twtty.md>" and run: twtty ${commands[state.command].verb}${type} project="<project-folder>"`;
    panel.querySelector("#info-source").href = stateUrl(guideUrl()).href.split("#")[0] + "#" + (item.entry && isHandoff() ? "customer-handoff" : item.section);
    panel.querySelector("#info-source").textContent = human ? "Read the detailed reference" : "Read the Detailed Reference";
    panel.querySelector("#seed-status").textContent = "";
    panel.querySelector("#prompt-status").textContent = "";
    panel.querySelector("#seed-status").classList.remove("error");
    panel.querySelector("#prompt-status").classList.remove("error");
    panel.querySelector("#info-state").textContent = item.entry ? "Command syntax" : "Workflow details";
    if (item.entry) {
      const help = document.createElement("p");
      help.className = "ws-availability";
      help.textContent = isHandoff() ? "Handoff exports an approved snapshot; it does not start a lifecycle or authorize deployment." : assessment() ? "Read-only assessment; no deployment profile applies. Existing investigations recover their recorded scope and approvals." : isResume() ? "Resume uses the project's recorded profile." : state.command === "iteration" ? "Recover existing configuration and confirm this iteration's stopping point." : "TWTTY confirms missing or changed delivery intent during startup.";
      panel.querySelector("#info-body").append(help);
    }
    if (human) {
      if (!positionHumanInfo()) return;
      panel.show();
      panel.querySelector("#close-info").focus({ preventScroll: true });
    } else {
      panel.showModal();
    }
    panel.scrollTop = 0;
  }
  function render(notice = "") {
    closeInfo(false);
    panel.querySelectorAll(".ws-availability").forEach(item => item.remove());
    root.dataset.command = state.command;
    root.dataset.kind = state.kind;
    root.dataset.profile = isHandoff() ? "not-applicable" : isResume() ? "recovered" : state.profile || "unresolved";
    root.querySelector("[data-delivery-choice]").hidden = isHandoff();
    root.querySelectorAll("[data-command]").forEach(button => button.setAttribute("aria-pressed", String(button.dataset.command === state.command)));
    root.querySelectorAll('input[name="project-type"]').forEach(input => { input.checked = input.value === state.kind; });
    root.querySelectorAll("[data-profile]").forEach(button => {
      button.disabled = !canSelectProfile();
      button.setAttribute("aria-pressed", String(canSelectProfile() && button.dataset.profile === state.profile));
    });
    root.querySelector("#outcome-title").textContent = assessment() ? "Read-only Investigation - No App Deployment" : isResume() ? "Delivery Intent Is Recovered by TWTTY" : "Project Delivery Intent";
    root.querySelector("#profile-note").textContent = assessment() ? "Assessment preserves its read-only boundary; app/emulator/deployment stages do not apply." : isResume() ? "Your local contribution does not change shared project delivery. TWTTY recovers remaining tasks and CI/CD obligations; no new deployment choice or checkpoint argument is required." : state.command === "iteration" ? "TWTTY recovers project configuration and asks only about missing or changed stopping-point decisions. These cards illustrate intent, not new command flags or deployment approval." : "Agree the project's stopping point during discovery. Both profiles can need approved cloud development services. Shared CI/CD does not create a deployment workflow for each teammate.";
    const status = root.querySelector("[data-flow-status]");
    const unsupported = isHandoff() && assessment();
    const message = notice || (unsupported ? "Handoff is not supported for Reverse Engineering. Use Resume to continue the read-only assessment." : "");
    status.textContent = message || `${types[state.kind]} - ${commands[state.command].name}`;
    status.classList.toggle("error", Boolean(message));
    const visible = region => activities.filter(item => item.region === region && matches(item));
    const human = visible("human"), guided = visible("guided");
    const execute = guided.find(item => item.id === "execute");
    const runtime = isHandoff() ? "" : assessment() ? `<div class="spine">${node({ id: "assessment", title: "Verify Assessment Outputs", caption: "Read-only evidence, findings and limitations." })}</div>` : `
      <section class="v20-outer" aria-labelledby="preparation-title">
        <h4 id="preparation-title">${isResume() ? "Set Up Only What You Need" : "1. Set Up the Development Environment"}</h4>
        <p>${isResume() ? "Run these steps only for selected setup/run or work that needs them, not to resume SPEC/PLAN. Reuse working tools and services; ask for any approval not already granted." : "Prepare required tools and packages, then services and application connection settings in the approved starting branch, before creating app-worker branches or implementing the app and its AI evaluation tests."}</p>
        <div class="spine">${spine(visible("preparation"))}</div>
      </section>${arrow}
      <section class="fork single-lane" aria-label="Application activities after required preparation">
        <div class="lane">
          <h4 class="lane-label">${isResume() ? "Run and Verify Locally (When Selected)" : state.kind === "dataeng" ? "2. Develop and Verify the Pipeline" : "2. Develop and Verify the Application"}</h4>
          ${spine(visible("app"))}
          <div class="loop">${state.kind === "dataeng" ? "Edit &rarr; Run &rarr; Verify Results &rarr; Repeat" : "Edit &rarr; Build/Test &rarr; Run/Debug &rarr; Repeat"}</div>
          <p class="lane-note">Run only the steps your approved work needs. Reuse valid results and follow the current risk level and policies. Required service access must work before you report the app as verified.</p>
        </div>
      </section>`;
    const shared = !assessment() && !isHandoff() && (state.profile === "shared" || isResume());
    const deliveryHeading = isResume() ? "h3" : "h4";
    const cloud = shared ? `<section class="v20-outer" aria-labelledby="outer-loop-title"><${deliveryHeading} id="outer-loop-title">${isResume() ? "Cloud Delivery (Only for Recovered Approved Work)" : "3. Build and Deploy (When Approved)"}</${deliveryHeading}><p>${isResume() ? "These steps apply only if the recovered project requires cloud delivery and the current work is authorized to continue it. Local setup/run does not authorize deployment. " : ""}Continuous integration (CI) runs the required build and verification checks. Approved continuous delivery/deployment (CD) workflows manage cloud releases. Your local work does not grant deployment permission.</p><div class="spine">${spine(outer)}</div></section>` : "";
    const localFinish = visible("finish").filter(item => item.id === "local-end");
    const work = execute ? `${arrow}<section class="ws-execution" aria-label="EXECUTE activities">
      <h3 class="ws-execution-heading">${node(execute)}</h3>
      <div class="ws-execution-content">${runtime}${cloud}<div class="spine">${spine(localFinish)}</div></div>
    </section>` : isResume() && !assessment() ? `${arrow}<section class="ws-resume-actions" aria-labelledby="resume-actions-title">
      <h3 id="resume-actions-title">Local Setup and Run (When Selected)</h3>
      <p>Resume can return to any lifecycle stage. These activities run only when your selected action or recovered work needs them; they do not start a new EXECUTE stage.</p>
      ${runtime}
    </section>${cloud}` : runtime + cloud;
    root.querySelector("[data-diagram]").innerHTML = unsupported ? `<p class="dev-note">The investigated target remains read-only. No export or deployment is authorized.</p>` : `<fieldset class="v5-responsibility-group v5-human-work"><legend>Your part</legend><div class="spine">${spine(human)}</div></fieldset>${arrow}<fieldset class="v5-responsibility-group v5-ai-work"><legend>AI-led</legend><p class="v5-ownership-note">${isHandoff() ? "AI prepares and verifies the approved export. You retain control over source, history, destination and publication access." : isResume() ? "The remaining steps depend on the recovered stage/task; runtime setup and lifecycle work run only when needed." : "AI leads discovery, requirements, design and delivery, asking for decisions and approvals when needed."}</p><div class="spine">${spine(guided.filter(item => item !== execute))}</div>${work}<div class="spine">${spine(visible("finish").filter(item => item.id !== "local-end"))}</div></fieldset>`;
    root.querySelectorAll("[data-activity]").forEach(button => button.addEventListener("click", () => openInfo(button)));
    document.querySelectorAll("[data-agentic]").forEach(item => { item.hidden = !agentic(); });
    const entry = document.getElementById("entry-point");
    if (entry) entry.textContent = commands[state.command].name;
    const label = document.getElementById("application-label");
    if (label) label.textContent = types[state.kind];
    updateLinks();
  }
  function read() {
    const url = new URL(location.href);
    const legacy = url.searchParams.get("journey") || url.searchParams.get("entry");
    let command = url.searchParams.get("workflow") || legacy || "new";
    let notice = "";
    if (["setup", "adopt", "contribute"].includes(command)) {
      command = "resume";
      notice = "This older link is now shown through Resume. Explain the existing-project goal; no setup, claim or export is authorized by the link.";
    } else if (command === "hotfix") {
      command = "iteration";
      notice = "State the urgent incident in the change intent. Production recovery still requires explicit incident approval; this link does not open a Hotfix.";
    }
    const kind = url.searchParams.get("project-type") || ((url.searchParams.get("ai") === "true" || url.searchParams.get("app") === "agentic") ? "sdlc-for-agentic-apps" : "sdlc");
    const profile = url.searchParams.get("loop");
    if (!Object.hasOwn(commands, command) || !Object.hasOwn(types, kind) || (profile !== null && !Object.hasOwn(profiles, profile))) notice = "Unknown workflow option. Select one of the displayed commands, project types and delivery intents; no command was executed.";
    state = { command: Object.hasOwn(commands, command) ? command : "new", kind: Object.hasOwn(types, kind) ? kind : "sdlc", profile: Object.hasOwn(profiles, profile) ? profile : null };
    if (isResume() || isHandoff() || assessment()) {
      state.profile = null;
      if (profile !== null) notice = "This entry uses existing project context; the link's delivery choice is ignored. Resume cannot override project delivery, Handoff is not deployment, and assessment remains read-only.";
    }
    if (url.searchParams.has("deploy") || url.searchParams.has("setup") || url.searchParams.has("checkpoint")) notice = "Unsupported deployment/checkpoint inputs. Use one of the four commands and describe the intended outcome.";
    render(notice);
  }
  function sync() {
    history.pushState(null, "", stateUrl(location.href));
    render();
  }
  root.querySelectorAll("[data-command]").forEach(button => button.addEventListener("click", () => {
    if (state.command !== button.dataset.command) state.profile = null;
    state.command = button.dataset.command;
    sync();
  }));
  root.querySelectorAll("[data-profile]").forEach(button => button.addEventListener("click", () => {
    state.profile = button.dataset.profile;
    sync();
  }));
  root.querySelectorAll('input[name="project-type"]').forEach(input => input.addEventListener("change", () => {
    state.kind = input.value;
    if (assessment()) state.profile = null;
    sync();
  }));
  panel.querySelector("#close-info").addEventListener("click", () => closeInfo());
  panel.addEventListener("cancel", event => {
    event.preventDefault();
    closeInfo();
  });
  document.addEventListener("keydown", event => {
    if (event.key === "Escape" && panel.open) {
      event.preventDefault();
      closeInfo();
    }
  });
  document.addEventListener("focusin", event => {
    if (panel.open && panel.dataset.popupLayout === "anchored" && !panel.contains(event.target) && !opener?.contains(event.target)) closeInfo(false);
  });
  addEventListener("resize", () => {
    if (panel.open && panel.dataset.popupLayout === "anchored") positionHumanInfo();
  });
  addEventListener("scroll", () => {
    if (panel.open && panel.dataset.popupLayout === "anchored") positionHumanInfo();
  }, { passive: true });
  panel.querySelector("#seed-text").addEventListener("input", event => {
    drafts.set(draftKey, event.target.value);
    panel.querySelector("#seed-status").textContent = "";
  });
  async function copy(source, feedback, label) {
    const field = panel.querySelector(source), status = panel.querySelector(feedback);
    const human = panel.dataset.popupLayout === "anchored";
    try {
      if (!navigator.clipboard?.writeText) throw new Error("Clipboard access unavailable.");
      await navigator.clipboard.writeText(field instanceof HTMLTextAreaElement ? field.value : field.textContent);
      status.classList.remove("error");
      status.textContent = human
        ? label === "Command" ? "Copied." : "Copied. Paste into your seed file or the iteration's SEED discussion."
        : `${label} copied. Replace the example paths before starting real work.`;
    } catch (error) {
      console.warn(`${label} copy unavailable.`, error);
      status.classList.add("error");
      const name = human && label !== "Command" ? "seed text" : label.toLowerCase();
      status.textContent = `Clipboard unavailable. Select the ${name} and copy it manually.`;
    }
  }
  panel.querySelector("#copy-seed").addEventListener("click", () => copy("#seed-text", "#seed-status", "Seed or intent"));
  panel.querySelector("#copy-prompt").addEventListener("click", () => copy("#prompt-text", "#prompt-status", "Command"));
  function reveal(hash = location.hash) {
    const target = document.getElementById(hash.slice(1));
    for (let parent = target?.closest("details"); parent; parent = parent.parentElement?.closest("details")) parent.open = true;
    const stage = target?.closest("[data-stage-panel]");
    if (stage) activate(stage.dataset.stagePanel);
  }
  const tabs = [...document.querySelectorAll("button[data-stage]")];
  function activate(stage, focus = false) {
    tabs.forEach(tab => {
      const selected = tab.dataset.stage === stage;
      tab.setAttribute("aria-selected", String(selected));
      tab.tabIndex = selected ? 0 : -1;
      if (selected && focus) tab.focus();
    });
    document.querySelectorAll("[data-stage-panel]").forEach(panel => { panel.hidden = panel.dataset.stagePanel !== stage; });
  }
  tabs.forEach((tab, index) => {
    tab.addEventListener("click", () => {
      activate(tab.dataset.stage);
      const url = new URL(location.href);
      url.hash = tab.dataset.stage;
      history.pushState(null, "", url);
    });
    tab.addEventListener("keydown", event => {
      let next = index;
      if (event.key === "ArrowRight") next = (index + 1) % tabs.length;
      else if (event.key === "ArrowLeft") next = (index + tabs.length - 1) % tabs.length;
      else if (event.key === "Home") next = 0;
      else if (event.key === "End") next = tabs.length - 1;
      else return;
      event.preventDefault();
      activate(tabs[next].dataset.stage, true);
      const url = new URL(location.href);
      url.hash = tabs[next].dataset.stage;
      history.pushState(null, "", url);
    });
  });
  document.addEventListener("click", event => {
    const link = event.target.closest("a[href]");
    if (!link) return;
    updateLinks();
    const url = new URL(link.href);
    if (url.origin === location.origin && url.pathname === location.pathname) reveal(url.hash);
  });
  const toggle = document.getElementById("toggle-nav"), nav = document.getElementById("page-nav");
  if (toggle && nav) {
    const query = matchMedia("(max-width: 759px)");
    function updateNav() {
      toggle.hidden = !query.matches;
      nav.hidden = query.matches && toggle.getAttribute("aria-expanded") !== "true";
    }
    toggle.addEventListener("click", () => {
      toggle.setAttribute("aria-expanded", String(toggle.getAttribute("aria-expanded") !== "true"));
      updateNav();
    });
    nav.addEventListener("click", event => {
      if (event.target.closest("a")) {
        toggle.setAttribute("aria-expanded", "false");
        updateNav();
      }
    });
    query.addEventListener("change", updateNav);
    updateNav();
  }
  addEventListener("popstate", () => { read(); reveal(); });
  addEventListener("hashchange", () => reveal());
  read();
  reveal();
})();
