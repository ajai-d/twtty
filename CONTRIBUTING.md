# Contributing to TWTTY

TWTTY is a maintainer-controlled open-source project in beta.
The official repository is [ajai-d/twtty](https://github.com/ajai-d/twtty).

## Feedback and proposed changes

Use the official repository's issues for non-sensitive bug reports or feature
requests. Describe the affected revision, assistant, expected
behavior, actual behavior and minimal reproduction. Redact secrets, personal
information, customer data and confidential material before sharing.

Follow [SECURITY.md](SECURITY.md), not a public issue, for vulnerabilities.
Discuss substantial changes with the maintainer before implementing them.

For code or documentation changes, fork the public repository after release,
make a focused branch, and open a pull request against `main`. Outside
contributors do not need, and are not granted, write or administrative access
to the official repository. Maintainers may decline changes or request revisions.

## Development and verification

This repository is a methodology/prompt framework, not an installable `twtty`
command. The optional redaction tool requires Python 3.10+ and uses only the
standard library. Git is needed for the repository integration tests.

Run from the repository root:

```text
python -B -m unittest discover -s tests -v
```

These are contract, privacy-tool and disposable Git-selection tests, not proof
that a coding assistant followed the framework or that a live application works.
For methodology changes, keep the dispatcher, inherited specializations,
configuration and directly affected templates consistent. Add focused behavioral
regressions where appropriate. Preserve approvals, privacy controls, provenance,
existing contributor credits and unrelated changes.

## Licensing and credit

Submit only material you are authorized to contribute and disclose any
third-party material and its license. Do not submit confidential employer or
customer content. Obtain any required employer or other rights-holder approval
before contributing.

Unless explicitly stated otherwise, contributions intentionally submitted for
inclusion are offered under Apache 2.0, as described in section 5 of
[LICENSE](LICENSE). Contributors retain their copyright unless separately
agreed. Keep applicable copyright, license and attribution notices.

[AUTHORS.md](AUTHORS.md) distinguishes original authorship, ownership and
maintenance. Citation and "Built with TWTTY" acknowledgments are welcome but
are not extra license conditions. A project created using TWTTY need not license
its independently authored code under Apache 2.0 merely because it used TWTTY;
copied framework material remains subject to its applicable license.

## Official repository and releases

Only the owner or explicitly authorized maintainers may modify the official
repository, manage its settings, merge changes or publish official releases.
Public readability and the right to fork do not grant those permissions.
Apache 2.0 still permits others to modify and redistribute their own copies.

The official `main` branch requires pull requests, all four Framework CI matrix
checks and resolved review threads, and blocks force pushes and deletion.
Outside contributions require owner review. For owner-authored pull requests,
the owner may bypass the independent-review requirement rather than approve
their own work; the separate pull-request, CI and history-protection rules
still apply. This solo-maintainer exception grants no bypass rights to outside
contributors. Protected `v*` tags cannot be updated or deleted.

There is no automatic release or auto-merge workflow in the prepared files.
Publication and any access changes require separate owner approval.
