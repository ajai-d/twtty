"""Prompt-contract regressions and Git-selection integration checks, not live agent execution."""

from collections import Counter
import hashlib
import os
from pathlib import Path, PureWindowsPath
import re
import shutil
import subprocess
import tempfile
import unittest
from urllib.parse import unquote, urlsplit
import zipfile


ROOT = Path(__file__).resolve().parents[1]
SDLC = ROOT / "framework" / "methodology" / "specialized-implementations" / "sdlc"

def read(path):
    return path.read_text(encoding="utf-8")


def git(root, *args, env=None):
    return subprocess.run(
        ["git", "--no-pager", "-C", str(root), *args],
        check=True, capture_output=True, env=env,
    ).stdout


def subsection(text, heading):
    tail = text.split(heading, 1)[1]
    return re.split(r"^#{2,3} ", tail, maxsplit=1, flags=re.MULTILINE)[0]


def anchors(text):
    result = set()
    for heading in re.findall(r"^#{1,6} (.+)$", text, re.MULTILINE):
        slug = re.sub(r"[^\w -]", "", heading.lower()).replace(" ", "-")
        result.add(slug)
    result.update(re.findall(r'\bid=["\']([^"\']+)["\']', text))
    return result


class ProtocolContracts(unittest.TestCase):
    def test_framework_read_only_rule_preserves_authorized_project_writes(self):
        dispatcher = " ".join(subsection(
            read(ROOT / "framework" / "twtty.md"),
            "## What the AI Agent MUST do on any `twtty` command"
        ).split())
        for guard in ("On every command", "framework checkout as read-only",
                      "core-twtty-methodology.md#45-rules",
                      "explicit Human User request for framework maintenance",
                      "application approvals and Autopilot grants do not",
                      "Project-owned configuration and approved Handoff exports"):
            with self.subTest(dispatcher=guard):
                self.assertIn(guard, dispatcher)
        rules = subsection(read(ROOT / "framework" / "methodology" /
                                "core-twtty-methodology.md"), "### 4.5 Rules")
        heading = "- **Protect the framework source.**"
        self.assertIn(heading, rules)
        protection = " ".join(rules.split(heading, 1)[1].split("\n- **", 1)[0].split())
        for guard in ("During application work",
                      "selected TWTTY framework checkout as read-only",
                      "MUST NOT create, edit, delete or move framework files",
                      "automatically update the checkout",
                      "explicit Human User request for framework maintenance",
                      "application approvals and Autopilot grants do not",
                      "outputs and tool caches outside the framework checkout",
                      "Project-owned configuration copies and artifacts remain editable",
                      "existing approvals",
                      "Handoff MAY write to explicitly approved export destinations "
                      "outside the framework checkout",
                      "not filesystem enforcement or a security boundary"):
            with self.subTest(core=guard):
                self.assertIn(guard, protection)
        self.assertIn("assistant guidance, not a filesystem lock", read(ROOT / "README.md"))

    def test_documented_bootstrap_path_resolves_to_shared_framework(self):
        invocation = subsection(read(ROOT / "framework" / "twtty.md"), "## How to invoke")
        self.assertIn('Read "<full-path-to-twtty.md>" and run: <command>', invocation)
        self.assertIn("including the filename", invocation)
        for source, text in (("README", read(ROOT / "README.md")),
                             ("dispatcher", invocation)):
            with self.subTest(source=source):
                examples = re.findall(r'^Read "([A-Za-z]:\\[^"]+)" and run:',
                                      text, re.MULTILINE)
                self.assertEqual(len(examples), 1)
                dispatcher = ROOT.joinpath(*PureWindowsPath(examples[0]).parts[-2:])
                self.assertTrue(dispatcher.is_file(),
                                f"Missing documented dispatcher: {dispatcher}")
                for relative in ("methodology/core-twtty-methodology.md",
                                 "templates/seed-prompt-template.md"):
                    self.assertTrue(dispatcher.parent.joinpath(relative).is_file(),
                                    f"Missing bootstrap dependency: {relative}")
        handoff = read(SDLC / "templates" / "handoff-template.md")
        self.assertIn('Read "<full-path-to-twtty.md>" and run: twtty resume', handoff)

    def test_framework_build_configuration_is_not_ignored(self):
        for path, expected in (
            ("framework/methodology/specialized-implementations/sdlc/config/"
             "tokenomics/build/build-profile1.md", 1),
            ("build/twtty-test-output", 0),
        ):
            with self.subTest(path=path):
                result = subprocess.run(
                    ["git", "-C", str(ROOT), "check-ignore", "--no-index", "--", path],
                    capture_output=True, text=True,
                )
                self.assertEqual(result.returncode, expected, result.stdout + result.stderr)

    def test_exactly_four_commands_without_legacy_aliases(self):
        dispatcher = read(ROOT / "framework" / "twtty.md")
        commands = dispatcher.split("## Commands", 1)[1].split("## Parameters", 1)[0]
        rows = re.findall(r"^\| `twtty ([^`]+)` \|", commands, re.MULTILINE)
        self.assertEqual(rows, ["start project", "resume", "start iteration", "handoff"])
        for guard in ("unknown/duplicate", "malformed quotes", "conflicting parameters",
                      "only when explicitly requested", "No `deploy` or `checkpoint`",
                      "accept exactly the four commands", "no aliases or additional entrypoints",
                      "Reject removed spellings before mutation"):
            self.assertIn(guard, dispatcher)
        surfaces = [ROOT / "README.md", *sorted((ROOT / "framework").rglob("*.md")),
                    *sorted((ROOT / "docs").rglob("*.html"))]
        for path in surfaces:
            text = read(path)
            for removed in ("twtty contribute", "twtty start work", "twtty start hotfix"):
                with self.subTest(path=path.relative_to(ROOT), removed=removed):
                    self.assertNotIn(removed, text)
        parameters = subsection(dispatcher, "## Parameters")
        self.assertNotRegex(parameters, r"(?m)^- \*\*`(?:iteration|domain)=")
        self.assertIn("do not accept `iteration=` or `domain=` command parameters", parameters)

    def test_resume_pickup_requires_explicit_intent_and_preserves_claim_safeguards(self):
        dispatcher = read(ROOT / "framework" / "twtty.md")
        pickup = " ".join(subsection(dispatcher, "## Explicit work pickup during Resume").split())
        for guard in ("Only when the Human explicitly requests",
                      "`twtty resume`", "MUST NOT create an Iteration",
                      "replace an existing assignment without explicit Human direction",
                      "apply any Iteration/domain constraints",
                      "Exclude paused Iterations", "Human User to select the work",
                      "refresh remote state and re-check eligibility",
                      "draft change request as the claim", "Never run concurrent writers",
                      "if another claim won", "unbounded polling loop"):
            self.assertIn(guard, pickup)
        method = " ".join(read(SDLC / "sdlc.md").split())
        self.assertIn("Ordinary Resume never scans/ranks global assignments", method)
        guide = read(ROOT / "docs" / "life-cycle-workstation.html")
        for guard in ("Ordinary Resume never scans for new assignments.",
                      "Claim only explicitly requested pickup.",
                      "Human selection and refreshed dependency/claim/pause/footprint "
                      "checks precede the shared draft-PR claim."):
            self.assertIn(guard, guide)
        core = read(ROOT / "framework" / "methodology" / "core-twtty-methodology.md")
        self.assertIn("work-pickup discovery during Resume", core)

    def test_incident_intent_routes_before_iteration_creation_without_losing_controls(self):
        dispatcher = read(ROOT / "framework" / "twtty.md")
        incident = " ".join(subsection(dispatcher,
                                      "## Production-incident routing on Start iteration").split())
        for guard in ("`twtty start iteration`", "explicit urgent production-incident",
                      "before ordinary Iteration creation", "Do not generate an Iteration ID",
                      "active specialization defines a Hotfix path",
                      "confirmed production incident", "explicit Human User approval",
                      "even under Autopilot", "one commit", "draft hotfix PR",
                      "both are remotely discoverable", "partial opening MUST Escalate",
                      "Ambiguous incident intent needs clarification",
                      "Existing Hotfix Scopes continue through ordinary Resume",
                      "rewrites history or abandons a pause"):
            self.assertIn(guard, incident)
        core = read(ROOT / "framework" / "methodology" / "core-twtty-methodology.md")
        iteration = " ".join(subsection(core, "### 4.3 On new Iteration").split())
        self.assertLess(iteration.index("explicit urgent production-incident intent"),
                        iteration.index("Before creating an Iteration"))
        method = " ".join(subsection(read(SDLC / "sdlc.md"),
                                     "### 3.5 Hotfix path (production incident fast path)").split())
        for guard in ("Entry through Start iteration", "inherited", "one commit",
                      "meta/iteration-pause", "every applicable inherited task",
                      "HOTFIX-EXIT", "same Iteration/Hotfix pair"):
            self.assertIn(guard, method)

    def test_resume_uses_selected_context_not_global_assignment_discovery(self):
        core = read(ROOT / "framework" / "methodology" / "core-twtty-methodology.md")
        resume = core.split("### 4.1 ", 1)[1].split("### 4.2 ", 1)[0]
        for guard in ("ask the Human User once", "selected scope", "not routine Resume",
                      "Missing execution logs", "only for an explicit new-project request",
                      "not an automatic", "recipient's authorization"):
            with self.subTest(guard=guard):
                if guard == "not an automatic":
                    self.assertIn("never an automatic baseline/iteration", resume)
                else:
                    self.assertIn(guard, resume)
        self.assertNotIn("treated as a single concatenated log", resume)
        self.assertNotIn("read every existing stage artifact", resume)

    def test_resume_selects_actions_after_recovery_and_responsibility(self):
        method = read(SDLC / "sdlc.md")
        resume = " ".join(subsection(
            method, "### 3.6 Existing-project preparation"
        ).split())
        for requirement in (
            "first recovers the selected scope's state",
            "before proposing lifecycle continuation",
            "original approved SEED evidence",
            "Git's last author/committer",
            "ask one focused clarification",
            "same Human or approved successor",
            "continuation only within the current Human's verified claim",
            "do not offer its continuation by default",
            "local setup/run, a new Iteration, or both",
            "does not propose its intent",
            "An unfinished baseline cannot be bypassed",
            "only on an explicit work-pickup request",
            "MUST NOT bypass",
        ):
            with self.subTest(requirement=requirement):
                self.assertIn(requirement, resume)

    def test_resume_preparation_is_selected_action_specific(self):
        resume = " ".join(subsection(
            read(SDLC / "sdlc.md"),
            "### 3.6 Existing-project preparation"
        ).split())
        for requirement in (
            "Check readiness for the selected action",
            "MUST NOT interrupt recovered SPEC/PLAN work",
            "Reuse verified unchanged readiness",
            "obtain uncovered approvals",
            "return to the selected action",
            "blocks only work that needs it",
            "development/default.md#resume-preparation",
            "age alone does not require an update",
            "If a required setting, file or preparation procedure is missing/incompatible",
            "request an approved scoped update preserving overrides",
            "never silently substitute shared defaults",
        ):
            with self.subTest(requirement=requirement):
                self.assertIn(requirement, resume)
        self.assertNotIn("Missing/older config requires", resume)

    def test_resume_preparation_is_separate_from_start_in_configuration(self):
        profile = read(SDLC / "config" / "development" / "default.md")
        preparation = " ".join(subsection(
            profile, "## Resume preparation"
        ).split())
        for requirement in (
            "applies only to local setup/run selected during Resume",
            "Start project and later Iterations keep their existing EXECUTE setup procedure",
            "Other Resume actions prepare only their own missing prerequisites",
            "do not restart the lifecycle, reopen completed work",
            "perform authorized setup through available tools",
            "setup/run selection alone does not authorize",
            "Manual execution is only for a Human-selected route",
            "Never transfer another Human's credentials or authorization",
            "Never request credentials in chat",
            "requirements-and-dependencies",
            "tooling-readiness-and-reuse",
            "application-connection-settings",
            "including actual service/model access",
            "partial readiness",
            "do not substitute samples/mocks",
            "Keep the verified app available",
        ):
            with self.subTest(requirement=requirement):
                self.assertIn(requirement, preparation)
        method = read(SDLC / "sdlc.md")
        execute = subsection(method, "### 3.4 Execute")
        resume = subsection(method, "### 3.6 Existing-project preparation")
        self.assertIn("development/default.md#resume-preparation", resume)
        self.assertNotIn("#resume-preparation", execute)
        self.assertNotIn("### Assisted environment preparation", profile)
        for duplicated_instruction in ("**Assist through completion.**",
                                       "native sign-in initiation",
                                       "UI/startup/health success",
                                       "az login"):
            self.assertNotIn(duplicated_instruction, resume)

    def test_resume_authenticates_then_discovers_and_verifies_real_services(self):
        profile = read(SDLC / "config" / "development" / "default.md")
        preparation = " ".join(subsection(profile, "## Resume preparation").split())
        stages = (
            "1. **Prepare missing tools.",
            "2. **Initiate required sign-in.",
            "3. **Discover before asking for endpoints.",
            "4. **Select reuse and save bindings.",
            "5. **Offer manual configuration when needed.",
            "6. **Provision only an approved remainder.",
            "7. **Run and verify the actual app.",
        )
        offsets = [preparation.index(stage) for stage in stages]
        self.assertEqual(offsets, sorted(offsets))
        for requirement in (
            "az account show",
            "Reuse a usable applicable login",
            "have the AI Agent launch",
            "az login --use-device-code",
            "actual execution environment",
            "Human completes browser authentication",
            "wait for its result before dependent Azure lookups",
            "If the harness cannot support native sign-in",
            "do not assume the default/first account",
            'az account set --subscription "<approved-subscription>"',
            "confirm the authorized subscription/resource-group scope once",
            "rather than asking the Human to transcribe discoverable values",
            "Manual settings do not bypass required app authentication",
            "not proof that a service is absent",
            "obtain uncovered target/identity/RBAC/data/usage-cost consent",
            "execute the bound provider's native apply and wait for its terminal result",
            "billable-call consent",
        ):
            with self.subTest(requirement=requirement):
                self.assertIn(requirement, preparation)

    def test_continuation_assignment_preserves_other_authority_boundaries(self):
        method = read(SDLC / "sdlc.md")
        record = next(
            line for line in method.splitlines()
            if line.startswith("- **`meta/continuation-assignment`**")
        )
        for requirement in (
            "prior SEED/assignment evidence",
            "successor's native Human confirmation",
            "under project policy",
            "not real identities copied into redacted records",
            "never an invented historical starter",
            "before successor lifecycle execution",
            "Contributor claims, historical approvals, paused-state restrictions "
            "and Autopilot grants remain separate",
        ):
            with self.subTest(requirement=requirement):
                self.assertIn(requirement, record)
        self.assertIn("defines nine additional `meta/*` entries", method)

    def test_discovery_delivery_defaults_and_local_provider_selection(self):
        config = read(SDLC / "config" / "default-config.md")
        profile = read(SDLC / "config" / "development" / "default.md")
        self.assertRegex(config, r"(?m)^development:\s+development/default\.md")
        for setting in ("local-execution: native", "ci: required", "cd: disabled",
                        "cloud-environments: []"):
            self.assertIn(setting, profile)
        for choice in ("Develop and test locally, with CI protecting main",
                       "Develop locally and deploy to cloud through CI/CD"):
            self.assertIn(choice, profile)
        discovery = subsection(read(SDLC / "sdlc.md"), "### 3.2 Spec")
        self.assertIn("development/default.md#discovery-and-configuration", discovery)
        self.assertIn("CI-free merge is an explicit policy-permitted exception", profile)
        self.assertIn("Resume and team clones reuse valid settings", profile)
        self.assertIn("does not disable approved Azure development services",
                      read(SDLC / "templates" / "spec-template.md"))

    def test_lean_local_azure_and_hosted_identity_remain_distinct(self):
        azure = read(SDLC / "config" / "cloud" / "azure.md")
        local = " ".join(azure.split("## Local-development dependencies", 1)[1].split(
            "## Stage hooks", 1)[0].split())
        for requirement in ("Azure CLI / Entra", "required provisioning consent",
                            "no mandatory separate", "optional separate preview",
                            "data/cost", "not missing",
                            "does **not** require unrelated CI federation"):
            with self.subTest(requirement=requirement):
                self.assertIn(requirement, local)
        self.assertIn("Cloud hosting stays pipeline-owned", local)
        self.assertIn("Managed Identity", local)
        profile = read(SDLC / "config" / "development" / "default.md")
        self.assertIn("Do not wait", profile)
        self.assertIn("for app work, an eval harness, app CI", profile)

    def test_azure_reuse_is_asked_at_infra_kickoff_and_saves_app_bindings(self):
        azure = read(SDLC / "config" / "cloud" / "azure.md")
        profile = read(SDLC / "config" / "development" / "default.md")
        reuse = " ".join(subsection(profile, "### Development infrastructure first").split())
        for requirement in ("before creation-specific IaC",
                            "at EXECUTE infra kickoff",
                            "not a Discovery prerequisite or a separate gate",
                            "Discover and offer reuse", "Offer manual configuration",
                            "Create only the remainder",
                            "Ask which candidates the Human wants to reuse",
                            "Reuse valid previously selected services/bindings/answers on Resume",
                            "endpoint/connection URLs", "deployment/model names",
                            "application-connection-settings",
                            "Never ask for credentials or credential-bearing URLs",
                            "no implicit modification/redeclaration",
                            "Save returned bindings",
                            "approved design does not restart PLAN"):
            self.assertIn(requirement, reuse)
        self.assertIn("development/default.md#development-infrastructure-first", azure)
        self.assertIn("development/default.md#application-connection-settings", azure)
        discovery = " ".join(subsection(read(SDLC / "sdlc.md"), "### 3.2 Spec").split())
        self.assertIn("not mandatory instance/connection details", discovery)
        self.assertIn("development/default.md#development-infrastructure-first", discovery)
        plan = read(SDLC / "templates" / "plan-template.md")
        self.assertIn("without assuming new\nresources or demanding endpoint values", plan)
        self.assertIn("configuration writes in the infra work footprint", plan)

    def test_connection_settings_have_one_loaded_location_and_no_normal_handoff(self):
        profile = read(SDLC / "config" / "development" / "default.md")
        settings = subsection(profile, "### Application connection settings")
        for requirement in ("Reuse the app's existing runtime-config file",
                            "Do not move working settings or add a competing file",
                            "one ignored `.env.local` at the product repository root",
                            "native convention takes precedence",
                            "ignored before writing actual values",
                            "normal launcher/framework configuration MUST load",
                            "not automatically loaded by every stack",
                            "not a validation\n  wrapper",
                            "No copy, handoff step, repeated reuse question or reprovisioning",
                            "Separate checkout only", "Do not copy the whole environment file"):
            self.assertIn(requirement, settings)
        self.assertIn("not under `twtty/`, `twtty-runtime-config/` or the IaC folder", settings)
        self.assertIn("never actual connection values", settings)
        template = read(ROOT / "framework" / "templates" / "project-readme-template.md")
        self.assertIn("actual app runtime-config path, required key names", template)
        self.assertIn("startup loads it", template)

    def test_tooling_reuse_distinguishes_restore_versions_and_permission(self):
        profile = read(SDLC / "config" / "development" / "default.md")
        tooling = profile.split("### Tooling readiness and reuse", 1)[1].split(
            "## Environment IaC and resource ownership", 1)[0]
        for requirement in ("Available and compatible", "Project dependency restore",
                            "Missing or incompatible version", "Access or restore failure",
                            "supported shared browser/package cache",
                            "actual execution context", "do not downgrade, repin",
                            "current Human User and execution context",
                            "exact action/version or approved range",
                            "source/destination and trust/cost scope", "remain unrevoked",
                            "general Autopilot are not installation consent",
                            "Do not suppress native permission prompts",
                            "Do not couple this prerequisite question to downgrading",
                            "verify the selected version and actual task readiness"):
            with self.subTest(requirement=requirement):
                self.assertIn(requirement, tooling)
        method = read(SDLC / "sdlc.md")
        self.assertIn("tooling-readiness-and-reuse",
                      subsection(method, "### 3.4 Execute"))
        self.assertIn("development/default.md#resume-preparation",
                      subsection(method, "### 3.6 Existing-project preparation"))
        self.assertIn("tooling-readiness-and-reuse",
                      subsection(profile, "## Resume preparation"))

    def test_product_budget_controls_are_conditional_without_waiving_evidence(self):
        agentic = SDLC.parent / "sdlc-for-agentic-apps"
        profile = read(agentic / "config" / "tokenomics" / "product" / "product-profile1.md")
        no_caps = " ".join(profile.split("- **All caps `none`.**", 1)[1].split())
        for requirement in ("Formal verification still records measured usage and machine-readable",
                            "forced-cap tests are not required", "not as a passing test",
                            "an uncapped budget does not waive them"):
            self.assertIn(requirement, no_caps)
        active_caps = " ".join(profile.split("- **Runtime caps + degradation", 1)[1].split(
            "- **All caps `none`.**", 1)[0].split())
        for requirement in ("approved budget", "non-`none` runtime caps",
                            "tests MUST force each applicable cap",
                            "missing/failing required test MUST `Escalate`",
                            "L1 smoke-only still verifies required guards",
                            "Do not invent a cap"):
            self.assertIn(requirement, active_caps)
        template = read(agentic / "templates" / "spec-for-agentic-apps-template.md")
        check = next(line for line in template.splitlines() if line.startswith("6. Section 11"))
        self.assertIn("every approved non-`none` budget threshold", check)
        self.assertIn("not applicable", check)
        self.assertIn("controls remain enforced", check)
        method = read(agentic / "sdlc-for-agentic-apps.md")
        gate = next(line for line in method.splitlines() if line.startswith("8. For affected LLM"))
        for requirement in ("eval-measured tokens/per-request cost", "machine-readable usage",
                            "L1 smoke-only records actual provided usage",
                            "unavailable cost", "not a mandatory eval artifact",
                            "Approved caps/degradation", "Required cap verification must pass",
                            "all-`none` caps", "unrun passing tests"):
            self.assertIn(requirement, gate)
        rule = next(line for line in method.splitlines() if line.startswith("3. Apply EXECUTE-EXIT"))
        for requirement in ("condition 8", "Do not invent caps",
                            "independently approved safety/budget controls"):
            self.assertIn(requirement, rule)
        self.assertNotIn("the app's **degradation-policy** check are gate-blocking", method)

    def test_archived_branch_corrections_cannot_rewrite_evidence(self):
        method = read(SDLC / "sdlc.md")
        rule = next(line for line in method.splitlines() if line.startswith("- **Immutability.**"))
        for requirement in ("MUST NOT be edited, reordered or removed",
                            "before or after archive", "Append corrections to the current scope's log",
                            "exact archived branch entry", "preserving the originals",
                            "never authorizes rewriting replay history", "separate explicit approval"):
            self.assertIn(requirement, rule)
        self.assertNotIn("except through a subsequent branch", rule)
        branch_rules = subsection(method, "#### 8.1.2 Branch-scoped replay logs")
        for requirement in ("<scope-id>-<branch-token>-execution-log.md",
                            "br-<branch-token>-<n>", "project-keyed",
                            "native Git refs and PR head/base metadata remain unchanged",
                            "Existing non-identifying legacy filenames/IDs",
                            "Never silently rename files", "reset counters",
                            "privacy-remediation approval"):
            self.assertIn(requirement, branch_rules)
        self.assertNotIn("MUST equal the branch's full git name", branch_rules)

    def test_build_hard_caps_stop_both_execution_modes_before_overage(self):
        profile = read(SDLC / "config" / "tokenomics" / "build" / "build-profile1.md")
        self.assertIn("both Interactive and Autopilot modes", profile)
        self.assertIn("before continuing", profile)
        self.assertIn("do not defer an overage", profile)
        self.assertNotIn("Interactive mode surfaces the overage at the next gate", profile)
        self.assertIn("before exceeding a cap", read(SDLC / "sdlc.md"))

    def test_readme_matches_closeout_dependencies_and_actual_process_paths(self):
        template = read(ROOT / "framework" / "templates" / "project-readme-template.md")
        closeout = next(line for line in read(SDLC / "sdlc.md").splitlines()
                        if line.startswith("| 3m. Iteration"))
        for obsolete in ("What was actually implemented", "Every control in one table",
                         "The R<n> result", "Continue with TWTTY"):
            self.assertNotIn(obsolete, closeout)
        for requirement in ("MUST complete the applicable", "brief", "actual artifact root",
                            "iteration-execution diagram"):
            self.assertIn(requirement, closeout)
        for requirement in ("necessary developer", "when real cloud dependencies are required",
                            "only if approved and implemented", "Do not introduce mocks",
                            "Resolve the actual approved artifact root", "never move artifacts"):
            self.assertIn(requirement, template)
        self.assertNotIn("works with no cloud credentials", template)
        process_links = re.findall(r"\[[^\]\n]*\]\((twtty/[^)\n]+)\)", template)
        self.assertEqual(set(process_links), {
            "twtty/seed/seed.md", "twtty/spec/spec.md", "twtty/plan/plan.md",
            "twtty/replay-execution/execution-log.md",
        })
        with tempfile.TemporaryDirectory(prefix="twtty-readme-links-") as directory:
            product = Path(directory)
            for relative in ("seed/seed.md", "spec/spec.md", "plan/plan.md",
                             "replay-execution/execution-log.md"):
                path = product / "twtty" / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("Synthetic approved artifact\n", encoding="utf-8")
            for target in process_links:
                self.assertTrue((product / target).is_file(), target)

    def test_stochastic_l1_exception_does_not_lower_other_approved_controls(self):
        agentic = SDLC.parent / "sdlc-for-agentic-apps"
        method = read(agentic / "sdlc-for-agentic-apps.md")
        exception = method.split("**L1 single-sample exception.**", 1)[1].split("\n---", 1)[0]
        for requirement in ("effective approved overlay permits L1", "approved evaluation requirement",
                            "both the L1 prototype acknowledgment",
                            "separate single-sample acknowledgment", "Missing acknowledgment blocks",
                            "never proof of repeatability", "stricter overlay or approved larger N",
                            "do not reduce N, pass rules or quality thresholds",
                            "Other levels require their declared multi-run evidence"):
            self.assertIn(requirement, exception)
        gate = next(line for line in method.splitlines() if line.startswith("7. For affected LLM"))
        self.assertIn("When formal evaluations apply", gate)
        self.assertIn("only the narrowly approved L1 single-sample exception", gate)
        rule = next(line for line in method.splitlines() if line.startswith("6. When formal stochastic"))
        self.assertIn("approved N/pass rule/variance", rule)
        template = read(agentic / "templates" / "spec-for-agentic-apps-template.md")
        check = next(line for line in template.splitlines() if line.startswith("4. Every dimension"))
        self.assertIn("except under", check)
        self.assertIn("both required acknowledgments and no stricter approved N", check)
        self.assertIn("deterministic", template)
        self.assertIn("a single run suffices", template)

    def test_reverse_engineering_discovery_is_explicit_under_either_execution_mode(self):
        reverse = SDLC.parent / "reverse-engineering"
        method = read(reverse / "reverse-engineering.md")
        discovery = method.split("**Discovery mode is explicitly selected", 1)[1].split(
            "Use the [reverse-engineering spec template]", 1)[0]
        for requirement in ("ask the Human User", "before any", "elicitation or drafting",
                            "before\nRound 1", "Honor Interactive",
                            "Autopilot authorization is not an answer"):
            self.assertIn(requirement, discovery)
        for removed in ("Discovery defaults to **Delegated**", "Delegated by necessity",
                        "the only interactive step", "stage task without stopping"):
            self.assertNotIn(removed, method)
        self.assertIn("Interactive Discovery still elicits Human input when selected", method)
        checklist = read(reverse / "templates" / "spec-template.md").split(
            "## SPEC-EXIT validation checklist", 1)[1]
        for requirement in ("put to the Human User", "explicit answer", "before Round 1",
                            "Metadata matches", "Autopilot grant alone does not satisfy"):
            self.assertIn(requirement, checklist)

    def test_agentic_model_default_is_not_duplicated_in_methodology(self):
        agentic = SDLC.parent / "sdlc-for-agentic-apps"
        method = read(agentic / "sdlc-for-agentic-apps.md")
        selection = next(line for line in method.splitlines()
                         if line.startswith("**Agentic technology and framework selection.**"))
        config = read(agentic / "config" / "default-config.md")
        self.assertNotRegex(selection + config, r"\bgpt-[\w.-]+")
        self.assertIn("concrete model choice lives in that profile", selection)
        self.assertIn("do not silently repin", selection)
        self.assertIn("defaults live in the bound agentic-stack profile", config)
        self.assertIn("existing projects retain adopted choices until an approved update", config)

    def test_shared_execution_iac_and_release_artifact_contract(self):
        profile = read(SDLC / "config" / "development" / "default.md")
        for requirement in ("self-contained IaC", "no shared infrastructure-module",
                            "cross-environment module dependency", "one declared deployment owner",
                            "datasets, thresholds", "report schema",
                            "PR code gets no production/deployment credentials",
                            "host `az login` is not automatically available",
                            "Local images are candidates, not release artifacts"):
            with self.subTest(requirement=requirement):
                self.assertIn(requirement, profile)
        for stage in ("local/", "dev/modules/", "qa/modules/", "uat/modules/",
                      "preprod/modules/", "prod/modules/"):
            self.assertIn(stage, profile)
        method = read(SDLC / "sdlc.md")
        hosting = method.split("**Separate infrastructure and application CD (cloud targets).**", 1)[1].split(
            "**Subsequent iterations are incremental", 1)[0]
        for requirement in ("separate workflow/pipeline definitions",
                            "consumes the verified immutable release artifact produced by trusted CI",
                            "promotes the same digest",
                            "MUST fail clearly when prerequisites are missing or incompatible",
                            "shared environment-level deployment lock",
                            "waiting for the other pipeline MUST NOT hold that lock"):
            self.assertIn(requirement, hosting)
        shared = subsection(profile, "## Shared CI and CD")
        self.assertIn("../../sdlc.md#34-execute", shared)
        self.assertNotIn("independently triggerable workflow definitions", shared)
        self.assertNotIn("Coordinate changes/locks", shared)
        azure = read(SDLC / "config" / "cloud" / "azure.md")
        for stage in ("infrastructure CD", "application CD"):
            hook = next(line for line in azure.splitlines()
                        if line.startswith(f"- **EXECUTE ({stage}):**"))
            self.assertIn("../../sdlc.md#34-execute", hook)
            self.assertNotIn("shared environment mutation locking", hook)
            self.assertNotIn("separate, independently triggerable workflow", hook)
        self.assertNotIn("builds or consumes", azure)

    def test_handoff_blocks_required_gaps_and_preserves_authority_boundaries(self):
        handoff = subsection(read(SDLC / "sdlc.md"), "### 3.7 Project handoff")
        for guard in ("private GitHub repository, ZIP, or both, as requested", "Tracked-but-ignored",
                      "not only the latest iteration", "unresolved required gaps block",
                      "Never copy source `.git`", "Sanitize export copies only",
                      "approved history", "LFS", "submodule", "symlink",
                      "outside source and payload", "Stage the requested outputs",
                      "repository/ZIP parity when both are delivered",
                      "safe extraction when a ZIP is delivered",
                      "planned private destination/access when a repository is delivered",
                      "Only then", "Failed checks block publication"):
            with self.subTest(guard=guard):
                self.assertIn(guard, handoff)
        template = read(SDLC / "templates" / "handoff-template.md")
        self.assertIn("twtty resume project=", template)
        self.assertIn("not a deployment authorization", template)
        self.assertIn("payload or claim unrun checks passed", template)
        self.assertIn("unrun recipient/cloud checks remain pending", handoff)

    def test_read_only_assessment_does_not_enter_application_setup(self):
        self.assertIn("Reverse Engineering keeps the investigated target read-only",
                      read(ROOT / "framework" / "twtty.md"))
        self.assertIn("must not install workflows/protection into their investigated target",
                      read(SDLC / "sdlc.md"))

    def test_local_iac_exception_is_enforced_by_the_matrix(self):
        matrix = read(SDLC / "config" / "risk-calibration" / "default.md")
        deployment = matrix.split("## 7.1.4 Deployment", 1)[1].split("## 7.1.5", 1)[0]
        row = next(line for line in deployment.splitlines() if "Approved cloud creation/updates" in line)
        for requirement in ("reviewed IaC", "developer Azure CLI", "approved minimal local-development",
                            "one-time identity bootstrap", "hosting deploys use CD",
                            "No raw resource-create/portal", "explicit approval/logging"):
            self.assertIn(requirement, row)
        self.assertEqual([cell.strip() for cell in row.split("|")[2:-1]], ["MUST"] * 5)
        self.assertNotIn("no dev-machine provisioners", matrix)

    def test_identity_requirements_follow_actual_execution_context(self):
        matrix = read(SDLC / "config" / "risk-calibration" / "default.md")
        identity = matrix.split("## 7.1.7 Identity", 1)[1].split("## 7.1.8", 1)[0]
        for requirement in ("only to its actual access/deployment context",
                            "When CI accesses cloud services/resources",
                            "local execution uses approved developer authentication",
                            "cloud-hosted execution uses the bound provider's workload identity",
                            "Offline-only CI needs no cloud identity",
                            "real-cloud evaluations", "Local candidate build/run does not require a cloud registry"):
            self.assertIn(requirement, identity)
        plan = read(SDLC / "templates" / "plan-template.md")
        for requirement in ("identity patterns actually needed", "Native local execution and offline-only CI",
                            "CI/CD actually accesses cloud services/resources",
                            "real-cloud CI evaluations without CD", "only where used",
                            "actual local, hosted and pipeline access contexts"):
            self.assertIn(requirement, plan)
        self.assertNotIn("When required, MUST declare: (a) the workload-identity pattern", plan)

    def test_recipient_mode_requires_own_context_authorization(self):
        core = read(ROOT / "framework" / "methodology" / "core-twtty-methodology.md")
        rule = next(line for line in core.splitlines() if line.startswith("7. Recover mode"))
        for requirement in ("independently verifiable human anchor",
                            "current Human User, repository/working context, selected scope and unchanged constraints",
                            "Handoff/imported history", "another caller's grant",
                            "unverified applicability MUST NOT enable Autopilot",
                            "start Interactive", "even when no setup work is needed",
                            "Historical evidence remains intact",
                            "Valid same-developer, same-context continuation MAY reuse its grant"):
            self.assertIn(requirement, rule)
        self.assertIn("A new Autopilot grant requires explicit, in-session", core)
        self.assertIn("Historical sender Autopilot approval is not recipient authorization",
                      read(SDLC / "templates" / "handoff-template.md"))
        self.assertIn("verify that it authorizes the current Human User",
                      read(SDLC / "sdlc.md"))

    def test_fixed_l1_autopilot_uses_native_human_approval_not_a_git_ceremony(self):
        core = read(ROOT / "framework" / "methodology" / "core-twtty-methodology.md")
        modes = " ".join(subsection(core, "### Execution modes").split())
        for requirement in ("Autopilot - EXECUTE only", "Autopilot - all remaining stages",
                            "A future EXECUTE-only grant never self-approves PLAN",
                            "not necessarily a Git commit", "current caller/context",
                            "Hard guardrails remain enforced", "record the authorization"):
            self.assertIn(requirement, modes)
        auth = " ".join(read(SDLC / "sdlc.md").split(
            "**Autopilot authorization evidence.**", 1)[1].split(
                "#### Axis 2", 1)[0].split())
        for requirement in ("L1, absent a stricter selected policy",
                            "one direct Human approval/request",
                            "Verify the original native Human input",
                            "An agent-to-agent relay is not itself Human approval",
                            "original native approval and its target can be checked",
                            "No Human Git commit", "L2-L5 / stricter policy",
                            "At L3+, require a verified-signature commit",
                            "Risk escalation out of L1", "unchanged applicable authorization on Resume"):
            self.assertIn(requirement, auth)
        for name in ("ghcopilot.md", "claudecode.md"):
            harness = " ".join(read(SDLC / "config" / "harness" / name).split())
            self.assertIn("L1", harness)
            self.assertIn("native Human", harness)
        discovery = subsection(core, "### Interview Me")
        self.assertIn("valid Autopilot scope", discovery)
        self.assertIn("four rounds and disclosed rationale are never skipped", discovery)
        self.assertIn("Autopilot does not fabricate answers", discovery)

    def test_l1_autopilot_design_review_remains_real_and_higher_levels_remain_human(self):
        matrix = read(SDLC / "config" / "risk-calibration" / "default.md")
        row = next(line for line in matrix.splitlines() if line.startswith("| UX-005 |"))
        for requirement in ("actually rendered", "at L1", "explicit Autopilot grant",
                            "actual browser/design checks", "never a Human attestation",
                            "L2-L5 and stricter Human-only policies retain Human approval"):
            self.assertIn(requirement, row)
        self.assertEqual([cell.strip() for cell in row.split("|")][-6:-1], ["MUST"] * 5)
        method = " ".join(read(SDLC / "sdlc.md").split())
        self.assertIn("existing spec explicitly requiring Human review needs an approved refinement",
                      method)
        ux = read(SDLC / "config" / "ux" / "default.md")
        self.assertIn("UX-005", ux)
        self.assertIn("explicitly delegated L1", ux)
        plan = read(SDLC / "templates" / "plan-template.md")
        self.assertIn("explicitly delegated L1 Autopilot AI review", plan)
        self.assertIn("actual browser demonstration", plan)

    def test_missing_state_recovery_has_no_global_rebuild_requirement(self):
        core = read(ROOT / "framework" / "methodology" / "core-twtty-methodology.md")
        summary = subsection(core, "### Project state summary")
        for requirement in ("selected scope and verified referenced Iterations",
                            "highest `<sequence-id>` verified in each indexed scope",
                            "missing, malformed or inconsistent",
                            "recover/reconcile the selected scope",
                            "Rebuild only that verified working-context summary",
                            "explicitly requested audit", "do not invent its status",
                            "Required selected-scope approval, pause, drift and log-integrity checks remain mandatory"):
            self.assertIn(requirement, summary)
        self.assertNotIn("falls back to a full-log read", summary)
        self.assertNotIn("one row per Iteration", summary)

    def test_existing_seed_layout_preserves_both_required_intents(self):
        dispatcher = read(ROOT / "framework" / "twtty.md")
        seeds = next(line for line in dispatcher.splitlines() if line.startswith("- **Seeds and intents"))
        for requirement in ("actual artifact root", "preserving existing layouts",
                            "default for new projects only", "<artifact-root>/seed/seed.md",
                            "Every first TWTTY baseline requires",
                            "including a baseline refactoring existing code",
                            "Every later Iteration reuses that approved Project Seed",
                            "own approved Iteration Intent", "neither can substitute for the other",
                            "Operational Resume preparation does not establish lifecycle approval",
                            "<artifact-root>/seed/intent-<iteration-id>.md"):
            self.assertIn(requirement, seeds)
        self.assertNotIn("always read from `<project>/twtty/seed/seed.md`", dispatcher)

    def test_first_contact_calibrates_risk_before_recording_seed_exit(self):
        core = read(ROOT / "framework" / "methodology" / "core-twtty-methodology.md")
        first_contact = subsection(core, "### 4.2 On first contact")
        steps = dict(re.findall(r"(?m)^(\d+)\. (.+)$", first_contact))
        self.assertIn("not `SEED-EXIT`", steps["3"])
        self.assertNotIn("append", steps["3"])
        self.assertIn("`meta/risk-level`", steps["4"])
        self.assertIn("MUST be appended **before**", steps["4"])
        for requirement in ("ladder alternatives and an override choice",
                            "Human User's actual selection",
                            "seed preference is a recommendation input, not approval",
                            "not reduce the choice to a Boolean"):
            self.assertIn(requirement, steps["4"])
        self.assertIn("Calibrate the pipeline", steps["5"])
        self.assertIn("Only after approval append", steps["6"])
        self.assertIn("`seed/0a`", steps["6"])
        self.assertIn("Risk confirmation/recording and calibration MUST precede", steps["6"])
        self.assertIn("do not reorder, backdate or rewrite existing logs", steps["6"])
        self.assertIn("Proceed to SPEC", steps["7"])

    def test_guided_decisions_and_materialized_config_share_existing_approval_flow(self):
        core = read(ROOT / "framework" / "methodology" / "core-twtty-methodology.md")
        rules = " ".join(subsection(core, "### 4.5 Rules").split())
        for requirement in ("In Discovery and every TWTTY loop",
                            "context-grounded values", "editable/customize choice",
                            "genuinely unknown intent", "Reuse settled answers",
                            "adds no gate", "actual required Human decision"):
            self.assertIn(requirement, rules)
        interview = subsection(read(SDLC / "sdlc.md"), "#### Config interview")
        finalize = interview.split("**Finalize after materialization.**", 1)[1].split(
            "For later iterations", 1)[0]
        for requirement in ("as a draft", "actual effective settings",
                            "provisional", "Use these settings / Customize settings",
                            "before recording `meta/config`", "earlier valid approval",
                            "unchanged configuration on Resume"):
            self.assertIn(requirement, " ".join(finalize.split()))
        for filename in ("README.md", "runtime-config-readme-template.md"):
            self.assertIn("Use these settings / Customize settings",
                          read(SDLC / "config" / filename))
        seed = " ".join(subsection(read(SDLC / "sdlc.md"), "### 3.1 Seed").split())
        self.assertIn("Propose a concrete repository name", seed)
        self.assertIn("before creation", seed)
        github = " ".join(read(SDLC / "config" / "devtools" / "devtools-config1.md").split())
        self.assertIn("otherwise the current authenticated account", github)
        self.assertIn("private visibility absent an approved preference", github)
        azure = " ".join(read(SDLC / "config" / "devtools" / "devtools-config2.md").split())
        self.assertIn("respect inherited project visibility", azure)

    def test_bootstrap_requires_complete_applicable_methodology_reads(self):
        dispatcher = read(ROOT / "framework" / "twtty.md")
        loading = " ".join(subsection(
            dispatcher, "## What the AI Agent MUST do on any `twtty` command"
        ).split("\n2.", 1)[0].split())
        for requirement in (
            "Read this dispatcher and the complete",
            "in full from the explicitly selected bootstrap tree",
            "bounded read-only lookup needed to identify its active specialization",
            "read that specialization and every methodology it explicitly inherits in full",
            "obtain the missing Human selection before loading its complete methodology chain",
            "Do not decide the command outcome or begin execution until this reading is complete",
            "Read the required methodology files in full on every invocation",
            "Truncated output, summaries, path resolution and prior-session memory "
            "do not satisfy this requirement",
            "report the blocker rather than proceeding from assumptions",
            "identify the methodology files actually read",
            "Read applicable project-owned profiles and artifact templates "
            "when their procedures require them",
        ):
            with self.subTest(requirement=requirement):
                self.assertIn(requirement, loading)

    def test_bootstrap_source_and_multiple_artifact_roots_do_not_reset_existing_work(self):
        dispatcher = read(ROOT / "framework" / "twtty.md")
        roots = " ".join(subsection(dispatcher, "## Artifact-root resolution").split())
        for requirement in ("Preserve a verified legacy root", "`baseline SDLC` to `sdlc`",
                            "not an accepted command value", "current branch/scope evidence",
                            "ask for the exact artifact root", "never choose the newest",
                            "Missing logs on Resume never create a new baseline",
                            "never move artifacts", "Handoff still does not accept `type=`",
                            "each included root", "multi-root export"):
            self.assertIn(requirement, roots)
        for requirement in ("explicitly selected bootstrap tree", "actual revision",
                            "do not substitute another checkout",
                            "does not upgrade the project's adopted configuration"):
            self.assertIn(requirement, dispatcher)
        core = " ".join(read(ROOT / "framework" / "methodology" /
                             "core-twtty-methodology.md").split())
        self.assertIn("one consistent current account", core)
        self.assertIn("refresh or remove stale duplicate prose", core)

    def test_privacy_requires_keyless_program_and_ai_context_before_persistence(self):
        core = read(ROOT / "framework" / "methodology" / "core-twtty-methodology.md")
        privacy = " ".join(core.split("**Before each risky evidence write.**", 1)[1].split(
            "**GitHub and other platform identities", 1)[0].split())
        for requirement in ("AI Agent MUST identify context-sensitive details",
                            "supply already-known sensitive values privately",
                            "inspect its sanitized output", "requires no key",
                            "add it to private context and rerun", "Failure blocks that write",
                            "Controlled metadata-only", "No extra discovery"):
            self.assertIn(requirement, privacy)
        tool = read(ROOT / "framework" / "tools" / "README.md")
        steps = [tool.index(label) for label in (
            "**AI identifies context.", "**Program redacts in memory.",
            "**AI reviews actual output.", "**Persist reviewed sanitized text only.")]
        self.assertEqual(steps, sorted(steps))
        for requirement in ("not an exhaustive list", "not unique or stable cross-session",
                            "--require-key", "blocks a missing key", "never fall back to raw"):
            self.assertIn(requirement, " ".join(tool.split()))
        branches = " ".join(subsection(read(SDLC / "sdlc.md"),
                                       "#### 8.1.2 Branch-scoped replay logs").split())
        for requirement in ("random 32-hex reference once", "no key or hash",
                            "never regenerate it on Resume", "Missing or inconsistent",
                            "policy-required scope PR", "without a duplicate",
                            "Existing branch logs remain authoritative",
                            "shared claims or worker/domain isolation"):
            self.assertIn(requirement, branches)

    def test_infrastructure_apply_and_acceptance_are_explicit_not_configuration_proxies(self):
        profile = read(SDLC / "config" / "development" / "default.md")
        creation = " ".join(profile.split("3. **Create only the remainder.", 1)[1].split(
            "4. **Continue on native success.", 1)[0].split())
        steps = [creation.index(label) for label in (
            "author and review", "provisioning consent", "Actually execute",
            "wait for its terminal result", "Capture the native result/output",
            "Save returned bindings after native success", "before dependent app work")]
        self.assertEqual(steps, sorted(steps))
        self.assertIn("Keep concrete commands in the provider binding", creation)
        readiness = " ".join(profile.split())
        self.assertIn("only under an explicitly approved plan deferral", readiness)
        self.assertIn("acceptance remains pending", readiness)
        method = " ".join(subsection(read(SDLC / "sdlc.md"), "### 3.4 Execute").split())
        self.assertIn("green offline CI is not live-model acceptance", method)
        self.assertIn("cannot satisfy an applicable required gate or `EXECUTE-EXIT`", method)

    def test_original_seed_and_completed_baseline_are_required_before_iterations(self):
        core = read(ROOT / "framework" / "methodology" / "core-twtty-methodology.md")
        iteration = subsection(core, "### 4.3 On new Iteration")
        required = iteration.index("Before creating an Iteration")
        create = iteration.index("At creation")
        self.assertLess(required, create)
        normalized = " ".join(iteration.split())
        for requirement in ("approved Project Seed exists",
                            "initial baseline has a verified approved `EXECUTE-EXIT`",
                            "Missing evidence blocks iteration creation",
                            "replace the Project Seed with an Iteration Intent",
                            "approval in Interactive mode at `SEED-EXIT`"):
            self.assertIn(requirement, normalized)
        discovery = subsection(core, "### Interview Me")
        self.assertIn("Every later Iteration requires both", discovery)
        self.assertIn("an iteration intent cannot replace the original project seed", discovery.lower())
        self.assertRegex(subsection(core, "### 4.2 On first contact"), r"refactor(?:ing)? existing code")
        method = read(SDLC / "sdlc.md")
        self.assertIn("Every later Iteration", read(ROOT / "framework" / "twtty.md"))
        self.assertIn("Missing required intent blocks discovery", method)
        self.assertIn("preparation never substitutes for that lifecycle", method)
        for text in (core, method, read(ROOT / "framework" / "twtty.md")):
            self.assertNotIn("seedless", text.lower())
            self.assertNotIn("without a baseline/project seed", text.lower())

    def test_existing_repository_publication_preserves_integration_controls(self):
        method = read(SDLC / "sdlc.md")
        seed = " ".join(subsection(method, "### 3.1 Seed").split())
        for requirement in ("For a new repository only", "For an existing repository",
                            "configured integration branch", "do not reinitialize",
                            "Publish the approved seed", "PRs and required CI/reviews",
                            "original Project Seed and full baseline remain mandatory"):
            self.assertIn(requirement, seed)
        self.assertNotIn("SEED artifact is committed on `main`", seed)
        realization = next(line for line in method.splitlines()
                           if line.startswith("**Gate realization tracks"))
        for requirement in ("only for a new repository", "from SEED onward",
                            "authoritative integration gate is the reviewed, CI-passing merge",
                            "stage-exit approval is not itself an integration request"):
            self.assertIn(requirement, realization)
        publication = next(line for line in method.splitlines()
                           if line.startswith("- **Version control from SEED"))
        for requirement in ("existing PR/CI/review controls from SEED onward",
                            "no onboarding exception bypasses existing protection",
                            "If authorized publication cannot be completed, `Escalate`"):
            self.assertIn(requirement, publication)
        for binding in ("devtools-config1.md", "devtools-config2.md"):
            hooks = read(SDLC / "config" / "devtools" / binding).split("## Stage hooks", 1)[1]
            self.assertIn("preserve existing history, remotes and integration branch", hooks)
            self.assertIn("Direct bootstrap pushes are limited to new", hooks)
            self.assertIn("never disable protection for onboarding", hooks)
            self.assertNotIn("to `main`", hooks)

    def test_stage_approval_does_not_force_a_publication_pr_or_merge(self):
        method = read(SDLC / "sdlc.md")
        boundary = next(line for line in method.splitlines()
                        if line.startswith("**Stage approval is not a PR boundary.**"))
        for requirement in ("`SEED-EXIT`, `SPEC-EXIT` and `PLAN-EXIT`",
                            "required stage checks and approvals",
                            "approval evidence committed and pushed there",
                            "Reuse one domain/scope PR",
                            "rather than open or merge a PR solely to complete a stage",
                            "planned domain/scope integration checkpoint",
                            "explicit external policy or approved plan",
                            "satisfy it before advancing the dependent work",
                            "Required CI/reviews still gate integration",
                            "pending or failing integration checks MUST NOT be reported as passed",
                            "checks due at the current stage still block that stage"):
            self.assertIn(requirement, boundary)
        self.assertNotIn("local approval is only a working checkpoint until they pass and merge",
                         method)
        for binding in ("devtools-config1.md", "devtools-config2.md"):
            hooks = read(SDLC / "config" / "devtools" / binding)
            self.assertIn("authorized working branch", hooks)
            self.assertIn("Stage approval does not require a separate PR or merge per stage", hooks)
            self.assertIn("explicit earlier-merge policies remain binding", hooks)

    def test_environment_ownership_remains_without_bespoke_infra_checks(self):
        profile = read(SDLC / "config" / "development" / "default.md")
        self.assertIn("by environment purpose and deployment ownership, not physical resource location", profile)
        self.assertIn("mistaken paths in a newly generated plan are not approved legacy layouts", profile)
        none = read(SDLC / "config" / "cloud" / "none.md")
        self.assertIn("Do not infer it from `Runtime target: N/A`", none)
        self.assertIn("Local support services/emulators", none)
        template = read(SDLC / "templates" / "plan-template.md")
        self.assertIn("environment-purpose rule", template)
        self.assertIn("Native operations, recovery and preview requirements are defined by the bound development profile", template)
        self.assertIn("existing finite recovery limits", profile)
        self.assertIn("Use preview/native plan when modifying shared/production resources", profile)
        self.assertIn("no custom infrastructure validator or executable IaC is required", template)

    def test_dependency_setup_precedes_infra_then_app_and_eval_implementation(self):
        profile = read(SDLC / "config" / "development" / "default.md")
        sequence = subsection(profile, "## Developer workstation inner loop")
        steps = dict(re.findall(r"(?m)^(\d+)\. (.+)$", sequence))
        self.assertIn("Identify required software/packages", steps["2"])
        self.assertIn("next operation", steps["3"])
        self.assertIn("after dependency setup", steps["4"])
        self.assertIn("then implement the app", steps["5"])
        requirements = " ".join(subsection(profile, "### Requirements and dependencies").split())
        for requirement in ("For new work, Resume and each isolated worker",
                            "manifests/lockfiles", "runtime/package-manager version declarations",
                            "no manifests yet", "not infer requirements from a prior conversation",
                            "minimal approved manifests/version declarations",
                            "native package manager generate locks during its initial resolve/restore",
                            "Do not handwrite lockfiles",
                            "not feature or eval-harness implementation",
                            "only after its required tools/packages are available"):
            self.assertIn(requirement, requirements)
        method = read(SDLC / "sdlc.md")
        order = method.split("**Development execution policy.**", 1)[1].split(
            "| Stage task", 1)[0]
        for section in ("developer-workstation-inner-loop", "requirements-and-dependencies",
                        "tooling-readiness-and-reuse", "parallel-setup"):
            self.assertIn(f"development/default.md#{section}", order)
        self.assertIn("authoritative setup procedure", order)
        plan = read(SDLC / "templates" / "plan-template.md")
        plan_sequence = subsection(plan, "### 3.2 Sequencing and dependencies")
        self.assertIn("development/default.md#developer-workstation-inner-loop", plan_sequence)
        self.assertIn("this app's work dependencies", plan_sequence)
        agentic = read(SDLC.parent / "sdlc-for-agentic-apps" / "sdlc-for-agentic-apps.md")
        self.assertIn("have no eval-harness prerequisite", agentic)
        resume = subsection(method, "### 3.6 Existing-project preparation")
        for requirement in ("development/default.md#resume-preparation",
                            "prepare only missing prerequisites",
                            "first unmet prerequisite/plan obligation",
                            "not the next numeric stage-task ID"):
            self.assertIn(requirement, resume)
        level_one = next(line for line in method.splitlines() if line.startswith("| **1** | 3a"))
        self.assertIn("required local services/emulators", level_one)
        self.assertIn("after their dependency setup", level_one)

    def test_parallel_setup_is_shared_once_then_isolated_per_checkout(self):
        profile = read(SDLC / "config" / "development" / "default.md")
        setup = " ".join(subsection(profile, "### Parallel setup").split())
        for requirement in ("coordinator prepares shared manifests/locks",
                            "before dispatching app workers", "Only one owner",
                            "separate branch and worktree/clone",
                            "restores only its missing checkout packages",
                            "Independent per-checkout restores may run concurrently",
                            "Never share/copy `node_modules`, virtual environments or credentials",
                            "own actual context, not assumed host tools",
                            "do not create a service stack per worker by default",
                            "Serialize conflicting service/data mutations",
                            "do not repeat unchanged questions or add setup gates/logs",
                            "concurrent writers never share a branch or checkout"):
            self.assertIn(requirement, setup)
        self.assertIn("Same checkout", profile)

    def test_development_procedure_has_one_owner_not_a_second_plan(self):
        profile = read(SDLC / "config" / "development" / "default.md")
        ownership = " ".join(subsection(profile, "## Policy ownership").split())
        for requirement in ("authoritative reusable development procedure",
                            "SDLC retains lifecycle/task contracts, gates",
                            "PLAN references the bound profile and records app-specific",
                            "Native manifests/locks and existing setup/run recipes",
                            "Do not add a separate requirements inventory"):
            self.assertIn(requirement, ownership)
        plan = read(SDLC / "templates" / "plan-template.md")
        for heading, anchor in (("### 1.3 Infrastructure architecture", "policy-ownership"),
                                ("### 3.2 Sequencing and dependencies", "developer-workstation-inner-loop"),
                                ("### 3.3 Team collaboration", "parallel-setup")):
            self.assertIn(f"development/default.md#{anchor}", subsection(plan, heading))
        for duplicated_instruction in ("Ask about existing services immediately before provisioning",
                                       "use ignored `.env.local`",
                                       "restore packages before infrastructure",
                                       "Do not make them reinstall machine tools"):
            self.assertNotIn(duplicated_instruction, plan)
        azure = read(SDLC / "config" / "cloud" / "azure.md")
        self.assertNotIn("MUST ask whether", azure)
        runtime_readme = read(SDLC / "config" / "runtime-config-readme-template.md")
        self.assertIn("profile selected by `development` in `runtimeconfig.md`", runtime_readme)
        self.assertIn("rather than copying it here", runtime_readme)

    def test_methodology_does_not_generate_validator_tooling(self):
        core = read(ROOT / "framework" / "methodology" / "core-twtty-methodology.md")
        self.assertIn("Do not generate a custom identifier detector", core)
        for requirement in ("single framework-supplied shared privacy utility",
                            "Before each risky evidence write", "Controlled metadata-only",
                            "Do not wait for stage end", "Failure blocks that write",
                            "not a harness-wide file-write hook"):
            self.assertIn(requirement, core)
        self.assertIn("Native history is not a cryptographic tamper-proof guarantee", core)
        self.assertIn("retaining originals", read(SDLC.parent / "reverse-engineering" / "reverse-engineering.md"))
        self.assertNotIn("MUST define automated detection checks", core)
        matrix = read(SDLC / "config" / "risk-calibration" / "default.md")
        self.assertNotIn("Identifier detection MUST be exercised", matrix)
        self.assertIn("without generating a custom gate-check job", matrix)
        for binding in ("devtools-config1.md", "devtools-config2.md"):
            provider = " ".join(read(SDLC / "config" / "devtools" / binding).split())
            self.assertNotIn("Provide project-local detection", provider)
            self.assertIn("Do not generate", provider)
            self.assertIn("shared privacy utility before risky evidence writes", provider)
            self.assertIn("organization/regulatory control", provider)
        stack = read(SDLC.parent / "sdlc-for-agentic-apps" / "config" / "agentic-stack" / "default.md")
        self.assertIn("Preserve the approved model/version/region", stack)
        self.assertIn("Do not\n  silently repin", stack)

    def test_native_infra_outcomes_replace_custom_tests_and_preview_chains(self):
        profile = read(SDLC / "config" / "development" / "default.md")
        infra = subsection(profile, "### Development infrastructure first")
        for requirement in ("No additional local-infra checks",
                            "build/validate/what-if chain", "dedicated",
                            "no blanket", "custom infra validators",
                            "correct and retry", "existing finite recovery limits",
                            "changed resource/permission/cost boundary",
                            "normal\n   first app run"):
            self.assertIn(requirement, infra)
        azure = read(SDLC / "config" / "cloud" / "azure.md")
        local = " ".join(azure.split("## Local-development dependencies", 1)[1].split(
            "## Stage hooks", 1)[0].split())
        for requirement in ("az deployment group create", "Azure CLI compiles Bicep",
                            "no mandatory separate", "not something Bicep runs automatically",
                            "profile's stronger preview requirements",
                            "native prompts are not bypassed", "no-op approval flags"):
            self.assertIn(requirement, local)
        matrix = read(SDLC / "config" / "risk-calibration" / "default.md")
        self.assertNotIn("| IaC validation job present and green |", matrix)
        self.assertIn("not a separate CI job or custom validator", matrix)
        method = read(SDLC / "sdlc.md")
        exit_gate = method.split("**Stage exit gate (`EXECUTE-EXIT`).**", 1)[1].split(
            "**Replay-log entry shapes:**", 1)[0]
        self.assertIn("execute/3h/W-<n>", exit_gate)
        self.assertIn("not duplicate app-stage entries", exit_gate)
        self.assertIn("deployment success alone does not satisfy it", exit_gate)

    def test_branch_topology_is_sequential_domain_or_isolated_parallel(self):
        method = read(SDLC / "sdlc.md")
        topology = method.split("**Branching for isolation only.**", 1)[1].split(
            "**Worker integration is pre-authorized work.**", 1)[0]
        cases = {
            "Single domain, sequential": ("no extra branch", "direct development is permitted"),
            "Multiple domains": ("one scope-limited working branch per affected domain",
                                 "not one branch per work item"),
            "Parallel workers": ("separate branch and isolated worktree or clone",
                                 "merge results back there serially"),
            "Protected repository or stricter policy": ("Preserve required PR/CI/review controls",
                                                      "one working branch/PR"),
        }
        for scenario, requirements in cases.items():
            row = next(line for line in topology.splitlines()
                       if line.startswith(f"| {scenario} |"))
            for requirement in requirements:
                with self.subTest(scenario=scenario, requirement=requirement):
                    self.assertIn(requirement, row)
        self.assertIn("Never run concurrent writers on the same branch or checkout", topology)
        self.assertIn("not as permanent release branches", topology)
        common = topology.split("**Common working context.**", 1)[1]
        for requirement in ("Prepare initial local/Azure infrastructure and save app settings there first",
                            "before deriving needed app-domain or worker",
                            "Do not create a branch or worktree solely because",
                            "Reuse the same checkout for Sequential development",
                            "not merely because Sequential work switches branches"):
            self.assertIn(requirement, common)
        self.assertNotIn("including applicable platform/infra layers", topology)
        self.assertNotIn("Domains are not a branching unit", method)
        self.assertNotIn("Every `W-<n>` MUST be delivered on a short-lived branch", method)
        for binding in ("devtools-config1.md", "devtools-config2.md"):
            provider = read(SDLC / "config" / "devtools" / binding)
            self.assertIn("one working branch per affected domain", provider)
            self.assertIn("isolated branches/worktrees for parallel writers", provider)

    def test_worker_integration_reuses_approval_without_protection_bypass(self):
        method = read(SDLC / "sdlc.md")
        integration = method.split("**Worker integration is pre-authorized work.**", 1)[1].split(
            "Two independent axes", 1)[0]
        for requirement in ("approved parallel-dispatch prompt includes the target working branch",
                            "without another Human approval or worker PR where target policy permits",
                            "Run affected checks on the combined result",
                            "Stop for changed scope/behavior", "native permission prompts remain",
                            "protected main", "No grant bypasses repository protection"):
            self.assertIn(requirement, integration)
        churn = next(line for line in method.splitlines()
                     if line.startswith("- **Avoid protection-driven churn.**"))
        for requirement in ("Refresh a domain/scope candidate when it reaches integration",
                            "every required target check", "evidence-only PRs",
                            "not permission to disable strict up-to-date protection"):
            self.assertIn(requirement, churn)
        logs = subsection(method, "#### 8.1.2 Branch-scoped replay logs")
        self.assertIn("Sequential direct development uses the active scope log", logs)
        self.assertIn("an internal worker does not need its own PR", logs)
        self.assertIn("required shared-contributor claim still must be published", logs)
        record = next(line for line in method.splitlines()
                      if line.startswith("- **`meta/branch-integrated`**"))
        self.assertIn("next ordinary evidence update", record)
        self.assertIn("Do not predict a resulting SHA", record)

    def test_pattern_answer_is_reused_instead_of_reasked_at_plan(self):
        method = read(SDLC / "sdlc.md")
        confirmation = method.split("**Execution-pattern confirmation, not re-interview.**", 1)[1].split(
            "**Environment consistency.**", 1)[0]
        for requirement in ("reuse the Human's recorded Sequential/Parallel answer from Discovery",
                            "Do not ask the same question again at PLAN or Resume",
                            "If no applicable answer exists, collect it once",
                            "only for a material change outside the recorded scope/constraints"):
            self.assertIn(requirement, confirmation)
        config = read(SDLC / "config" / "default-config.md")
        self.assertIn("PLAN reuses that answer", config)
        self.assertNotIn("not resolved by the config interview", config)
        template = read(SDLC / "templates" / "plan-template.md")
        self.assertIn("reuse the human's existing discovery pattern answer", template.lower())
        dispatcher = read(ROOT / "framework" / "twtty.md")
        self.assertIn("Never run concurrent writers on", dispatcher)

    def test_metadata_derives_hosting_from_approved_outcome(self):
        spec = read(SDLC / "templates" / "spec-template.md")
        metadata = subsection(spec, "## Metadata")
        for requirement in ("confirmed application-hosting outcome",
                            "`N/A` when no cloud application hosting is selected",
                            "even with an Azure development-service binding",
                            "Provider selection alone MUST NOT enable CD"):
            self.assertIn(requirement, metadata)
        self.assertNotIn("Runtime target (the active `cloud` binding", metadata)

    def test_service_selection_is_ordered_scoped_and_fails_closed(self):
        profile = read(SDLC / "config" / "development" / "default.md")
        infra = " ".join(subsection(profile, "### Development infrastructure first").split())
        stages = ["1. **Discover and offer reuse.", "2. **Offer manual configuration.",
                  "3. **Create only the remainder.", "4. **Continue on native success."]
        offsets = [infra.index(stage) for stage in stages]
        self.assertEqual(offsets, sorted(offsets))
        for requirement in ("For each required Azure service", "without authorization",
                            "Only after reuse and manual configuration are declined",
                            "invalid/unusable manual settings are blocked/unknown",
                            "not proof of absence", "approved secure local input/secret storage",
                            "does not waive identity/no-key policy",
                            "Reuse valid previously selected services/bindings/answers on Resume",
                            "no implicit modification/redeclaration"):
            self.assertIn(requirement, infra)
        requirements = " ".join(subsection(profile, "### Requirements and dependencies").split())
        self.assertIn("only the immediate operation's dependencies", requirements)
        self.assertIn("Defer unrelated app-only restores", requirements)

    def test_model_access_uses_minimal_matching_client_not_a_forced_project(self):
        stack = " ".join(read(SDLC.parent / "sdlc-for-agentic-apps" / "config" /
                                 "agentic-stack" / "default.md").split())
        for requirement in ("direct Azure OpenAI resource client",
                            "reusing an approved project endpoint",
                            "Do not create a new resource merely to preserve a default client",
                            "not an all-provider umbrella/meta-package",
                            "SDK construction is not a model-provisioning prerequisite",
                            "not silent migration or model substitution"):
            self.assertIn(requirement, stack)
        azure = read(SDLC / "config" / "cloud" / "azure.md")
        self.assertIn("reviewed IaC", azure)
        self.assertIn("az deployment group create", azure)
        self.assertIn("Resolve any conflict between a helper workflow", azure)

    def test_l1_formal_tests_and_evals_are_optional_without_lowering_l2_plus(self):
        sources = [
            (SDLC / "config" / "risk-calibration" / "default.md",
             ("| Every application", "| Tests independently")),
            (SDLC.parent / "sdlc-for-agentic-apps" / "config" / "risk-calibration" / "eval-delta.md",
             ("| Evaluation harness present", "| Declared pass rule")),
            (SDLC.parent / "dataeng" / "config" / "risk-calibration" / "dataeng-delta.md",
             ("| Completeness test", "| Uniqueness test", "| Data quality run outputs",
              "| Every `DQ-<n>`")),
        ]
        for source, prefixes in sources:
            lines = read(source).splitlines()
            for prefix in prefixes:
                row = next(line for line in lines if line.startswith(prefix))
                cells = [cell.strip() for cell in row.split("|")][-6:-1]
                with self.subTest(source=source.name, row=prefix):
                    self.assertNotEqual(cells[0], "MUST")
                    self.assertEqual(cells[1:], ["MUST"] * 4)
        method = read(SDLC.parent / "sdlc-for-agentic-apps" / "sdlc-for-agentic-apps.md")
        self.assertIn("When formal evaluations apply, agentic planning adds", method)
        self.assertIn("L1 smoke-only records its declared normal-app journey", method)
        template = read(SDLC.parent / "sdlc-for-agentic-apps" / "templates" /
                        "spec-for-agentic-apps-template.md")
        self.assertIn("formal evaluations not selected", template)
        self.assertIn("unless the Human explicitly selected", template)
        data_plan = read(SDLC.parent / "dataeng" / "templates" / "plan-for-dataeng-template.md")
        self.assertIn("L1 smoke-only uses normal source-to-sink verification", data_plan)

    def test_l1_smoke_retains_safeguards_and_does_not_create_cloud_ci(self):
        matrix = read(SDLC / "config" / "risk-calibration" / "default.md")
        smoke = " ".join(subsection(matrix, "### Level 1 verification").split())
        for requirement in ("real model response", "not a mock/health result",
                            "actual artifact inspection", "explicit Human selection",
                            "not automatic opt-in", "Preserve existing explicitly approved",
                            "L2-L5 controls are unchanged", "Privacy, permissions",
                            "approved cost/rate limits", "CI and UI prototype",
                            "does not require new CI federation"):
            self.assertIn(requirement, smoke)
        delta = read(SDLC.parent / "sdlc-for-agentic-apps" / "config" / "risk-calibration" /
                     "eval-delta.md")
        self.assertIn("selected formal evaluations only", delta)
        self.assertIn("not a scored quality/stability claim", delta)
        for requirement in ("generic quality ambitions are not formal-QA opt-in",
                            "If a draft seed conflicts", "never silently discard approved",
                            "not a blanket L2 QA selection", "basic deployed happy-path acceptance"):
            self.assertIn(requirement, " ".join(matrix.split()))

    def test_interactive_prototype_requires_working_browser_journeys(self):
        matrix = read(SDLC / "config" / "risk-calibration" / "default.md")
        prototype = next(line for line in matrix.splitlines() if line.startswith("| UX-003 |"))
        for requirement in ("wireframe or mockup AND", "locally served interactive browser",
                            "working navigation", "visible state changes",
                            "mock data and simulated services", "screenshots",
                            "without overwriting prior evidence"):
            self.assertIn(requirement, prototype)
        self.assertEqual([cell.strip() for cell in prototype.split("|")][-6:-1], ["MUST"] * 5)
        profile = read(SDLC / "config" / "ux" / "default.md")
        self.assertIn("| `html-prototype` | `required` |", profile)
        self.assertIn("retained for compatibility", profile)
        self.assertIn("model call is not a PLAN prerequisite", profile)
        plan = read(SDLC / "templates" / "plan-template.md")
        preview = subsection(plan, "### 2.6 UX design")
        for requirement in ("entry point", "startup instructions", "preview URL",
                            "actually exercised in a browser", "reusing unchanged"):
            self.assertIn(requirement, " ".join(preview.split()))
        gate = next(line for line in plan.splitlines() if line.startswith("16. UX design"))
        self.assertIn("actual browser demonstration", gate)
        self.assertIn("clean design-quality scan", gate)
        self.assertIn("approved rendered evidence", gate)

    def test_ui_craft_is_product_specific_not_a_forced_cinematic_style(self):
        matrix = read(SDLC / "config" / "risk-calibration" / "default.md")
        craft = next(line for line in matrix.splitlines() if line.startswith("| UX-002 |"))
        for requirement in ("named design system", "loading, empty, error, and recovery",
                            "Product-specific visual direction", "typography, spacing, color",
                            "reduced-motion preferences", "not delay tasks",
                            "familiar patterns remain valid"):
            self.assertIn(requirement, craft)
        profile = read(SDLC / "config" / "ux" / "default.md")
        self.assertIn("not a mandatory cinematic style", profile)
        self.assertIn("all-designs-must-pass", profile)
        self.assertIn("complete authored process", profile)

    def test_new_markdown_links_resolve(self):
        changed = git(ROOT, "diff", "--name-only", "--diff-filter=ACMR").decode().splitlines()
        untracked = git(ROOT, "ls-files", "--others", "--exclude-standard").decode().splitlines()
        new_documents = {
            (SDLC / "config" / "development" / "default.md").relative_to(ROOT).as_posix(),
            (SDLC / "templates" / "handoff-template.md").relative_to(ROOT).as_posix(),
        }
        entry_points = {
            "README.md", "framework/twtty.md",
            (SDLC / "sdlc.md").relative_to(ROOT).as_posix(),
            (SDLC / "templates" / "plan-template.md").relative_to(ROOT).as_posix(),
            (SDLC / "templates" / "spec-template.md").relative_to(ROOT).as_posix(),
        }
        for name in sorted(set(changed + untracked) | new_documents | entry_points):
            path = ROOT.joinpath(*name.split("/"))
            if path.suffix != ".md":
                continue
            current = read(path)
            if name in new_documents or name in untracked:
                baseline = ""
            elif name in changed:
                baseline = git(ROOT, "show", f"HEAD:{name}").decode()
            else:
                baseline = current
            def links(text):
                text = re.sub(r"`[^`\n]*`", "", text)
                return Counter(re.findall(r"\[[^\]\n]*\]\(([^)\n]+)\)", text))
            required = {target for target in links(current)
                        if "development/default.md" in target or "handoff-template.md" in target
                        or (name in entry_points and target.startswith("#"))}
            for target in set(links(current) - links(baseline)) | required:
                with self.subTest(source=name, target=target):
                    parsed = urlsplit(target.strip("<>"))
                    if parsed.scheme:
                        continue
                    if name == "framework/templates/project-readme-template.md" and (
                        parsed.path.startswith("twtty/") or parsed.path in {"LICENSE", "URL"}
                    ):
                        # App paths and placeholders resolve after copying and filling the template.
                        continue
                    destination = path.parent.joinpath(unquote(parsed.path)) if parsed.path else path
                    self.assertTrue(destination.exists(), f"Missing target: {destination}")
                    if parsed.fragment and destination.suffix == ".md":
                        self.assertIn(unquote(parsed.fragment), anchors(read(destination)))


