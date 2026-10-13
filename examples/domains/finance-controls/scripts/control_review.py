#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""control_review.py — transaction ledger → internal-control findings.

A second non-medical module on the same `lgd-skeleton/1.0` contract as the 21
medical repositories. Two unrelated domains now share one contract with no change
to the core — which is the point.

Rules are deterministic and print their own reasoning. Nothing is scored or
ranked by a model; a finding either matches a stated rule or it does not.

Zero third-party dependencies — standard library only.

Usage:
    python scripts/control_review.py --demo
    python scripts/control_review.py --transactions my_ledger.json
    python scripts/control_review.py --demo --json
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import sys

THRESHOLDS = {
    "dual_approval": 10000.0,  # amount at or above this needs two approvers
    "review": 5000.0,          # amount at or above this must carry an approver
    "round_amount_min": 1000.0,
}

DEMO_TRANSACTIONS = [
    {"id": "T-1001", "date": "2026-10-01", "amount": 12500.00, "account": "AP-2100",
     "counterparty": "Northwind", "approvers": []},
    {"id": "T-1002", "date": "2026-10-01", "amount": 980.00, "account": "AP-2100",
     "counterparty": "Contoso", "approvers": ["L. Chen"]},
    {"id": "T-1003", "date": "2026-10-01", "amount": 12500.00, "account": "AP-2100",
     "counterparty": "Northwind", "approvers": ["L. Chen"]},
    {"id": "T-1004", "date": "2026-10-03", "amount": 50000.00, "account": "AP-2100",
     "counterparty": "Fabrikam", "approvers": ["L. Chen", "M. Ortiz"]},
    {"id": "T-1005", "date": "2026-10-04", "amount": 2000.00, "account": "AP-2100",
     "counterparty": "Tailspin", "approvers": ["M. Ortiz"]},
    {"id": "T-1006", "date": "2026-10-05", "amount": 3000.00, "account": "AP-2100",
     "counterparty": "Adventure Works", "approvers": ["M. Ortiz"]},
]

SEVERITY_ORDER = {"high": 0, "medium": 1, "low": 2}


def _amount(t: dict) -> float:
    try:
        return float(t.get("amount") or 0)
    except (TypeError, ValueError):
        return 0.0


def _approvers(t: dict) -> list:
    raw = t.get("approvers")
    if raw is None:
        single = (t.get("approver") or "").strip()
        raw = [single] if single else []
    return [a for a in raw if str(a).strip()]


def _is_weekend(date_str: str) -> bool:
    try:
        return dt.date.fromisoformat(str(date_str)).weekday() >= 5
    except ValueError:
        return False


def review(transactions: list) -> list:
    """Return a list of findings: dict(id, rule, severity, detail)."""
    findings = []

    # rule: probable duplicate — same date + counterparty + amount appears more than once
    seen: dict = {}
    for t in transactions:
        key = (str(t.get("date")), str(t.get("counterparty", "")).strip().lower(),
               round(_amount(t), 2))
        seen.setdefault(key, []).append(str(t.get("id", "?")))

    for t in transactions:
        tid = str(t.get("id", "?"))
        amount = _amount(t)
        approvers = _approvers(t)

        if not approvers:
            findings.append({"id": tid, "rule": "missing_approval", "severity": "high",
                             "detail": "No approver recorded for this posting."})

        if amount >= THRESHOLDS["dual_approval"] and len(approvers) < 2:
            findings.append({"id": tid, "rule": "dual_approval_required", "severity": "high",
                             "detail": "Amount %.2f is at or above the dual-approval threshold "
                                       "%.2f; %d approver(s) recorded."
                                       % (amount, THRESHOLDS["dual_approval"], len(approvers))})

        if amount >= THRESHOLDS["review"] and len(approvers) < 1:
            findings.append({"id": tid, "rule": "review_required", "severity": "medium",
                             "detail": "Amount %.2f is at or above the review threshold %.2f "
                                       "and carries no approval." % (amount, THRESHOLDS["review"])})

        key = (str(t.get("date")), str(t.get("counterparty", "")).strip().lower(),
               round(amount, 2))
        peers = [x for x in seen.get(key, []) if x != tid]
        if peers:
            findings.append({"id": tid, "rule": "possible_duplicate", "severity": "high",
                             "detail": "Same date, counterparty and amount as %s."
                                       % ", ".join(sorted(peers))})

        if amount >= THRESHOLDS["round_amount_min"] and amount == int(amount):
            findings.append({"id": tid, "rule": "round_amount", "severity": "low",
                             "detail": "Round amount %.2f — verify against the source document."
                                       % amount})

        if _is_weekend(t.get("date")):
            findings.append({"id": tid, "rule": "weekend_posting", "severity": "low",
                             "detail": "Posted on a weekend (%s); confirm authorisation path."
                                       % t.get("date")})

    findings.sort(key=lambda f: (SEVERITY_ORDER.get(f["severity"], 9), f["id"], f["rule"]))
    return findings


