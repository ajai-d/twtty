# Technical stack

**Category:** `technical-stack` · **Status:** empty by default

This folder is **empty by default**. With no stack bound (`technical-stack: none`), the AI
Agent **proposes current, appropriate technology choices** during PLAN for Human User
approval — researching current standards rather than relying on a hardcoded stack.

## When to bind a stack

Add a stack file (e.g. `technical-stack/dotnet-azure.md`, `technical-stack/node-azure.md`)
and point `runtimeconfig.md` at it when your organization **pins** approved languages,
frameworks, versions, libraries, and patterns. A bound stack constrains the PLAN technology choices: the AI
Agent MUST choose within it (or `Escalate` with rationale if the spec cannot be satisfied
within the pinned stack).

## Suggested contents of a stack file

- Approved languages + versions; framework(s); package manager.
- Standard libraries for cross-cutting concerns (logging, config, auth, HTTP, data access).
- Build/test tooling; lint/format config.
- Design-system / UI stack (pairs with `reusable-assets/skills` for UX).
- Any banned dependencies or patterns.

Keep it a list of **choices**, not a rationale essay; the plan records why the stack fits
the project.

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
