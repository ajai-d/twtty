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

# TWTTY runtime config — <REPLACE: project name>

This folder holds **this project's complete TWTTY configuration**, copied from the full
baseline config tree and merged with its active specialization's additions. It includes
default profiles as well as overrides. This project can change settings locally without
editing or depending on the shared methodology's config files.

> Keep this file in sync when the configuration changes. Unchanged configuration is
> reused; it does not require another full interview or a new copy of the library.

## How it works

- **Review after copying.** Initial config is materialized as a draft, then its actual
  effective settings/files are offered as **Use these settings / Customize settings**
  within Discovery. Model/stack choices still awaiting PLAN are provisional. Resolve
  requested edits before `meta/config`; unchanged approved settings need no repeat prompt.
- **Complete folder structure.** All baseline config files/folders and the active
  specialization's config tree are present, including unchanged defaults and unselected
  profiles. Source inheritance was composed during initial resolution, not deferred to
  execution.
- **`default-config.md` is the complete adopted default configuration.** Baseline and
  specialization defaults were composed by key, including nested mappings. It is a local
  initialization/reset reference, not an automatic fallback for missing runtime settings.
- **`runtimeconfig.md` is the complete effective configuration.** It uses the same binding
  keys and nesting as the local default configuration, with this project's approved
  override values substituted. Settings equal to defaults remain present. Runtime-only
  selections, such as the assessed risk level, are recorded as they become known.
- **Overrides remain supported.** Change the relevant effective setting or customize the
  local profile it selects. Explicitly overridden setting names and customized profiles
  are recorded in `meta/config`; there is no second authoritative list of current values.
- **Local references.** Config-file paths resolve relative to the file containing them
  and remain inside this project's config tree. Spec-defined settings, such as a product
  cost budget, can reference this project's own spec. Shared methodology/vendor links are
  documentation, not sources of missing runtime configuration.
- **Environment paths and ownership.** The development profile's infrastructure/recipe
  paths resolve from the product root, not this config folder. Local-development Azure
  dependencies and local services belong to the local environment when newly owned;
  shared stages retain their own IaC. Consuming an existing service does not transfer
  ownership. Follow the approved PLAN and profile; no automatic migrations.
- **Development procedure.** The profile selected by `development` in `runtimeconfig.md`
  owns setup, service reuse, Resume and worker preparation. Follow that project-owned
  procedure rather than copying it here. PLAN records app-specific decisions; native
  manifests/locks and existing recipes hold the implemented requirements.
- **Services are not hosting.** `Runtime target: N/A` means no cloud application hosting,
  not no Azure services. Enable only approved needed stages/recipes; copied defaults
  and listed paths are not provisioned resources or runnable tooling.
- **App connection settings are not TWTTY configuration.** Follow the bound development
  profile's storage/loading policy; service bindings belong to the app's runtime settings,
  not these profiles/logs. Credentials use the approved identity/secret store.
- **No silent fallback.** A missing required setting or config file is an incomplete
  configuration to resolve explicitly. Do not read current shared defaults to fill it.
- **No automatic upgrades.** An approved refresh can adopt newer defaults. Preserve
  explicit overrides and customized files; surface conflicts before changing them.
  Older overrides-only projects need explicit materialization from their adopted
  defaults and existing overrides, not silent use of a newer library.

## This project's settings

<REPLACE: identify the active specialization, adopted default source, and any explicitly
overridden settings/customized profiles. Current effective values live in runtimeconfig.md
and its local profiles, not a duplicate settings table here. If there are no overrides,
write "No explicit overrides; runtimeconfig.md contains the complete adopted defaults."
>

## How to change a binding

1. **Pick the attribute** (for example `cloud`, `devtools`, `risk-calibration`).
2. **Use or customize the local file** under the matching sub-folder, retaining the
   binding's schema and applicable controls. New config files must also be project-local.
3. **Update its value in `runtimeconfig.md`**, retaining the default configuration's key
   structure. Validate the effective selection and obtain any required approval.
4. **Record and commit** the authorized change with the project and append `meta/config`.
   Later runs use the updated project config.

To **reset an override**, explicitly restore its adopted default value and applicable
local profile, validate it, and record the update. Do not delete the setting to trigger
fallback. Refreshing to newer defaults is a separate approved action.

## Rules

- This folder is **committed with the project** and version-controlled — it is part of the
  project's reproducible record, and the active iteration's `meta/config` replay-log entry
  pins the effective bindings.
- **Never put secrets here** (API keys, tokens, connection strings, webhook URLs). Bindings
  *select* providers and *reference* configuration; credentials belong in your secret
  store, per TWTTY's no-secrets rule.
- Configuration values do not themselves grant Autopilot, Parallel execution, or approval
  for trust-boundary actions. Existing risk, policy, and compliance controls still apply.
- Reuse this scope's recorded Sequential/Parallel Human answer from Discovery at PLAN
  and Resume; do not ask twice. Sequential is normal. Domain/parallel branches follow
  the approved topology, and concurrent writers never share a branch or checkout.
- Shared TWTTY defaults are consulted only for initial resolution or an explicit approved
  refresh/materialization. Ordinary execution uses this project-owned copy.
