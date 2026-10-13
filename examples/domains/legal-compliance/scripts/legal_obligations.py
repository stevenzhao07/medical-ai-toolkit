#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""legal_obligations.py — contract clause → obligation ledger.

A minimal, non-medical module built on the same `lgd-skeleton/1.0` contract as the
21 medical repositories. It exists to demonstrate a claim made in this matrix:
the skeleton is industry-neutral. The contract (module.json + entry + --demo) is
identical; only the domain content differs.

Zero third-party dependencies — standard library only.

Usage:
    python scripts/legal_obligations.py --demo
    python scripts/legal_obligations.py --clauses my_clauses.json
    python scripts/legal_obligations.py --demo --json
"""
from __future__ import annotations

import argparse
import json
import sys

DEMO_CLAUSES = [
    {"clause": "7.2", "obligation": "Notify the customer of any security incident",
     "party": "vendor", "trigger": "incident discovered", "deadline": "72h",
     "owner": "Security Lead"},
    {"clause": "9.1", "obligation": "Deliver an annual compliance attestation",
     "party": "vendor", "trigger": "end of contract year", "deadline": "annually",
     "owner": "Compliance Officer"},
    {"clause": "11.4", "obligation": "Return or destroy all customer data",
     "party": "vendor", "trigger": "termination", "deadline": "",
     "owner": "Data Protection Lead"},
    {"clause": "5.3", "obligation": "Pay undisputed invoices within the stated period",
     "party": "customer", "trigger": "invoice received", "deadline": "30d",
     "owner": "Finance"},
    {"clause": "6.7", "obligation": "Provide written notice before subcontracting",
     "party": "vendor", "trigger": "subcontractor change", "deadline": "15d",
     "owner": "Legal"},
]

REQUIRED_FIELDS = ("clause", "obligation", "party", "trigger")


def urgency(deadline: str) -> str:
    """Classify a deadline string. Deliberately conservative: anything that
    cannot be parsed is reported as unspecified rather than assumed benign."""
    d = (deadline or "").strip().lower()
    if not d:
        return "unspecified"
    if d.endswith("h"):
        return "high"
    if d.endswith("d"):
        try:
            n = int(d[:-1])
        except ValueError:
            return "unspecified"
        return "high" if n <= 7 else "medium"
    if d in ("annually", "annual", "yearly"):
        return "low"
    return "unspecified"


def validate(clauses: list[dict]) -> list[str]:
    problems = []
    for i, c in enumerate(clauses):
        for f in REQUIRED_FIELDS:
            if not str(c.get(f, "")).strip():
                problems.append("clause #%d (%s): missing %s"
                                % (i + 1, c.get("clause") or "?", f))
    return problems


def build_ledger(clauses: list[dict]) -> list[dict]:
    out = []
    for c in clauses:
        out.append({
            "clause": c.get("clause", ""),
            "obligation": c.get("obligation", ""),
            "party": c.get("party", ""),
            "trigger": c.get("trigger", ""),
            "deadline": c.get("deadline", "") or "—",
            "owner": c.get("owner", "") or "—",
            "urgency": urgency(c.get("deadline", "")),
        })
    rank = {"high": 0, "medium": 1, "low": 2, "unspecified": 3}
    out.sort(key=lambda r: (rank[r["urgency"]], r["clause"]))
    return out


def render(ledger: list[dict], problems: list[str]) -> str:
    lines = ["### Obligation ledger", "",
             "| Clause | Obligation | Party | Triggered by | Deadline | Internal owner | Urgency |",
             "|---|---|---|---|---|---|---|"]
    for r in ledger:
        lines.append("| %s | %s | %s | %s | %s | %s | %s |"
                     % (r["clause"], r["obligation"], r["party"], r["trigger"],
                        r["deadline"], r["owner"], r["urgency"]))

    by_party: dict[str, int] = {}
    by_urgency: dict[str, int] = {}
    for r in ledger:
        by_party[r["party"]] = by_party.get(r["party"], 0) + 1
        by_urgency[r["urgency"]] = by_urgency.get(r["urgency"], 0) + 1

    lines += ["", "### Summary", "",
              "- By party: " + ", ".join("%s=%d" % kv for kv in sorted(by_party.items())),
              "- By urgency: " + ", ".join("%s=%d" % kv for kv in sorted(by_urgency.items()))]

    unspec = [r["clause"] for r in ledger if r["urgency"] == "unspecified"]
    if unspec:
        lines += ["", "### Needs attention",
                  "The following clauses carry an obligation with no machine-readable deadline "
                  "(clauses %s). A clause without a deadline is the most common reason an "
                  "obligation is missed in practice — assign one before relying on this ledger."
                  % ", ".join(unspec)]

    if problems:
        lines += ["", "### Input problems", ""] + ["- " + p for p in problems]

    lines += ["", "_This is a structural aid, not legal advice. Clause interpretation and "
              "enforceability depend on the governing law and the full contract text._"]
    return "\n".join(lines)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        description="Build an obligation ledger from contract clauses "
                    "(non-medical example module on the lgd-skeleton/1.0 contract)")
    ap.add_argument("--demo", action="store_true", help="run the built-in sample clauses")
    ap.add_argument("--clauses", metavar="FILE", help="JSON file with a list of clause objects")
    ap.add_argument("--json", action="store_true", help="emit JSON instead of Markdown")
    args = ap.parse_args(argv)

    if args.clauses:
        try:
            with open(args.clauses, encoding="utf-8") as fh:
                clauses = json.load(fh)
        except FileNotFoundError:
            print("[error] clause file not found: %s" % args.clauses, file=sys.stderr)
            return 2
        except json.JSONDecodeError as exc:
            print("[error] clause file is not valid JSON: %s" % exc, file=sys.stderr)
            return 2
        if not isinstance(clauses, list):
            print("[error] clause file must contain a JSON list", file=sys.stderr)
            return 2
    elif args.demo:
        clauses = DEMO_CLAUSES
    else:
        ap.print_help()
        return 1

    problems = validate(clauses)
    ledger = build_ledger(clauses)

    if args.json:
        print(json.dumps({"ledger": ledger, "problems": problems},
                         ensure_ascii=False, indent=2))
    else:
        print(render(ledger, problems))
    return 0


if __name__ == "__main__":
    sys.exit(main())
