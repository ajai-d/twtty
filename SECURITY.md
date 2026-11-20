# Security policy

TWTTY is in beta. No production-readiness guarantee, security
certification, supported-version SLA or response-time commitment is made.
Reports should identify the exact affected revision or release. The latest beta
is the initial focus for security fixes.

## Report vulnerabilities privately

Do not disclose vulnerabilities, exploit details, credentials or customer data
in public issues, discussions or pull requests.

Use GitHub private vulnerability reporting through
[Report a vulnerability](https://github.com/ajai-d/twtty/security/advisories/new)
from the repository's Security tab. Reports are routed privately to the
maintainer. No response-time commitment is made.

GitHub supports this route only for public repositories. Enable and verify it
immediately during public launch; if activation or verification fails, return
the repository to private until reporting is available. If the route is later
unavailable, use only a previously established private maintainer channel; no
email address or alternate contact is asserted here. Do not post the report
publicly.

Include the affected revision, impact, prerequisites and a minimal safe
reproduction with synthetic data. Do not send live credentials, private keys,
customer records or confidential employer material. Agree disclosure timing
with the maintainer; reporting is not permission to test third-party systems.

## Scope and limits

Relevant issues include unsafe behavior in the shared redaction utility,
exposure of secrets or identifiers, unsafe prompt/tool guidance and missing
approval or trust-boundary controls. The framework is interpreted by an AI
assistant; it is not an operating-system sandbox or a universal write interceptor.
Pattern scanning and AI review cannot guarantee removal of all sensitive data.

Suspected credential exposure requires private investigation and appropriate
revocation/rotation. Do not silently delete evidence or rewrite Git history;
any remediation and publication require explicit authorization.
