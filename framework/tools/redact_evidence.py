"""Conservative text redaction and create/append-only process-evidence writing."""

from __future__ import annotations

import argparse
from bisect import bisect_right
from collections import Counter
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
import hashlib
import hmac
import html
import ipaddress
import json
import os
from pathlib import Path
import re
import sys
from urllib.parse import quote, quote_plus, unquote
from uuid import uuid4


MAX_BYTES = 4 * 1024 * 1024
KINDS = frozenset({
    "secret", "private-key", "email", "phone", "url", "hostname", "ip-address",
    "path", "identifier", "resource-id", "resource-group", "project", "deployment",
    "account", "subscription", "tenant", "organization", "customer", "username",
    "git-identity",
    "person", "address", "location", "government-id", "financial", "health",
    "biometric", "personal", "business", "legal", "security",
})
_KINDS = "|".join(sorted(KINDS, key=len, reverse=True))
_PLAIN_TAG = re.compile(r"<REDACTED:(?:" + _KINDS + r")>")
_TAG = re.compile(
    r"<REDACTED:(?P<kind>" + _KINDS
    + r")-(?P<digest>[0-9a-f]{32})(?P<signature>[0-9a-f]{32})>"
)
_VALUE = r"""(?P<value>"(?:\\.|[^"\\\r\n])*"|'(?:\\.|[^'\\\r\n])*'|[^\r\n]+)"""


class RedactionError(ValueError):
    """A safe, value-free error suitable for reporting without input contents."""


@dataclass(frozen=True)
class RedactionResult:
    text: str
    counts: Mapping[str, int]


@dataclass(frozen=True, repr=False)
class _Match:
    start: int
    end: int
    kind: str
    canonical: str
    known: bool = False


def _assignment(keys: str) -> re.Pattern[str]:
    return re.compile(
        r"""(?i)(?<!\w)(?:\\?["'`*]){0,2}(?:""" + keys
        + r""")(?:\\?["'`*]){0,2}\s*[:=]\s*[*`]{0,2}""" + _VALUE
    )


