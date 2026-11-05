#!/usr/bin/env python3
"""claim_check.py - verify every number in a draft against a claims ledger.

Executive offers fall apart at the background check and the reference call, not at the
resume screen. A claims ledger is the one place where each fact has a canonical wording,
a status and a source. This script is the claim freeze: it refuses any draft (resume,
pitch, LinkedIn About, interview answer, thank-you note) that says something the ledger
does not.

Checks (FAIL unless noted):
  unknown-number   a money amount, percent, multiplier or count that no ledger claim carries
  qualifier        the number matches but its "+" differs from the ledger ("41,000" vs "41,000+")  [warn]
  private-figure   a number the ledger marks internal (public: false), on an external surface
  unbound-growth   a growth number with no role, employer or tenure year in its sentence,
                   paragraph or section header
  misattributed    a number placed under a role it does not belong to
  beyond-tenure    "over N years" next to a ledger number, where N exceeds that role's tenure
  role-dates       a role header whose year range differs from the ledger
  forbidden        a ledger pattern (stale status, wrong metric type, overclaim) matched
  anachronism      a term inside a role that became public after the role ended
  unknown-year     a year outside every role and claim in the ledger  [warn]

Usage:
  python3 scripts/claim_check.py draft.md examples/claims-ledger.example.json
  python3 scripts/claim_check.py draft.md ledger.json --json
  python3 scripts/claim_check.py draft.md ledger.json --surface internal   # allow private figures

Exit status: 0 when no FAIL, 1 when any FAIL, 2 on a usage or ledger error.
Python 3.8+, standard library only. Ledger format: references/claims-ledger.md.
"""
from __future__ import annotations

import json
import re
import sys
from dataclasses import asdict, dataclass

NUM = re.compile(
    r"(?<![\w.$\u20ac\u00a3])(?<![A-Za-z]-)"
    r"(?P<cur>[$\u20ac\u00a3])?"
    r"(?P<num>\d{1,3}(?:,\d{3})+|\d+)(?:\.(?P<dec>\d+))?"
    r"(?:\s?(?P<scale>[KMB]\b|bn\b|million\b|billion\b|thousand\b|k\b))?"
    r"(?P<plus>\+)?"
    r"(?P<suffix>%|x\b|X\b|\s?percent\b|\s?bps\b|\s?basis points\b)?",
)
SCALE = {"k": 1e3, "thousand": 1e3, "m": 1e6, "million": 1e6, "b": 1e9, "bn": 1e9, "billion": 1e9}
DEFAULT_NON_CLAIMS = [
    r"\b\d+[- ]?(second|minute|hour)s?\b",
    r"\b(first|next|last|within) \d+ (days|weeks|hours)\b",
    r"\b\d+ (days|weeks)\b",
    r"\btop[- ]\d+\b",
    r"\b\d+ of \d+\b",
    r"\b1:1s?\b",
    r"\b24/7\b",
    r"\bL\d+\b",
    r"\bQ[1-4]\b",
    r"\b(over|in|across|within) \d+ years?\b",
    r"\b(week|day|month|step|phase|round|stage|mock|question|story|stories)s? \d+(\s*(to|and|-)\s*\d+)?\b",
]
LIST_MARKER = re.compile(r"^\s*(?:[-*\u2022]|\d{1,2}[.)])\s+")
TENURE_SPAN = re.compile(r"\b(?:over|in|across|within) (\d+) years?\b", re.I)
RANGE = re.compile(r"\b((?:19|20)\d{2})\s*-\s*((?:19|20)\d{2}|Present|present|now|today)\b")
SENT_SPLIT = re.compile(r"(?<=[.!?])\s+(?=[A-Z\"'(])")


@dataclass
class Finding:
    rule: str
    severity: str
    line: int
    match: str
    reason: str

    def show(self) -> str:
        return "%-4s %-15s line %-3d %s\n     %s" % (self.severity.upper(), self.rule, self.line,
                                                   self.match[:100], self.reason)