class HandoffGitSelection(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="twtty-contract-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.repo = self.root / "product with spaces"
        self.repo.mkdir()
        self.env = os.environ.copy()
        self.env.update(GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM="1")
        self.excludes = self.root / "global.ignore"
        self.excludes.write_text("globally-ignored.txt\n", encoding="utf-8")
        self.run_git("init", "--quiet", "--template=")
        for name in (".gitignore", "README.md", "tracked-but-ignored.txt", "deleted.txt",
                     "twtty/replay-execution/execution-log.md"):
            self.write(name, b"original\r\n")
        self.run_git("add", ".")
        self.write(".gitignore", b"tracked-but-ignored.txt\ncache/\nignored-required.bin\n")
        self.write("README.md", b"current working contents\r\n")
        (self.repo / "deleted.txt").unlink()
        self.write("new file.md", b"untracked source\n")
        self.write("twtty/replay-execution/Iteration-old-execution-log.md", b"older scope\n")
        self.write("cache/generated.bin", b"ignored cache\n")
        self.write("ignored-required.bin", b"required synthetic input\n")
        self.write("globally-ignored.txt", b"globally ignored\n")

    def run_git(self, *args):
        return git(self.repo, "-c", "core.autocrlf=false",
                   "-c", f"core.excludesFile={self.excludes}", *args, env=self.env)

    def write(self, name, content):
        path = self.repo.joinpath(*name.split("/"))
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)

    def selection(self):
        documented = subsection(read(SDLC / "sdlc.md"), "### 3.7 Project handoff")
        commands = re.findall(r"`(git ls-files [^`]+)`", documented)
        self.assertEqual(commands, ["git ls-files --cached -z",
                                    "git ls-files --others --exclude-standard -z"])
        names = set()
        for command in commands:
            names.update(os.fsdecode(name) for name in self.run_git(*command.split()[1:]).split(b"\0") if name)
        return {name for name in names if self.repo.joinpath(*name.split("/")).is_file()}

    def test_current_tracked_untracked_and_historical_logs_are_selected(self):
        self.assertEqual(self.selection(), {
            ".gitignore", "README.md", "tracked-but-ignored.txt", "new file.md",
            "twtty/replay-execution/execution-log.md",
            "twtty/replay-execution/Iteration-old-execution-log.md",
        })
        self.assertEqual((self.repo / "README.md").read_bytes(), b"current working contents\r\n")

    def test_ignored_required_input_is_a_gap_not_silently_selected(self):
        self.assertNotIn("ignored-required.bin", self.selection())
        self.assertIn("Required ignored inputs need safe approved inclusion",
                      subsection(read(SDLC / "sdlc.md"), "### 3.7 Project handoff"))

    def test_selected_zip_roundtrip_preserves_raw_contents_and_source(self):
        selected = self.selection()
        snapshot = {name: hashlib.sha256(self.repo.joinpath(*name.split("/")).read_bytes()).hexdigest()
                    for name in selected}
        status = self.run_git("status", "--porcelain=v1", "-z", "--untracked-files=all")
        payload = self.root / "payload"
        payload.mkdir()
        archive_path = self.root / "delivery.zip"
        with zipfile.ZipFile(archive_path, "w") as archive:
            for name in sorted(selected):
                source = self.repo.joinpath(*name.split("/"))
                export = payload.joinpath(*name.split("/"))
                export.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, export)
                archive.write(export, arcname=name)
        with zipfile.ZipFile(archive_path) as archive:
            self.assertEqual(set(archive.namelist()), selected)
            self.assertEqual({name: hashlib.sha256(archive.read(name)).hexdigest()
                              for name in selected}, snapshot)
        self.assertEqual(self.run_git("status", "--porcelain=v1", "-z", "--untracked-files=all"), status)
        self.assertEqual({name: hashlib.sha256(self.repo.joinpath(*name.split("/")).read_bytes()).hexdigest()
                          for name in selected}, snapshot)


if __name__ == "__main__":
    unittest.main()
