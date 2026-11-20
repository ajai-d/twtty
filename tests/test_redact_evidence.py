"""Behavioral tests for shared privacy code, not per-project methodology validators."""

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from urllib.parse import quote

from framework.tools.redact_evidence import RedactionError, Redactor, write_evidence


ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "framework" / "tools" / "redact_evidence.py"
KEY = b"unit-test-only-project-redaction-key"


class EvidenceRedaction(unittest.TestCase):
    def test_keyless_redaction_masks_categories_without_identity_hashes(self):
        redactor = Redactor()
        result = redactor.redact(
            "first_name=Example Person\nssn=123-45-6789\n"
            "card_number=4111111111111111\ndiagnosis=private condition\n"
            "cookie=private-session\n"
            "address=123 Example Street\nlatitude=45.12\n"
            "dob=2000-01-01\nfingerprint=private-template\n"
            "case_number=private-case\nconfidential=private-business-plan\n"
            "person@example.invalid and another@example.invalid\n"
        )
        self.assertIn("<REDACTED:person>", result.text)
        self.assertIn("<REDACTED:government-id>", result.text)
        self.assertIn("<REDACTED:financial>", result.text)
        self.assertIn("<REDACTED:health>", result.text)
        self.assertIn("<REDACTED:security>", result.text)
        for kind in ("address", "location", "personal", "biometric", "legal", "business"):
            self.assertIn(f"<REDACTED:{kind}>", result.text)
        self.assertEqual(result.text.count("<REDACTED:email>"), 2)
        for value in ("Example Person", "123-45", "411111", "private", "@example",
                      "Example Street", "45.12", "2000-01-01"):
            self.assertNotIn(value, result.text)
        self.assertEqual(redactor.redact(result.text).text, result.text)
        self.assertEqual(Redactor().redact(result.text).text, result.text)

    def test_keyless_context_removes_ai_identified_free_form_and_encoded_values(self):
        context = {"business": ["Unannounced acquisition of Example Company"],
                   "person": ["Example Person"], "address": ["123 Example Street"]}
        redactor = Redactor(known_identifiers=context)
        for kind, values in context.items():
            value = values[0]
            for candidate in (value, quote(value, safe=""), json.dumps(value)[1:-1]):
                with self.subTest(kind=kind, encoded=candidate != value):
                    self.assertEqual(redactor.redact(candidate).text, f"<REDACTED:{kind}>")
        existing = redactor.redact("person@example.invalid").text
        self.assertNotIn("new-sensitive-value",
                         redactor.redact(f"password={existing} new-sensitive-value").text)
        self.assertNotIn("private-payload",
                         redactor.redact("<REDACTED:email-private-payload>").text)

    def test_keyless_cli_needs_no_key_and_invalid_context_cannot_append(self):
        with tempfile.TemporaryDirectory() as directory:
            args = ("--root", directory, "--output", "reports/result.md")
            result = self.run_cli(b"person@example.invalid", *args, key=None)
            self.assertEqual(result.returncode, 0, result.stderr)
            target = Path(directory) / "reports" / "result.md"
            self.assertEqual(target.read_text(encoding="utf-8"), "<REDACTED:email>")
            rejected = self.run_cli(b"password=private-value", *args, "--append",
                                    key=None, context="{invalid")
            self.assertNotEqual(rejected.returncode, 0)
            self.assertEqual(rejected.stdout, b"")
            self.assertNotIn(b"private-value", rejected.stderr)
            self.assertEqual(target.read_text(encoding="utf-8"), "<REDACTED:email>")
            rejected = self.run_cli(b"password=private-value", *args, "--append",
                                    "--require-key", key=None)
            self.assertNotEqual(rejected.returncode, 0)
            self.assertEqual(rejected.stdout, b"")
            self.assertEqual(target.read_text(encoding="utf-8"), "<REDACTED:email>")
        first = self.run_cli(b"private-branch", "--branch-token", key=None)
        second = self.run_cli(b"private-branch", "--branch-token", key=None)
        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertEqual(second.returncode, 0, second.stderr)
        self.assertRegex(first.stdout.decode().strip(), r"^[0-9a-f]{32}$")
        self.assertNotEqual(first.stdout, second.stdout)

    def test_additional_credentials_and_unlabelled_ids_are_masked_without_a_key(self):
        examples = ("Basic cHJpdmF0ZTpwYXNzd29yZA==",
                    "sk-proj-" + "Z" * 24, "glpat-" + "Z" * 24,
                    "123-45-6789", "4111 1111 1111 1111",
                    "arn:aws:s3:::private-customer-bucket",
                    "sb://private-namespace.servicebus.windows.net")
        for value in examples:
            with self.subTest(example_kind=value.split(":", 1)[0][:8]):
                result = Redactor().redact(value)
                self.assertNotIn(value, result.text)
                self.assertTrue(result.counts)

    def test_cloud_failure_context_is_removed_before_append(self):
        context = {"resource-group": ["example-development-group"],
                   "project": ["example-model-project"]}
        text = ("Deployment failed for example-development-group / example-model-project.\n"
                "Reference /subscriptions/00000000-0000-0000-0000-000000000001/"
                "resourceGroups/example-development-group/providers/Test/accounts/example.\n")
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "twtty" / "replay-execution" / "execution-log.md"
            target.parent.mkdir(parents=True)
            target.write_text("### 001 approved\n", encoding="utf-8")
            result = write_evidence(text, Path("twtty/replay-execution/execution-log.md"),
                                    root=Path(directory), redactor=Redactor(KEY, context),
                                    append=True)
            stored = target.read_text(encoding="utf-8")
            self.assertEqual(stored, "### 001 approved\n" + result.text)
            for value in ("example-development-group", "example-model-project",
                          "00000000-0000-0000-0000-000000000001"):
                self.assertNotIn(value, stored)
            self.assertIn("Deployment failed", stored)
            self.assertNotIn("example-development-group", repr(result))

    def test_credentials_urls_and_private_keys_are_masked(self):
        token = "ghp_" + "A" * 36
        text = (
            f"Authorization: Bearer {token}\n"
            'password="private password with spaces"\n'
            "token=first;second,third\n"
            "https://person:password@example.invalid/path?sig=private-signature\n"
            "DefaultEndpointsProtocol=https;AccountName=privateaccount;AccountKey=privatekey\n"
            "-----BEGIN PRIVATE KEY-----\nprivate-key-material\n-----END PRIVATE KEY-----"
        )
        result = Redactor(KEY).redact(text)
        for value in (token, "private password", "first", "second", "third",
                      "person:password", "private-signature", "privateaccount", "privatekey",
                      "private-key-material"):
            self.assertNotIn(value, result.text)
        self.assertIn("secret", result.counts)
        self.assertIn("private-key", result.counts)

    def test_identity_paths_network_addresses_and_git_urls_are_masked(self):
        text = (
            'Author: Example Person <person@example.invalid>\n'
            "fixture-\u00e9@example.invalid\n"
            '"C:\\Users\\Example Person\\project\\file.txt"\n'
            "/home/example/project\n"
            "2001:db8::1 and :: and 192.0.2.10\n"
            "+1 (202) 555-0123\n"
            "git@github.com:example-owner/private-project.git\n"
            "rg-private-demo and ai-project-private-demo\n"
            "sample.openai.azure.com"
        )
        result = Redactor(KEY).redact(text)
        for value in ("Example Person", "person@example.invalid", "C:\\Users",
                      "/home/example", "2001:db8", "192.0.2.10", "+1 (202) 555-0123", "example-owner",
                      "rg-private-demo", "ai-project-private-demo", "sample.openai.azure.com"):
            self.assertNotIn(value, result.text)
        self.assertNotIn("fixture-\u00e9@example.invalid", result.text)

    def test_service_bus_credentials_do_not_reach_evidence(self):
        redactor = Redactor(KEY)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for index, key in enumerate(("SharedAccessKey", "AccessKey", "SharedAccessSignature")):
                with self.subTest(key=key):
                    secret = "synthetic-shared-credential-value"
                    connection = (
                        "Endpoint=sb://example-namespace.servicebus.windows.net/;"
                        f"SharedAccessKeyName=policy;{key}={secret};EntityPath=private-queue"
                    )
                    target = Path("reports") / f"connection-{index}.md"
                    write_evidence(f"- **Notes:** {connection}\n", target,
                                   root=root, redactor=redactor)
                    stored = (root / target).read_text(encoding="utf-8")
                    for value in (secret, "example-namespace", "private-queue"):
                        self.assertNotIn(value, stored)
                    standalone = redactor.redact(json.dumps({key: secret}))
                    self.assertNotIn(secret, json.loads(standalone.text)[key])

    def test_paths_with_spaces_are_fully_masked_and_quoted_json_stays_valid(self):
        redactor = Redactor(KEY)
        paths = (r"C:\Users\Example Person\private-project\app.py",
                 r"\\example-server\Example Share\private-project\app.py",
                 "/home/Example Person/private-project/app.py")
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for index, path in enumerate(paths):
                with self.subTest(index=index):
                    target = Path("reports") / f"path-{index}.md"
                    write_evidence(f"Failure in {path}\nOutcome: Failed\n", target,
                                   root=root, redactor=redactor)
                    stored = (root / target).read_text(encoding="utf-8")
                    for value in ("Example Person", "Example Share", "private-project"):
                        self.assertNotIn(value, stored)
                    self.assertIn("Outcome: Failed", stored)
                    structured = json.dumps({"path": path, "status": "Failed"})
                    parsed = json.loads(redactor.redact(structured).text)
                    self.assertEqual(parsed["status"], "Failed")
                    self.assertNotIn("private-project", parsed["path"])

    def test_safe_protocol_metadata_and_relative_paths_are_preserved(self):
        text = ("### 021 execute/3h/W-2\nTimestamp: 2026-11-16T23:04:25Z\n"
                "Approved: AC-1, W-2; commit abcdef0123456789abcdef0123456789abcdef01; PR 7\n"
                "twtty/plan/plan.md and reports/verification.md\n")
        result = Redactor(KEY).redact(text)
        self.assertEqual(result.text, text)
        self.assertEqual(result.counts, {})

    def test_context_aliases_are_stable_across_encoded_forms_and_calls(self):
        value = 'Example group & "team"'
        inputs = [value, quote(value, safe=""), quote(quote(value, safe=""), safe=""),
                  json.dumps(value)[1:-1]]
        aliases = [Redactor(KEY, {"organization": [value]}).redact(v).text for v in inputs]
        self.assertEqual(len(set(aliases)), 1)
        other = Redactor(KEY, {"organization": ["Different team"]}).redact("Different team")
        self.assertNotEqual(other.text, aliases[0])

    def test_encoded_urls_and_escaped_secret_assignments_are_redacted(self):
        redactor = Redactor(KEY)
        url = "https://person:password@example.invalid/path?sig=private-signature"
        variants = [url, quote(url, safe=""), quote(quote(url, safe=""), safe=""),
                    url.replace("/", r"\/")]
        aliases = [redactor.redact(value).text for value in variants]
        self.assertEqual(len(set(aliases)), 1)
        self.assertNotIn("private-signature", aliases[0])
        escaped = json.dumps(json.dumps({"password": "do-not-output-this"}))
        self.assertNotIn("do-not-output-this", redactor.redact(escaped).text)

    def test_authenticated_markers_are_idempotent_and_wrong_key_is_rejected(self):
        redactor = Redactor(KEY)
        first = redactor.redact("person@example.invalid")
        self.assertEqual(redactor.redact(first.text).text, first.text)
        with self.assertRaises(RedactionError):
            Redactor(b"different-unit-test-project-key-value").redact(first.text)
        with self.assertRaises(RedactionError):
            redactor.redact("<REDACTED:email-" + "0" * 64 + ">")

    def test_invalid_encoded_urls_block_append_without_mutating_evidence(self):
        redactor = Redactor(KEY)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / "reports" / "existing.md"
            target.parent.mkdir()
            target.write_text("previous evidence", encoding="utf-8")
            for suffix in ("%FF", "%FE"):
                encoded = "https%3A%2F%2Fexample.invalid%2F" + suffix
                for value in (encoded, quote(encoded, safe="")):
                    with self.subTest(suffix=suffix, double_encoded=value != encoded):
                        with self.assertRaises(RedactionError) as error:
                            write_evidence(value, Path("reports/existing.md"), root=root,
                                           redactor=redactor, append=True)
                        self.assertNotIn(value, str(error.exception))
                        self.assertEqual(target.read_text(encoding="utf-8"), "previous evidence")

    def test_branch_tokens_keep_identifiers_out_of_filenames_and_entries(self):
        branch = "users/example-owner/private-customer"
        redactor = Redactor(KEY)
        token = redactor.branch_token(branch)
        self.assertRegex(token, r"^[0-9a-f]{32}$")
        self.assertEqual(token, Redactor(KEY).branch_token(branch))
        self.assertNotEqual(token, redactor.branch_token(branch.upper()))
        self.assertNotEqual(token, redactor.branch_token("users/example-owner/another-customer"))
        self.assertNotEqual(token, Redactor(b"different-unit-test-project-key-value").branch_token(branch))
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = Path("replay-execution") / "branches" / f"baseline-{token}-execution-log.md"
            entry = f"### br-{token}-001\nBranch reference: {token}\n"
            write_evidence(entry, target, root=root, redactor=redactor)
            self.assertEqual((root / target).read_text(encoding="utf-8"), entry)
            for value in ("example-owner", "private-customer"):
                self.assertNotIn(value, str(target))
                self.assertNotIn(value, entry)

    def test_an_existing_marker_does_not_hide_new_sensitive_assignment_content(self):
        redactor = Redactor(KEY)
        existing = redactor.redact("old@example.invalid").text
        text = f"password={existing} newly-added-sensitive-value"
        result = redactor.redact(text)
        self.assertNotIn("newly-added-sensitive-value", result.text)
        self.assertEqual(redactor.redact(result.text).text, result.text)

    def test_untrusted_placeholder_payload_is_not_assumed_safe(self):
        redactor = Redactor(KEY)
        result = redactor.redact("<REDACTED:username-private-unknown-person>")
        self.assertNotIn("private-unknown-person", result.text)
        self.assertEqual(redactor.redact(result.text).text, result.text)

    def test_known_bare_username_and_mention_reuse_the_same_alias(self):
        redactor = Redactor(KEY, {"username": ["example-user"]})
        self.assertEqual(redactor.redact("example-user").text,
                         redactor.redact("@example-user").text.removeprefix("@"))

    def test_key_and_context_errors_do_not_include_raw_values(self):
        cases = [(b"short", None), (KEY, {"unsupported-sensitive-kind": ["private-value"]}),
                 (KEY, {"project": "private-value"}),
                 (KEY, {"project": ["private-value"], "account": ["PRIVATE-VALUE"]}),
                 (KEY, {"project": ["private-value\ud800"]})]
        for key, context in cases:
            with self.subTest(context_type=type(context).__name__):
                with self.assertRaises(RedactionError) as error:
                    Redactor(key, context)
                self.assertNotIn("private-value", str(error.exception).lower())

    def test_partial_private_key_and_bare_account_handle_are_redacted(self):
        text = "@example-user\n-----BEGIN PRIVATE KEY-----\ntruncated-private-material"
        result = Redactor(KEY).redact(text)
        self.assertNotIn("example-user", result.text)
        self.assertNotIn("truncated-private-material", result.text)

    def test_known_context_controls_alias_for_case_variants(self):
        redactor = Redactor(KEY, {"project": ["ai-project-example"]})
        self.assertEqual(redactor.redact("ai-project-example").text,
                         redactor.redact("AI-PROJECT-EXAMPLE").text)

    def test_distinct_unicode_identifiers_are_not_merged_by_case_matching(self):
        redactor = Redactor(KEY, {"organization": ["org-i", "org-\u0131"]})
        first = redactor.redact("org-i").text
        second = redactor.redact("org-\u0131").text
        self.assertNotEqual(first, second)
        self.assertNotIn("org-i", first)
        self.assertNotIn("org-\u0131", second)

    def test_output_is_create_or_append_only_and_cannot_escape_evidence_root(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            relative = Path("reports/new.md")
            write_evidence("safe", relative, root=root, redactor=Redactor(KEY))
            with self.assertRaises(RedactionError):
                write_evidence("replacement", relative, root=root, redactor=Redactor(KEY))
            self.assertEqual((root / relative).read_text(encoding="utf-8"), "safe")
            for bad in (Path("../reports/out.md"), Path(".git/config"),
                        Path("src/app.py"), Path("reports/LICENSE"), Path("reports/COPYRIGHT")):
                with self.subTest(target=bad):
                    with self.assertRaises(RedactionError):
                        write_evidence("unsafe", bad, root=root, redactor=Redactor(KEY))
            (root / ".git").mkdir()
            with self.assertRaises(RedactionError):
                write_evidence("unsafe", Path("reports/out.md"), root=root / ".git",
                               redactor=Redactor(KEY))

    def test_invalid_new_input_leaves_existing_evidence_unchanged(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / "reports" / "existing.md"
            target.parent.mkdir()
            target.write_text("previous evidence", encoding="utf-8")
            with self.assertRaises(RedactionError):
                write_evidence("binary\0content", Path("reports/existing.md"), root=root,
                               redactor=Redactor(KEY), append=True)
            self.assertEqual(target.read_text(encoding="utf-8"), "previous evidence")

    def test_linked_destination_is_rejected_without_changing_original(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            original = root / "original.txt"
            original.write_text("unchanged", encoding="utf-8")
            (root / "reports").mkdir()
            os.link(original, root / "reports" / "linked.md")
            with self.assertRaises(RedactionError):
                write_evidence("new", Path("reports/linked.md"), root=root,
                               redactor=Redactor(KEY), append=True)
            self.assertEqual(original.read_text(encoding="utf-8"), "unchanged")

    def run_cli(self, text, *args, key=KEY.decode(), context="{}"):
        env = dict(os.environ, TWTTY_REDACTION_KEY=key, TWTTY_REDACTION_CONTEXT=context)
        if key is None:
            del env["TWTTY_REDACTION_KEY"]
        return subprocess.run([sys.executable, "-B", str(TOOL), *args], input=text,
                              capture_output=True, env=env)

    def test_cli_writes_only_redacted_content_with_context(self):
        with tempfile.TemporaryDirectory() as directory:
            result = self.run_cli(
                b"Failed in example-development-group", "--root", directory,
                "--output", "reports/result.md",
                context=json.dumps({"resource-group": ["example-development-group"]}),
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stdout, b"")
            self.assertNotIn("example-development-group",
                             (Path(directory) / "reports" / "result.md").read_text())

    def test_branch_token_cli_accepts_one_private_name_and_cannot_write_files(self):
        branch = "users/example-owner/private-customer"
        result = self.run_cli((branch + "\r\n").encode(), "--branch-token", context="{unused")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.decode().strip(), Redactor(KEY).branch_token(branch))
        self.assertNotIn(branch.encode(), result.stdout + result.stderr)
        for raw in (b"", (branch + "\nother-branch").encode()):
            with self.subTest(input_size=len(raw)):
                rejected = self.run_cli(raw, "--branch-token")
                self.assertNotEqual(rejected.returncode, 0)
                self.assertEqual(rejected.stdout, b"")
                self.assertNotIn(branch.encode(), rejected.stderr)
        with tempfile.TemporaryDirectory() as directory:
            rejected = self.run_cli(branch.encode(), "--branch-token", "--root", directory,
                                    "--output", "reports/branch.md")
            self.assertNotEqual(rejected.returncode, 0)
            self.assertFalse((Path(directory) / "reports").exists())

    def test_cli_failures_emit_no_raw_input_context_or_key(self):
        raw = b"password=do-not-output-this"
        for key, context, text in (("", "{}", raw), (KEY.decode(), "{invalid", raw),
                                   (KEY.decode(), "null", raw),
                                   (KEY.decode(), "{}", b"https%3A%2F%2Fexample.invalid%2F%FF"),
                                   (KEY.decode(), "{}", b"\xffprivate-input"),
                                   (KEY.decode(), "{}", b"\0private-input")):
            with self.subTest(context_valid=context == "{}"):
                result = self.run_cli(text, key=key, context=context)
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(result.stdout, b"")
                for value in (b"do-not-output-this", b"private-input", KEY):
                    self.assertNotIn(value, result.stderr)


if __name__ == "__main__":
    unittest.main()