@dataclass
class Token:
    kind: str     # money, pct, mult, bps, count, year
    value: float
    plus: bool
    text: str
    start: int
    end: int


# ---------------------------------------------------------------- parsing

def normalize(text: str) -> str:
    return (text.replace("\u2013", "-").replace("\u2014", "-")
            .replace("\u2018", "'").replace("\u2019", "'")
            .replace("\u201c", '"').replace("\u201d", '"'))


def tokens(text: str):
    out = []
    for m in NUM.finditer(text):
        nxt = text[m.end():m.end() + 1]
        has_unit = m.group("cur") or m.group("scale") or m.group("suffix") or m.group("plus")
        if nxt.isalpha() and not has_unit:
            continue  # 1st, 3D, 5G, v2-style tokens
        raw = m.group("num").replace(",", "")
        value = float(raw + ("." + m.group("dec") if m.group("dec") else ""))
        scale = (m.group("scale") or "").lower()
        if scale:
            value *= SCALE[scale]
        suffix = (m.group("suffix") or "").strip().lower()
        if m.group("cur"):
            kind = "money"
        elif suffix in ("%", "percent"):
            kind = "pct"
        elif suffix == "x":
            kind = "mult"
        elif suffix in ("bps", "basis points"):
            kind = "bps"
        elif not scale and not m.group("dec") and 1900 <= value <= 2099 and len(raw) == 4:
            kind = "year"
        else:
            kind = "count"
        out.append(Token(kind, value, bool(m.group("plus")), m.group(0).strip(), m.start(), m.end()))
    return out


def same(a: Token, b: Token) -> bool:
    return a.kind == b.kind and abs(a.value - b.value) <= 1e-9 * max(1.0, abs(a.value))


def load_ledger(path: str) -> dict:
    with open(path, encoding="utf-8") as fh:
        ledger = json.load(fh)
    roles = {r["id"]: r for r in ledger.get("roles", [])}
    for c in ledger.get("claims", []):
        if c.get("role") and c["role"] not in roles:
            raise ValueError("claim %r names unknown role %r" % (c.get("id"), c["role"]))
    return ledger


def role_names(role: dict):
    names = [role.get("employer", "")] + list(role.get("aliases", []))
    return [n for n in names if n]


def role_end(role: dict, as_of: int) -> int:
    end = role.get("end")
    return as_of if isinstance(end, str) else int(end)


# ---------------------------------------------------------------- context

def build_context(text: str, ledger: dict):
    """For every line, the role in force from a section header (a short line naming a role)."""
    roles = ledger.get("roles", [])
    header_role = []
    current = None
    for line in text.split("\n"):
        if is_header(line):
            hit = mentioned_roles(line, roles)
            if hit:
                current = hit[-1]
        header_role.append(current)
    return header_role


def is_header(line: str) -> bool:
    """A short line that names a section: no list marker, no sentence end, no claim numbers."""
    if LIST_MARKER.match(line):
        return False
    stripped = line.strip().lstrip("#> ").strip("* ").strip()
    if not stripped or len(stripped.split()) > 12 or stripped.endswith((".", "?", "!")):
        return False
    return all(t.kind == "year" for t in tokens(stripped))


def mentioned_roles(text: str, roles):
    found = []
    for r in roles:
        for n in role_names(r):
            for m in re.finditer(r"\b%s\b" % re.escape(n), text, re.I):
                found.append((m.start(), r["id"]))
    return [rid for _, rid in sorted(found)]


def units(text: str):
    """Yield (line_number, paragraph_text, sentence_text, sentence_offset_in_paragraph)."""
    lines = text.split("\n")
    i = 0
    while i < len(lines):
        if not lines[i].strip():
            i += 1
            continue
        start = i
        block = []
        while i < len(lines) and lines[i].strip():
            block.append(lines[i])
            i += 1
        # list items and table rows are their own paragraphs
        groups, cur, cur_start = [], [], start
        for k, l in enumerate(block):
            starts_item = LIST_MARKER.match(l) or l.lstrip().startswith("|") or is_header(l)
            if starts_item and cur:
                groups.append((cur_start, cur))
                cur, cur_start = [], start + k
            cur.append(LIST_MARKER.sub("", l, count=1))
        if cur:
            groups.append((cur_start, cur))
        for g_start, g in groups:
            parts = [x.strip() for x in g]
            para = " ".join(parts)
            line_starts, acc = [], 0
            for x in parts:
                line_starts.append(acc)
                acc += len(x) + 1
            pos = 0
            for s in SENT_SPLIT.split(para):
                off = para.find(s, pos)
                pos = off + len(s)
                row = max(k for k, st in enumerate(line_starts) if st <= off)
                yield g_start + row + 1, para, s, off


