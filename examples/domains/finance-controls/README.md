# finance-controls-example

A second **non-medical** module on the same `lgd-skeleton/1.0` contract as the 21 medical repositories. Together with [`../legal-compliance`](../legal-compliance), it demonstrates that one contract carries unrelated domains with no change to the core.

## What it does

Runs a small, deterministic rule set over a transaction ledger and reports control findings:

| Rule | Severity | Trigger |
|---|---|---|
| `missing_approval` | high | No approver recorded |
| `dual_approval_required` | high | Amount ≥ threshold with fewer than two approvers |
| `review_required` | medium | Amount ≥ review threshold with no approval |
| `possible_duplicate` | high | Same date + counterparty + amount as another posting |
| `round_amount` | low | Round amount at or above the floor — verify against source |
| `weekend_posting` | low | Posted on a Saturday or Sunday |

Every finding names the rule that produced it. Nothing is ranked by a model — a finding either matches a stated rule or it does not.

## Run it

```bash
python scripts/control_review.py --demo                          # built-in sample ledger
python scripts/control_review.py --demo --json                   # machine-readable output
python scripts/control_review.py --transactions my_ledger.json   # your own ledger
```

Zero third-party dependencies. Python 3.8+.

Input format (`my_ledger.json`) — a JSON list:

```json
[
  {
    "id": "T-1001",
    "date": "2026-10-01",
    "amount": 12500.00,
    "account": "AP-2100",
    "counterparty": "Northwind",
    "approvers": ["L. Chen", "M. Ortiz"]
  }
]
```

`approvers` may be omitted in favour of a single `approver` string.

## Thresholds

`THRESHOLDS` in the script holds `dual_approval`, `review` and `round_amount_min`. They are illustrative — set them to your own control framework before use.

## Scope

Deterministic rule set, **not an audit opinion**. Findings identify postings that deserve a look under the stated thresholds; whether a posting is actually wrong depends on the underlying documents and your control framework.

---

## 中文

这是第二个**非医疗**模块，与矩阵中 21 个医疗仓库使用**同一份 `lgd-skeleton/1.0` 契约**。它与 [`../legal-compliance`](../legal-compliance) 一起证明：同一份契约可以承载互不相关的领域，内核无需任何改动。

**它做什么**：对一份交易台账跑一套**确定性规则**，输出内控发现 —— 缺少审批、超阈值未双人审批、疑似重复付款、整数金额、周末入账。每条发现都标明由哪条规则产生；没有任何模型打分 —— 命中规则就是命中，没命中就是没命中。

**运行**：

```bash
python scripts/control_review.py --demo                          # 内置样例台账
python scripts/control_review.py --demo --json                   # 机器可读输出
python scripts/control_review.py --transactions my_ledger.json   # 自己的台账
```

零第三方依赖，Python 3.8+。输入为 JSON 列表，字段见英文段；`approvers` 可省略，改用单个 `approver` 字符串。

**阈值**：脚本里的 `THRESHOLDS`（`dual_approval` / `review` / `round_amount_min`）只是示例，使用前须改成你自己的内控口径。

**边界**：这是确定性规则集，**不是审计意见**。发现指向的是"在既定阈值下值得看一眼"的凭证；是否真的有问题，取决于原始单据与你的内控框架。