_RULES = (
    ("private-key", re.compile(
        r"-----BEGIN (?:[A-Z0-9]+ )*PRIVATE KEY-----[\s\S]*?"
        r"(?:-----END (?:[A-Z0-9]+ )*PRIVATE KEY-----|\Z)"
    )),
    ("secret", _assignment(
        r"[a-z][a-z0-9_]*_(?:key|token|password|secret)|password|passwd|pwd|"
        r"api[-_ ]?key|client[-_ ]?secret|accountkey|access[-_ ]?token|refresh[-_ ]?token|"
        r"shared[-_ ]?access[-_ ]?(?:key|signature)|access[-_ ]?key|sas[-_ ]?token|"
        r"connection[-_ ]?string|authorization|signature|sig|token|secret|key"
    )),
    ("secret", re.compile(r"(?i)\b(?:Bearer|Basic)\s+(?P<value>[A-Za-z0-9._~+/%=-]+)")),
    ("secret", re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9_]{20,}|github_pat_[A-Za-z0-9_]{20,})\b")),
    ("secret", re.compile(
        r"\b(?:sk-(?:(?:proj|svcacct)-)?[A-Za-z0-9_-]{20,}|"
        r"sk_(?:live|test)_[A-Za-z0-9]{16,}|glpat-[A-Za-z0-9_-]{20,}|"
        r"xox[baprs]-[A-Za-z0-9-]{10,}|npm_[A-Za-z0-9]{20,}|AIza[A-Za-z0-9_-]{30,})\b"
    )),
    ("identifier", re.compile(r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b")),
    ("secret", re.compile(r"\beyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\b")),
    ("secret", re.compile(
        r"""(?i)\b(?:DefaultEndpointsProtocol|Endpoint|AccountEndpoint|Server|Data Source|Host)\s*="""
        r"""[^"'`\r\n]*\b(?:AccountKey|SharedAccessKey|SharedAccessSignature|AccessKey|Password|Pwd)"""
        r"""\s*=[^"'`\r\n]+"""
    )),
    ("identifier", re.compile(r"<REDACTED:[^>]*(?:>|\Z)")),
    ("url", re.compile(
        r"""(?i)\b(?:https?|s?ftp|ssh|ldaps?|sb|postgres(?:ql)?|rediss?|amqps?|mongodb(?:\+srv)?|file)"""
        r""":(?:\\?/){2}[^\s<>"'`]+"""
    )),
    ("url", re.compile(
        r"(?i)\b(?:https?|s?ftp|ssh|ldaps?|sb|postgres(?:ql)?|rediss?|amqps?|"
        r"mongodb(?:(?:\+|%2b|%252b)srv)?|file)"
        r"""(?:%3a(?:%2f){2}|%253a(?:%252f){2})[^\s<>"'`]+"""
    )),
    ("url", re.compile(r"""(?i)\bgit@[a-z0-9.-]+:[^\s<>"'`]+""")),
    ("resource-id", re.compile(
        r"""(?i)/subscriptions/[a-f0-9-]+(?:/[^\s<>"'`]+)?"""
    )),
    ("resource-id", re.compile(r"""(?i)\barn:aws[a-z-]*:[a-z0-9-]+:[^\s<>"'`]+""")),
    ("person", _assignment(r"(?:first|last|legal|person)[-_ ]?name")),
    ("address", _assignment(r"(?:(?:home|mailing|postal|street)[-_ ]?)?address|postal[-_ ]?code|zip[-_ ]?code")),
    ("location", _assignment(r"geolocation|latitude|longitude|gps|coordinates")),
    ("government-id", _assignment(
        r"ssn|social[-_ ]?security(?:[-_ ]?number)?|passport(?:[-_ ]?(?:number|id))?|"
        r"national[-_ ]?id|tax[-_ ]?id|driver[-_ ]?licen[cs]e"
    )),
    ("government-id", re.compile(r"(?<!\d)\d{3}-\d{2}-\d{4}(?!\d)")),
    ("financial", _assignment(
        r"(?:credit|debit)[-_ ]?card(?:[-_ ]?number)?|card[-_ ]?number|cvv|cvc|iban|"
        r"bank[-_ ]?account|routing[-_ ]?number|salary|income"
    )),
    ("financial", re.compile(r"(?<!\w)\d(?:[ -]?\d){12,18}(?!\w)")),
    ("personal", _assignment(r"date[-_ ]?of[-_ ]?birth|birth[-_ ]?date|dob|age|gender|religion|ethnicity")),
    ("health", _assignment(r"diagnosis|medical[-_ ]?(?:record|condition|id)|patient[-_ ]?id|prescription")),
    ("biometric", _assignment(r"fingerprint|face[-_ ]?(?:template|embedding)|voiceprint|dna")),
    ("legal", _assignment(r"case[-_ ]?number|legal[-_ ]?matter|privileged[-_ ]?advice")),
    ("business", _assignment(r"confidential|trade[-_ ]?secret|internal[-_ ]?(?:pricing|forecast|strategy)")),
    ("security", _assignment(r"recovery[-_ ]?codes?|security[-_ ]?answers?|session[-_ ]?id|cookie|set-cookie")),
    ("git-identity", re.compile(
        r"(?im)^(?:Author|Committer):\s*(?P<value>[^\r\n]+)"
    )),
    ("path", re.compile(
        r"""(?P<quote>["'`])(?P<value>(?:[A-Za-z]:[\\/]|\\\\|/home/|/Users/|/mnt/[a-z]/Users/)"""
        r"""[^\r\n]*?)(?P=quote)"""
    )),
    ("path", re.compile(r"""(?i)\b[A-Z]:[\\/][^\r\n"'`<>]+""")),
    ("path", re.compile(r"""\\\\[^\r\n"'`<>]+""")),
    ("path", re.compile(r"""(?:/home/|/Users/|/mnt/[a-z]/Users/)[^\r\n"'`<>]+""")),
    ("email", re.compile(r"(?<![\w.+-])[\w.!#$%&'*+/=?^`{|}~-]+@[\w-]+(?:\.[\w-]+)*\b")),
    ("username", re.compile(r"(?<![\w@])@(?P<value>[A-Za-z0-9][A-Za-z0-9_-]{1,38})\b")),
    ("phone", re.compile(r"(?<!\w)\+[1-9](?:[ ().-]*\d){6,14}(?!\w)")),
    ("phone", re.compile(r"(?<!\w)(?:\(\d{3}\)\s*|\d{3}[-. ])\d{3}[-. ]\d{4}(?!\d)")),
    ("identifier", re.compile(r"\b[0-9a-fA-F]{8}(?:-[0-9a-fA-F]{4}){3}-[0-9a-fA-F]{12}\b")),
    ("resource-group", re.compile(r"(?i)\brg-[a-z0-9][a-z0-9_-]*\b")),
    ("project", re.compile(r"(?i)\b(?:ai-project|foundry|aoai|aif)-[a-z0-9][a-z0-9_-]*\b")),
    ("hostname", re.compile(
        r"(?i)\b(?:[a-z0-9-]+\.)+(?:azure\.com|windows\.net|azurewebsites\.net)\b"
    )),
    ("identifier", _assignment(
        r"resource[-_ ]?group(?:[-_ ]?name)?|project[-_ ]?name|deployment[-_ ]?name|"
        r"account[-_ ]?(?:name|id)|tenant(?:[-_ ]?id)?|subscription(?:[-_ ]?id)?|"
        r"organization|org|owner|customer|username|user[-_ ]?(?:name|id)|user|"
        r"full[-_ ]?name|display[-_ ]?name|hostname|computer|machine|"
        r"git[-_ ]?author|user\.name|user\.email"
    )),
)
_IP = re.compile(
    r"(?<![\w:])(?:\d{1,3}\.){3}\d{1,3}(?![\w.])|"
    r"(?<![\w:])(?:[a-fA-F0-9]{0,4}:){2,}[a-fA-F0-9:.]*(?:%[\w.-]+)?"
)


class Redactor:
    def __init__(
        self, key: bytes | None = None,
        known_identifiers: Mapping[str, Sequence[str]] | None = None,
        *, require_key: bool = False,
    ) -> None:
        if require_key and key is None:
            raise RedactionError("The explicitly selected legacy keyed mode requires its existing key.")
        if key is not None and (not isinstance(key, bytes) or len(key) < 32):
            raise RedactionError("An explicitly supplied legacy redaction key must be at least 32 bytes.")
        self._key = key
        self._known: list[tuple[str, str, re.Pattern[str]]] = []
        seen: dict[str, tuple[str, str]] = {}
        if known_identifiers is not None and not isinstance(known_identifiers, Mapping):
            raise RedactionError("Known-identifier context must be a mapping.")
        for kind, values in (known_identifiers or {}).items():
            if kind not in KINDS or not isinstance(values, (list, tuple)):
                raise RedactionError("Known-identifier context has an unsupported kind or value list.")
            for value in values:
                if not isinstance(value, str) or not value.strip() or len(value) > MAX_BYTES:
                    raise RedactionError("Known-identifier values must be nonempty bounded strings.")
                try:
                    value.encode("utf-8")
                except UnicodeEncodeError:
                    raise RedactionError("Known identifiers must be valid UTF-8 text.") from None
                if any(ord(c) < 32 for c in value):
                    raise RedactionError("Known identifiers must not contain control characters.")
                variants = {value, html.escape(value, quote=True), json.dumps(value)[1:-1],
                            value.replace("/", r"\/")}
                variants.update({quote(value, safe=""), quote_plus(value, safe="")})
                variants.add(quote(quote(value, safe=""), safe=""))
                for variant in variants:
                    folded = variant.casefold()
                    if folded in seen and seen[folded] != (kind, value):
                        raise RedactionError("Known-identifier context has ambiguous overlapping values.")
                    seen[folded] = (kind, value)
                    left = r"(?<!\w)" if variant[0].isalnum() else ""
                    right = r"(?!\w)" if variant[-1].isalnum() else ""
                    self._known.append((kind, value, re.compile(
                        left + re.escape(variant) + right, re.IGNORECASE | re.ASCII,
                    )))

    def _signature(self, kind: str, digest: str) -> str:
        if self._key is None:
            raise RedactionError("Legacy marker authentication requires its existing key.")
        return hmac.new(self._key, f"tag\0{kind}\0{digest}".encode(), hashlib.sha256).hexdigest()[:32]

    def _digest(self, kind: str, value: str) -> str:
        if self._key is None:
            raise RedactionError("Legacy pseudonyms require their existing key.")
        return hmac.new(
            self._key, f"value\0{kind}\0{value}".encode(), hashlib.sha256,
        ).hexdigest()[:32]

    def _alias(self, kind: str, value: str) -> str:
        if self._key is None:
            return f"<REDACTED:{kind}>"
        digest = self._digest(kind, value)
        return f"<REDACTED:{kind}-{digest}{self._signature(kind, digest)}>"

    def branch_token(self, branch_name: str) -> str:
        """Allocate a random reference, or recover the legacy keyed reference."""
        if not isinstance(branch_name, str) or not branch_name or any(
            ord(c) <= 32 or ord(c) == 127 for c in branch_name
        ):
            raise RedactionError("A single nonempty branch name is required.")
        try:
            size = len(branch_name.encode("utf-8"))
        except UnicodeEncodeError:
            raise RedactionError("Branch name must be valid UTF-8 text.") from None
        if size > MAX_BYTES:
            raise RedactionError("Branch name exceeds the supported size.")
        return uuid4().hex if self._key is None else self._digest("branch", branch_name)

    def redact(self, text: str) -> RedactionResult:
        if not isinstance(text, str):
            raise RedactionError("Evidence must be bounded UTF-8 text.")
        try:
            size = len(text.encode("utf-8"))
        except UnicodeEncodeError:
            raise RedactionError("Evidence must be bounded UTF-8 text.") from None
        if size > MAX_BYTES:
            raise RedactionError("Evidence must be bounded UTF-8 text.")
        if any(ord(c) < 32 and c not in "\t\r\n" for c in text):
            raise RedactionError("Binary/control-character evidence is unsupported.")
        protected = [tag.span() for tag in _PLAIN_TAG.finditer(text)]
        for tag in _TAG.finditer(text) if self._key is not None else ():
            if not hmac.compare_digest(
                tag["signature"], self._signature(tag["kind"], tag["digest"]),
            ):
                raise RedactionError("A redaction marker is invalid for this project key.")
            protected.append(tag.span())
        protected.sort()
        protected_starts = [a for a, _ in protected]
        matches: list[_Match] = []

        def add(start: int, end: int, kind: str, canonical: str, known: bool = False) -> None:
            if start >= end:
                return
            first = bisect_right(protected_starts, start) - 1
            if first >= 0 and end <= protected[first][1]:
                return
            original = (start, end)
            if first >= 0 and start < protected[first][1]:
                start = protected[first][0]
            last = bisect_right(protected_starts, end - 1) - 1
            if last >= 0:
                end = max(end, protected[last][1])
            if (start, end) != original:
                canonical = text[start:end]
            matches.append(_Match(start, end, kind, canonical, known))

        for kind, pattern in _RULES:
            for match in pattern.finditer(text):
                start, end = match.span("value") if "value" in pattern.groupindex else match.span()
                if text[start:start + 1] in ('"', "'") and text[end - 1:end] == text[start]:
                    start, end = start + 1, end - 1
                if kind in ("url", "resource-id"):
                    while end > start and text[end - 1] in ".,;":
                        end -= 1
                    for opening, closing in (("(", ")"), ("[", "]"), ("{", "}")):
                        while text[start:end].count(closing) > text[start:end].count(opening) and text[end - 1] == closing:
                            end -= 1
                canonical = text[start:end]
                if kind == "url":
                    canonical = canonical.replace(r"\/", "/")
                    try:
                        if re.match(r"(?i)^[a-z0-9+%]+%253a(?:%252f){2}", canonical):
                            canonical = unquote(unquote(canonical, errors="strict"), errors="strict")
                        elif re.match(r"(?i)^[a-z0-9+%]+%3a(?:%2f){2}", canonical):
                            canonical = unquote(canonical, errors="strict")
                    except UnicodeDecodeError:
                        raise RedactionError("Encoded URL must contain valid UTF-8 text.") from None
                add(start, end, kind, canonical)
        for match in _IP.finditer(text):
            try:
                ipaddress.ip_address(match[0])
            except ValueError:
                continue
            add(*match.span(), "ip-address", match[0])
        for kind, value, pattern in self._known:
            for match in pattern.finditer(text):
                add(*match.span(), kind, value, known=True)

        matches.sort(key=lambda m: (m.start, -(m.end - m.start)))
        groups: list[list[_Match]] = []
        group_end = -1
        for match in matches:
            if groups and match.start < group_end:
                groups[-1].append(match)
                group_end = max(group_end, match.end)
            else:
                groups.append([match])
                group_end = match.end
        counts: Counter[str] = Counter()
        pieces: list[str] = []
        cursor = 0
        for group in groups:
            start, end = min(m.start for m in group), max(m.end for m in group)
            chosen = max(group, key=lambda m: (m.end - m.start, m.known))
            value = chosen.canonical if (chosen.start, chosen.end) == (start, end) else text[start:end]
            pieces.extend((text[cursor:start], self._alias(chosen.kind, value)))
            counts[chosen.kind] += 1
            cursor = end
        pieces.append(text[cursor:])
        return RedactionResult("".join(pieces), dict(counts))


def write_evidence(
    text: str, output: Path, *, root: Path, redactor: Redactor, append: bool = False,
) -> RedactionResult:
    """Sanitize first, then create/append; never overwrite existing evidence."""
    try:
        root = root.resolve()
        if not root.is_dir():
            raise RedactionError("An existing approved evidence root is required.")
        candidate = root / output
        if any(p.is_symlink() for p in (candidate, *candidate.parents)):
            raise RedactionError("Evidence writes must not follow symbolic links.")
        target = candidate.resolve()
        if target.exists() and target.stat().st_nlink > 1:
            raise RedactionError("Evidence writes must not follow hard links.")
    except (OSError, RuntimeError):
        raise RedactionError("Evidence destination could not be resolved safely.") from None
    if ".." in output.parts:
        raise RedactionError("Evidence output must stay inside the approved root.")
    if not target.is_relative_to(root):
        raise RedactionError("Evidence output must stay inside the approved root.")
    relative = target.relative_to(root)
    if ".git" in {p.casefold() for p in target.parts} or not {
        "replay-execution", "reports",
    }.intersection(relative.parts):
        raise RedactionError("Output must be process evidence, not native Git or source metadata.")
    if target.name.upper().startswith(("LICENSE", "COPYING", "COPYRIGHT", "NOTICE")):
        raise RedactionError("Original license/copyright notices must not be rewritten.")
    result = redactor.redact(text)
    try:
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open("a" if append else "x", encoding="utf-8", newline="") as stream:
            stream.write(result.text)
    except OSError:
        raise RedactionError("Evidence write failed; existing evidence is not overwritten.") from None
    return result


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--output", type=Path, help="Create a new evidence file; otherwise emit sanitized text.")
    parser.add_argument("--append", action="store_true", help="Append only sanitized new content to --output.")
    parser.add_argument("--require-key", action="store_true",
                        help="Compatibility only: require the key for an already adopted keyed workflow.")
    parser.add_argument("--branch-token", action="store_true",
                        help="Allocate a private branch reference once; recover it from opening evidence on Resume.")
    args = parser.parse_args(argv)
    try:
        if args.append and args.output is None:
            raise RedactionError("--append requires an evidence output.")
        if args.branch_token and args.output is not None:
            raise RedactionError("--branch-token cannot write an evidence output.")
        try:
            configured_key = os.environ.get("TWTTY_REDACTION_KEY")
            key = configured_key.encode("utf-8") if configured_key is not None else None
        except UnicodeEncodeError:
            raise RedactionError("Redaction key must be valid UTF-8 text.") from None
        context = {}
        if not args.branch_token:
            try:
                context = json.loads(os.environ.get("TWTTY_REDACTION_CONTEXT", "{}"))
            except json.JSONDecodeError:
                raise RedactionError("Known-identifier context is not valid JSON.") from None
        if not isinstance(context, dict):
            raise RedactionError("Known-identifier context must be a JSON object.")
        redactor = Redactor(key, context, require_key=args.require_key)
        raw = sys.stdin.buffer.read(MAX_BYTES + 1)
        if len(raw) > MAX_BYTES:
            raise RedactionError("Evidence input exceeds the supported size.")
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError:
            raise RedactionError("Evidence input must be UTF-8 text.") from None
        if args.branch_token:
            token = redactor.branch_token(text.rstrip("\r\n"))
            sys.stdout.buffer.write((token + "\n").encode("utf-8"))
            return 0
        result = (write_evidence(text, args.output, root=args.root, redactor=redactor, append=args.append)
                  if args.output is not None else redactor.redact(text))
        if args.output is None:
            sys.stdout.buffer.write(result.text.encode("utf-8"))
        return 0
    except (RedactionError, OSError):
        print("Redaction failed; no unredacted fallback is permitted. Check context, text, destination and any legacy key setting.",
              file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