def render(transactions: list, findings: list) -> str:
    lines = ["### Control findings", ""]
    if not findings:
        lines.append("No findings under the current rule set and thresholds.")
    else:
        lines += ["| Transaction | Rule | Severity | Detail |", "|---|---|---|---|"]
        for f in findings:
            lines.append("| %s | %s | %s | %s |"
                         % (f["id"], f["rule"], f["severity"], f["detail"]))

    by_rule: dict = {}
    by_sev: dict = {}
    for f in findings:
        by_rule[f["rule"]] = by_rule.get(f["rule"], 0) + 1
        by_sev[f["severity"]] = by_sev.get(f["severity"], 0) + 1

    lines += ["", "### Summary", "",
              "- Transactions reviewed: %d" % len(transactions),
              "- Findings: %d" % len(findings),
              "- By severity: " + (", ".join("%s=%d" % kv for kv in sorted(by_sev.items(),
                                                                          key=lambda kv: SEVERITY_ORDER.get(kv[0], 9)))
                                   or "—"),
              "- By rule: " + (", ".join("%s=%d" % kv for kv in sorted(by_rule.items())) or "—")]

    clean = [str(t.get("id", "?")) for t in transactions
             if not any(f["id"] == str(t.get("id", "?")) for f in findings)]
    if clean:
        lines += ["", "### Cleared", "No findings: " + ", ".join(sorted(clean))]

    lines += ["", "_Deterministic rule set, not an audit opinion. Thresholds are illustrative "
              "and must be set to your own control framework before use._"]
    return "\n".join(lines)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        description="Run a deterministic internal-control rule set over a transaction ledger "
                    "(non-medical example module on the lgd-skeleton/1.0 contract)")
    ap.add_argument("--demo", action="store_true", help="run the built-in sample ledger")
    ap.add_argument("--transactions", metavar="FILE", help="JSON file with a list of transaction objects")
    ap.add_argument("--json", action="store_true", help="emit JSON instead of Markdown")
    args = ap.parse_args(argv)

    if args.transactions:
        try:
            with open(args.transactions, encoding="utf-8") as fh:
                data = json.load(fh)
        except FileNotFoundError:
            print("[error] transaction file not found: %s" % args.transactions, file=sys.stderr)
            return 2
        except json.JSONDecodeError as exc:
            print("[error] transaction file is not valid JSON: %s" % exc, file=sys.stderr)
            return 2
        if not isinstance(data, list):
            print("[error] transaction file must contain a JSON list", file=sys.stderr)
            return 2
        transactions = data
    elif args.demo:
        transactions = DEMO_TRANSACTIONS
    else:
        ap.print_help()
        return 1

    findings = review(transactions)
    if args.json:
        print(json.dumps({"thresholds": THRESHOLDS, "findings": findings},
                         ensure_ascii=False, indent=2))
    else:
        print(render(transactions, findings))
    return 0


if __name__ == "__main__":
    sys.exit(main())