# ---------------------------------------------------------------- checks

def check(text: str, ledger: dict, surface: str = "external"):
    text = normalize(text)
    as_of = int(str(ledger.get("as_of", "2026"))[:4])
    roles = {r["id"]: r for r in ledger.get("roles", [])}
    role_list = ledger.get("roles", [])
    claims = ledger.get("claims", [])
    claim_tokens = [(c, tokens(normalize(c.get("text", "")) + " " + " ".join(c.get("also", [])))) for c in claims]
    years = set()
    for r in role_list:
        years.update(range(int(r["start"]), role_end(r, as_of) + 1))
    for c, toks in claim_tokens:
        years.update(int(t.value) for t in toks if t.kind == "year")
    non_claims = [re.compile(p, re.I) for p in DEFAULT_NON_CLAIMS + ledger.get("non_claims", [])]
    header_role = build_context(text, ledger)
    findings = []
    checked = matched = 0

    def add(rule, line, match, reason, sev="fail"):
        findings.append(Finding(rule, sev, line, match.strip(), reason))

    for lineno, para, sent, off in units(text):
        spans = [(m.start(), m.end()) for rx in non_claims for m in rx.finditer(sent)]
        in_sent = mentioned_roles(sent, role_list)
        before = mentioned_roles(para[:off], role_list)
        ctx = in_sent[-1:] or before[-1:] or ([header_role[lineno - 1]] if header_role[lineno - 1] else [])
        ctx_role = ctx[0] if ctx else None
        ledger_number_in_sentence = False
        for t in tokens(sent):
            if any(a <= t.start < b for a, b in spans):
                continue
            if t.kind == "year":
                if int(t.value) not in years:
                    add("unknown-year", lineno, sent, "%s is outside every role and claim in the ledger" % t.text, "warn")
                continue
            checked += 1
            hits = [(c, lt) for c, toks in claim_tokens for lt in toks if same(t, lt)]
            if not hits:
                add("unknown-number", lineno, sent,
                    "%s is not in the ledger; add it with a source, or cut it" % t.text)
                continue
            matched += 1
            ledger_number_in_sentence = True
            public_hits = [(c, lt) for c, lt in hits if c.get("public", True)]
            if not public_hits and surface == "external":
                add("private-figure", lineno, sent, "%s is internal (%s); external surfaces use the public figure"
                    % (t.text, hits[0][0].get("rule") or hits[0][0]["id"]))
                continue
            pool = public_hits or hits
            if not any(lt.plus == t.plus for _, lt in pool):
                add("qualifier", lineno, sent, "%s: the ledger writes it as %s" % (t.text, pool[0][1].text), "warn")
            owners = {c.get("role") for c, _ in pool if c.get("role")}
            if owners and ctx_role and ctx_role not in owners:
                add("misattributed", lineno, sent, "%s belongs to %s, but this sits under %s"
                    % (t.text, " or ".join(sorted(roles[o].get("employer", o) for o in owners)),
                       roles[ctx_role].get("employer", ctx_role)))
                continue
            if all(c.get("kind") == "growth" for c, _ in pool):
                if not ctx_role and not any(int(y.value) in years for y in tokens(sent) if y.kind == "year"):
                    add("unbound-growth", lineno, sent,
                        "%s is a growth claim; name the role or employer it happened in" % t.text)
        if ledger_number_in_sentence and ctx_role:
            r = roles[ctx_role]
            tenure = role_end(r, as_of) - int(r["start"])
            for m in TENURE_SPAN.finditer(sent):
                if int(m.group(1)) > max(tenure, 1):
                    add("beyond-tenure", lineno, sent, "'%s' but the %s tenure is %d years in the ledger"
                        % (m.group(0), r.get("employer", ctx_role), tenure))

    # role headers: year ranges must match the ledger
    for i, line in enumerate(text.split("\n"), 1):
        m = RANGE.search(line)
        if not m:
            continue
        named = mentioned_roles(line, role_list)
        if not named and header_role[i - 1] and len(line.split()) <= 6:
            named = [header_role[i - 1]]
        if not named:
            continue
        r = roles[named[-1]]
        want_end = str(r["end"])
        got_end = m.group(2)
        ok_end = (want_end.lower() == "present" and got_end.lower() in ("present", "now", "today")) or got_end == want_end
        if int(m.group(1)) != int(r["start"]) or not ok_end:
            add("role-dates", i, line, "the ledger has %s %s-%s" % (r.get("employer", r["id"]), r["start"], r["end"]))

    # forbidden patterns from the ledger
    status = {c["id"]: c.get("status") for c in claims}
    proof = {c["id"]: (c.get("proof") or {}) for c in claims}
    for f in ledger.get("forbidden", []):
        when = f.get("when")
        if when and status.get(when["claim"]) != when["status"]:
            continue
        unless = f.get("unless_proof")
        if unless and any(v for v in proof.get(unless, {}).values()):
            continue  # the claim now has proof on record (a number, a link, an approval)
        rx = re.compile(f["pattern"], re.I)
        for i, line in enumerate(text.split("\n"), 1):
            if rx.search(line):
                add("forbidden", i, line, "%s: %s" % (f.get("id", "rule"), f["reason"]), f.get("severity", "fail"))

    # anachronisms: a term inside a role that ended before the term existed
    for a in ledger.get("anachronisms", []):
        rx = re.compile(a["pattern"], re.I)
        for lineno, para, sent, off in units(text):
            if not rx.search(sent):
                continue
            in_sent = mentioned_roles(sent, role_list)
            before = mentioned_roles(para[:off], role_list)
            ctx = in_sent[-1:] or before[-1:] or ([header_role[lineno - 1]] if header_role[lineno - 1] else [])
            for rid in ctx:
                r = roles[rid]
                if role_end(r, as_of) < int(a["first_public"]):
                    add("anachronism", lineno, sent, "%s first public %s (%s); %s ended %s"
                        % (a["term"], a["first_public"], a.get("source", "ledger"), r.get("employer", rid), r["end"]))
    findings.sort(key=lambda f: (f.line, f.rule))
    return findings, checked, matched


