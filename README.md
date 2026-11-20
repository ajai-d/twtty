# TWTTY™ - Tell Me What To Tell You

TWTTY is an intent-driven engineering framework built for **teams developing production-grade applications**. You describe what you want to build, and AI plans, builds and tests the app, then deploys it when approved. Your team retains control over scope, approvals and consequential decisions.

**[Explore the interactive TWTTY guide](https://ajai-d.github.io/twtty/)** for setup, workflows and reference.

*The HTML guides are published on GitHub Pages.*

## Quick start

Clone or download this repository, then open it alongside your project in an AI coding assistant with file access. No TWTTY executable is installed; the commands below are assistant prompts, not shell commands.

To start building an agentic app, replace the placeholders with your full paths and paste the following prompt into your AI coding assistant:

```text
Read "<full-path-to-twtty.md>" and run: twtty start project type=sdlc-for-agentic-apps project="<project-folder>"
```

For example, with Windows paths:

```text
Read "C:\projects\twtty\framework\twtty.md" and run: twtty start project type=sdlc-for-agentic-apps project="C:\projects\clinic-appointment-assistant"
```

The assistant helps capture your project's intent and asks for the required approvals before execution. Each prompt below includes the required framework-read instruction. TWTTY asks focused questions, defines requirements, plans the work, then guides approved implementation and verification. It records decisions and progress so you can resume later.

| I want to... | Complete assistant prompt |
|---|---|
| Start a project | `Read "<full-path-to-twtty.md>" and run: twtty start project type=<project-type> project="<project-folder>"` |
| Continue or join a project | `Read "<full-path-to-twtty.md>" and run: twtty resume project="<project-folder>"` |
| Start a feature or fix after the initial baseline is complete | `Read "<full-path-to-twtty.md>" and run: twtty start iteration project="<project-folder>"` |
| Prepare a handoff to transition the project to another team or customer | `Read "<full-path-to-twtty.md>" and run: twtty handoff project="<project-folder>"` |

Replace `<full-path-to-twtty.md>` with the absolute path to the framework's `twtty.md` file inside its `framework` directory, including the filename, not just a folder. Replace `<project-folder>` with the absolute path to your product root. Keep both paths in quotes. `project=` is the product root, not its `twtty` subfolder.

During application work, the assistant treats the TWTTY framework checkout as read-only; your project's copied configuration remains editable under its normal approvals. Framework changes require an explicit maintenance request. This is assistant guidance, not a filesystem lock.

Choose `<project-type>` when starting a project:

| Project type | `type=` value | Use it to... |
|---|---|---|
| Software development | `sdlc` | Build traditional applications or refactor existing applications through a structured delivery lifecycle. |
| Agentic AI applications | `sdlc-for-agentic-apps` | Build Agentic AI apps with tool integrations, evaluations and safety controls. |
| Data engineering | `dataeng` | Build data pipelines and platforms with data quality and governance controls. |
| Reverse engineering | `reverse-engineering` | Assess and document an existing system without modifying the investigated code. |

---

## Responsible use and production readiness

Before production use, applications built or modified with TWTTY must meet the testing, security, privacy and release requirements appropriate to their intended use and risk. For AI applications, this includes applicable AI safety and responsible AI evaluations, including jailbreak and prompt-injection testing where relevant. Users remain responsible for validating, deploying and operating their applications.

## Attribution and license

Original Creator & Lead Architect: **Ajai Peddapanga**.

Copyright 2026 Ajai Peddapanga. First-party code, configuration, templates, documentation, methodology and artwork are offered under [Apache License 2.0](LICENSE). See [AUTHORS](AUTHORS.md), [NOTICE](NOTICE) and [branding information](TRADEMARKS.md).

TWTTY is provided "AS IS", without warranties, subject to the warranty disclaimers and liability limitations in the [Apache License 2.0](LICENSE).

AI-generated outputs may be incorrect, incomplete or unsafe; validate results before use. TWTTY does not guarantee accuracy, security, regulatory compliance or production suitability.

TWTTY is not officially sponsored or endorsed by Microsoft. Beta availability does not imply production readiness or enterprise certification.

TWTTY is currently in beta.
