# UX quality bar — default profile

**Category:** `ux` · **Status:** default

## What this binds

The **UX policy** for any iteration that ships user-facing UI — configurable knobs applied
through [SDLC §10](../../sdlc.md#10-ux-quality-bar). The [UX control matrix](../risk-calibration/default.md#718-ux-controls) is
authoritative for UX outcomes and default level applicability. This binding is an overlay:
it may strengthen those controls but does not satisfy or redefine them. It is
specialization-agnostic and governs UX *policy*. Every
UI-affecting iteration uses a bound UX/design skill's complete authored process for the
affected UI surface and records the design artifacts under `plan.md §2.6` /
`plan/wireframes/` for the baseline or `plan/wireframes/<iteration-id>/` for a
later Iteration. Affected surfaces always receive current incremental artifacts;
prior approved artifacts are inputs or references and are never overwritten.
Unchanged screens and themes may retain previously approved artifacts only
under the [SDLC §10 impact rule](../../sdlc.md#ux-impact-analysis); transitive
visual changes invalidate reuse.

`cloud: none` (local-only) does not exempt a UI-shipping iteration from its level-calibrated bar.

## Knobs and defaults

| Knob | Default | Notes / override direction |
|------|---------|----------------------------|
| `accessibility-target` | `accessible-defaults; WCAG 2.2 AA when UX-008 is selected` | Accessible platform/component defaults always apply; when `UX-008` is selected, overrides are up only (for example, AAA), never below AA. |
| `automated-a11y` | `required when UX-009 is selected` | When selected, axe-core, WAVE, or equivalent gates merges. |
| `design-skill` | `required` | A UX/design skill MUST be bound and used through its full authored process for every affected UI surface at every level. |
| `html-prototype` | `required` | Requires the interactive prototype defined by `UX-003` in the [UX control matrix](../risk-calibration/default.md#718-ux-controls). The existing key is retained for compatibility, not to prescribe a frontend framework. Unchanged approved prototypes may be retained under the [SDLC §10 impact rule](../../sdlc.md#ux-impact-analysis). |
| `design-quality-scan` | `required-when-available` | Available deterministic design-quality checks pass clean on affected prototypes before `PLAN-EXIT` at every level. |
| `rendered-evidence` | `required` | Each affected primary-screen prototype is actually rendered and approved under UX-005: Human approval, or its explicitly delegated L1 Autopilot AI-review route. Never label AI review as Human attestation. Unchanged approved evidence may be retained under the [SDLC §10 impact rule](../../sdlc.md#ux-impact-analysis). |
| `themes` | `all-designs-must-pass` | Each affected shipped theme passes the design-quality scan and has rendered evidence; a token, component, or other transitive visual change makes every impacted theme affected. Each affected theme also meets the accessibility target when `UX-008` is selected. |
| `usability-test` | `N>=3 when UX-010 is selected and shipping to users` | `UX-010` supplies the Nielsen review and lightweight-study requirement. |
| `design-system` | `none` | Empty means the AI Agent proposes a named system at PLAN at every level; set a value to pin one. |
| `ux-mode-default` | `interview` | The confirmed UX mode (Delegated / Interactive / N/A) is chosen per scope via the §3.2 shared mode-selection mechanic; this only seeds the default. |

## Ratchet rule

`policies/`, any confirmed `compliance/` regime, and the selected risk-policy column may
raise these controls (e.g. force `AAA`, mandate a usability test); they may never relax
them below the defaults above.

## How the AI Agent uses this file

Apply the purpose-led craft bar in `UX-002`, not a mandatory cinematic style, animation
toolkit or rejection of familiar dashboards. Interactive prototypes may simulate services;
a real backend, database, Azure deployment or model call is not a PLAN prerequisite.

This profile supplies initial defaults and is copied with the whole config tree into the
project. Apply approved knob overrides in the project-local UX profile and retain the
`ux` binding's default-config path structure in `runtimeconfig.md`. Materialize effective
knob values in that local profile rather than depending on this shared file to fill
missing values during execution. Later runs reuse the project profile; adopting updated
defaults requires an explicit refresh that preserves overrides. These knobs may raise
thresholds or add steps; they do not weaken selected controls or change their level
applicability.