# ---------------------------------------------------------------- CLI

def main(argv=None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if len(argv) < 2 or argv[0] in ("-h", "--help"):
        print(__doc__)
        return 2
    draft_path, ledger_path = argv[0], argv[1]
    surface = argv[argv.index("--surface") + 1] if "--surface" in argv else "external"
    try:
        ledger = load_ledger(ledger_path)
        if draft_path == "-":
            text = sys.stdin.read()
        else:
            with open(draft_path, encoding="utf-8") as fh:
                text = fh.read()
    except (OSError, ValueError, KeyError) as exc:
        print("claim_check.py: %s" % exc, file=sys.stderr)
        return 2
    findings, checked, matched = check(text, ledger, surface)
    fails = sum(1 for f in findings if f.severity == "fail")
    warns = len(findings) - fails
    if "--json" in argv:
        print(json.dumps({"draft": draft_path, "ledger": ledger_path, "numbers_checked": checked,
                          "numbers_in_ledger": matched, "fails": fails, "warns": warns,
                          "findings": [asdict(f) for f in findings]}, indent=1))
    else:
        print("claim_check: %s against %s" % (draft_path, ledger_path))
        for f in findings:
            print(f.show())
        print("numbers checked %d, in ledger %d; %d fail, %d warn" % (checked, matched, fails, warns))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
