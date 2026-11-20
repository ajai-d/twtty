# Shared evidence redaction

[Core privacy rules](../methodology/core-twtty-methodology.md#2-artifacts-and-formats)
remain authoritative. [redact_evidence.py](redact_evidence.py) is one shared Python
3.10+ standard-library program. **The default needs no key, key store, package install
or additional AI service.** It is not a per-project validator or CI requirement.

## When to call it

Before persisting new/changed potentially sensitive evidence: prompts, Notes, copied
user/tool/provider/error text, commands/results, transcripts, state/diagrams,
branch/hotfix evidence, reports and exported process evidence.

1. **AI identifies context.** Use the checklist below and the approved operation's
   already-known context to identify sensitive details, including ordinary names,
   confidential prose and indirect identifying combinations that patterns cannot infer.
   Do not retrieve extra secrets, conduct additional discovery or send data to a new
   external service just for redaction.
2. **Program redacts in memory.** Supply those known values privately as
   `TWTTY_REDACTION_CONTEXT` JSON: supported kind -> list of strings. The API accepts
   `Redactor(known_identifiers=context).redact(candidate)`. Reuse an instance for a
   coherent batch. Context is optional only when no additional sensitive values are
   known; a matching pattern is not required for context values.
3. **AI reviews actual output.** Inspect against the checklist and operation context,
   including indirect identification and encoded variants. For a residual, remove
   unnecessary content or add the value/span to context and rerun. Unresolved uncertainty
   blocks the write. A successful program exit is not proof of AI review or a clean scan.
4. **Persist reviewed sanitized text only.** Use the supplied create/append writer or
   an approved editor for derived artifacts. Never write raw temporary files, append
   raw text then clean it later, wait for stage end or rely only on a commit/push scan.
   Retain applicable native secret scanners and stricter organization controls.

This is the current AI Agent's context-aware review, not a new inference call or formal
evaluation. Controlled metadata-only entries (stage/work-item IDs, timestamps, status,
safe logical references, repository-relative artifact paths) and unchanged previously
verified sanitized content need no tool call. If uncertain, treat new content as risky.
Keep existing evidence cadence; do not add an entry merely because this tool ran.
Never persist raw context, a reversal map or raw matches in diagnostics.

## Sensitive-information checklist

This is a broad, extensible catalog, **not an exhaustive list of every possible sensitive
value or a claim that every example is automatically detected**. Sensitivity depends on
content, combinations, audience and policy. AI must assess every category, not only
program matches; use `identifier` or the appropriate context kind for additional values.

| Category | Examples to remove from evidence | Program coverage / AI responsibility |
|---|---|---|
| Credentials and authentication | Passwords, API/access keys, bearer/basic auth, PATs, JWTs, refresh/SAS tokens, connection strings, PEM/private/signing keys, passwords in URLs | Common assignments/prefixes, auth headers, connection strings and private-key blocks; AI adds unknown formats, fragments and unlabelled secrets |
| Sessions and recovery | Cookies, session identifiers, recovery codes, security answers, MFA/OTP seeds/codes, device-pairing codes | Labelled cookie/session/recovery/security-answer values; AI adds other formats/context |
| Personal identity and contact | Names, usernames, handles, login/git identities, email, phone, postal/street addresses, postal codes | Emails, handles, common phone forms, Git identity lines and common labels; AI adds free-form names/addresses and nicknames |
| Government and civic identifiers | National/tax/social-security IDs, passports, driving licences, immigration/voter identifiers | Common labels and SSN-shaped values; AI adds jurisdiction-specific formats and unlabelled IDs |
| Financial and payment | Card/PAN/CVV, bank/routing/IBAN numbers, financial account IDs, salary/income, balances, credit details, payment/transaction records | Common labels and 13-19-digit card-shaped spans (not validity checks); AI adds other formats and sensitive amounts/context |
| Health and care | Patient/medical IDs, diagnoses, prescriptions, conditions, disability, treatment/genetic information | Common labels; AI adds narrative, coded diagnoses and other records |
| Biometrics and highly sensitive personal traits | Fingerprints, face/voice templates, DNA, religion, ethnicity, sexual orientation, politics, union membership | Some labels; AI adds free text, inferred traits and combinations; do not infer missing personal traits |
| Demographic and relationship data | Birth dates, age/minor status, family/dependant/relationship, education and employment/personnel details | Common birth-date/age/gender labels; AI adds narrative and identifying combinations |
| Location and device/network data | Home/work locations, GPS, IP/MAC addresses, host/device names, serials, advertising/device IDs, telemetry | Valid IPv4/IPv6, selected host suffixes, GUIDs and location/host labels; AI adds MAC/device formats and arbitrary hostnames |
| Cloud and service identifiers | Tenants, subscriptions, accounts, RGs, resource IDs, deployments/model/project names, endpoints and bindings | Azure resource paths/common names, AWS ARNs, GUIDs, labels and known context; AI adds other provider formats and arbitrary names |
| Platform and repository identity | User/org/customer IDs, handles, owner/repo names, profile links, Git authors/noreply emails, branch names carrying identities | Email/handle/Git/URL/label patterns; AI adds bare names and numeric IDs, including public identities |
| Paths, URLs and access capabilities | Absolute/UNC/home paths, identifying filenames, URLs/query/fragment/userinfo, SSH Git URLs, signed links, webhooks, database/broker URIs | Common path and URI schemes, literal/escaped/common URL encoding; AI adds unsupported encodings, relative identifying paths and capabilities |
| Confidential business/IP | Customer/vendor names, contracts, pricing, forecasts, acquisition/strategy/roadmap details, proprietary code/data, unpublished research | Some labels plus supplied `business`/customer/organization context; AI reviews prose and minimum necessary excerpts |
| Legal and restricted records | Privileged advice, case/investigation IDs, legal/disciplinary records, sealed/protected material | Common labels plus `legal` context; AI reviews substance and applicable restrictions |
| Security-sensitive operational details | Internal topology, vulnerabilities/exploit details, non-public incident/access configuration, storage/recovery material | Credential/URL/path/ID patterns and supplied `security` context; AI reviews operational sensitivity |
| Indirect, embedded and non-text information | Rare identifying combinations, quoted/encoded payloads, OCR, screenshots, document metadata, attachments, archives | Common literal/ASCII-case/JSON/HTML/URL variants for known context only; AI checks combinations; binary/images require format-appropriate redaction before persistence |

Supported context kinds: `secret`, `private-key`, `email`, `phone`, `url`, `hostname`,
`ip-address`, `path`, `identifier`, `resource-id`, `resource-group`, `project`,
`deployment`, `account`, `subscription`, `tenant`, `organization`, `customer`,
`username`, `git-identity`, `person`, `address`, `location`, `government-id`,
`financial`, `health`, `biometric`, `personal`, `business`, `legal`, `security`.
Supply exact sensitive spans already identified by AI; conflicting context definitions
fail closed. Do not copy raw values into tool command literals or reports.

## Calling the shared writer

Use the shared framework location, not a generated project-local copy/wrapper.
First obtain sanitized candidate text with the API or stdout mode and perform AI review.
The example assumes `$reviewedSanitizedCandidate` and any private context are populated
in the **same process**, not with sensitive values embedded in a command:

```powershell
$OutputEncoding = [System.Text.UTF8Encoding]::new($false, $true)
$reviewedSanitizedCandidate | python $sharedRedactorPath --root $projectFolder --output 'replay-execution\execution-log.md' --append
if ($LASTEXITCODE -ne 0) { throw 'Evidence append blocked by redaction failure.' }
```

`$sharedRedactorPath` resolves to this framework's program; `$projectFolder` is the
approved existing directory containing `replay-execution/`. Use strict UTF-8 input;
prefer the API when exact newline/byte preservation matters.

The callable equivalent is `Redactor(known_identifiers=context).redact(candidate)`;
`write_evidence(candidate, output, root=project_folder, redactor=redactor, append=True)`
redacts **before opening the file**. Results expose sanitized `text` and category
`counts`, never raw matches. Native private errors/connection settings remain private:
sanitize evidence copies, not actual service/IaC/auth inputs.

Default replacements are simple `<REDACTED:kind>` markers. They are idempotent and
classify removed data, **not unique or stable cross-session identity aliases**. Do not
infer actor identity from matching markers; use safe role/scope references and native
approval records where relationships matter. No raw-value hash or mapping is saved.
Unrecognized marker payloads are redacted rather than trusted.

Without `--append`, `--output` creates a new file exclusively. With `--append`, only new
text is sanitized, not historical entries. Writes are restricted to `replay-execution/`
or `reports/` beneath the approved root; traversal, symbolic/hard links, `.git` and
license-notice filenames are rejected. Keep existing single-writer isolation: these are
not defenses against a malicious concurrent filesystem actor.

Without `--output`, only sanitized UTF-8 text is emitted to stdout for AI review before
an approved editor persists it elsewhere. Nonzero exit, invalid context, unsupported
input or write failure blocks the affected write; never fall back to raw text. Errors
do not echo input or context. Input must be text: binary/control characters, invalid
UTF-8 and over-4-MiB input are rejected. Whole-URL decoding rejects invalid UTF-8.
Compound matches win; unquoted paths/assignments may consume trailing prose on that line.
False positives are intentional; the tool is not a general JSON/CSV format-preserving
transformer. Inspect the intended artifact shape as well as privacy.

## Branch evidence tokens

Allocate one random 32-hex reference when a branch evidence context opens. Use
`uuid.uuid4().hex` or the program's `--branch-token` mode; no key or native-name hash
is needed. The compatibility API `Redactor().branch_token(native_branch_name)` validates
the name then allocates a fresh reference. **Call once, not on every invocation.**

Record it in existing opening/claim/dispatch evidence and reuse the exact reference,
filename and counters on Resume. Missing/conflicting recovery evidence blocks continuation;
never allocate another reference to disguise missing history. Use the reference in
`<scope-id>-<branch-token>-execution-log.md`, `br-<branch-token>-<n>` and source/receiving
context fields. Resolve native names privately from actual Git/PR context; never save
a raw-name reversal map or rename native refs. This does not add a new evidence file.

Existing non-identifying legacy filenames/IDs remain valid. Do not rename files, rewrite
entries or reset counters. Sensitive legacy references require explicit approved privacy
remediation before extension/copying. The program does not migrate historical evidence.

## Compatibility with already adopted keyed automation

New workflows do not create a key. Existing approved keyed callers can still use
`Redactor(existing_key, context, require_key=True)` or set their existing
`TWTTY_REDACTION_KEY` privately and invoke the CLI with `--require-key`.
An explicitly present environment key selects that legacy mode; invalid/empty keys fail,
and `--require-key` blocks a missing key rather than falling back to keyless redaction.
The existing HMAC aliases/authentication and branch-token algorithm are preserved.
Do not silently migrate an adopted keyed project or rewrite its records. Adoption of
the simplified method is explicit. Keyless copies do not authenticate old keyed markers.

## Limits

Program patterns plus AI review reduce exposure; **neither can guarantee detection of
all sensitive information**. Unknown formats, encodings, indirect identification and
non-text content require special care; block unresolved persistence and report actual
coverage. Do not claim a required scanner ran merely because the program succeeded.

This is shared code plus instructions, **not a harness/OS file-write hook**. It cannot
stop bypasses or sanitize terminal/chat/platform history retroactively. Keep native
authorship and required third-party notices unchanged. Existing disclosures require
separately approved remediation; a sanitized append cannot erase them or anonymize
correlatable platform history.

## License and disclaimer

Copyright 2026 Ajai Peddapanga. This TWTTY documentation is licensed under
[Apache License 2.0](../../LICENSE); see [NOTICE](../../NOTICE).

Provided "AS IS", subject to the license's warranty disclaimers and liability
limitations. AI-generated outputs may be incorrect or unsafe; validate results
before use. TWTTY does not guarantee security, regulatory compliance or production
suitability.
