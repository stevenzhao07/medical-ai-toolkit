# legal-compliance-example

A minimal, **non-medical** module built on the same `lgd-skeleton/1.0` contract as the 21 medical repositories in this matrix.

Its only job is to make one claim testable: **the skeleton is industry-neutral.** Compare this module's `module.json` with any medical module's — the contract is identical (`id`, `triggers`, `provides`, `entry`, `deps`); only the domain content differs. That is what "add your own `domains/` module without touching the core" means in practice.

## What it does

Turns a set of contract clauses into an **obligation ledger**: what must be done, by which party, triggered by what, against which deadline, and who inside the organisation owns it. Deadlines that cannot be parsed are reported as `unspecified` rather than assumed benign — an obligation with no deadline is the most common reason one gets missed.

## Run it

```bash
python scripts/legal_obligations.py --demo                      # built-in sample clauses
python scripts/legal_obligations.py --demo --json               # machine-readable output
python scripts/legal_obligations.py --clauses my_clauses.json   # your own clauses
```

Zero third-party dependencies. Python 3.8+.

Input format (`my_clauses.json`) — a JSON list:

```json
[
  {
    "clause": "7.2",
    "obligation": "Notify the customer of any security incident",
    "party": "vendor",
    "trigger": "incident discovered",
    "deadline": "72h",
    "owner": "Security Lead"
  }
]
```

`deadline` accepts `72h`, `15d`, `annually`, or an empty string when the trigger is event-driven with no fixed period.

## Build your own domain module

1. Copy this directory to `examples/domains/<your-domain>/`.
2. Rewrite `module.json` — change `id`, `title`, `description`, `triggers`, `provides`, `entry`, `extension_note`.
3. Rewrite the script. Keep the same CLI shape: a `--demo` that runs the built-in sample, `--help` that works, exit code 0 on success and 2 on bad input.
4. Keep it zero-dependency. That is not a stylistic preference — a compliance artefact has to be auditable offline and reproducible years later.

Then open an issue on [medical-ai-toolkit](https://github.com/stevenzhao07/medical-ai-toolkit/issues) — domains other than medical are explicitly welcome, and if you want to maintain what you build, say so.

## Scope

This module is a structural aid, not legal advice. Clause interpretation and enforceability depend on the governing law and the full contract text.

---

## 中文

这是一个**非医疗**的最小模块，与矩阵中 21 个医疗仓库使用**同一份 `lgd-skeleton/1.0` 契约**。

它只为一件事服务：让「骨架与行业无关」这个说法**可被验证**。把本模块的 `module.json` 与任一医疗模块对比 —— 契约完全相同（`id`、`triggers`、`provides`、`entry`、`deps`），不同的只是领域内容。这就是「加自己的 `domains/` 模块、不碰内核」在实际中的样子。

**它做什么**：把一组合同条款转成**义务台账** —— 谁该做什么、由什么触发、期限多长、公司内部谁负责。无法解析的期限如实标为 `unspecified`，而不是假定它没问题 —— 没有期限的义务，正是实践中被漏掉的头号原因。

**运行**：

```bash
python scripts/legal_obligations.py --demo                      # 内置样例条款
python scripts/legal_obligations.py --demo --json               # 机器可读输出
python scripts/legal_obligations.py --clauses my_clauses.json   # 自己的条款
```

零第三方依赖，Python 3.8+。

**自己建一个领域模块**：复制本目录 → 改写 `module.json`（id/title/description/triggers/provides/entry）→ 改写脚本（保持 CLI 形状：`--demo` 跑内置样例、`--help` 可用、成功退 0、输入错误退 2）→ 保持零依赖。之后到门户仓提 Issue 说明；**医疗以外的领域同样欢迎**，若你想长期维护它，也请一并说明。

**边界**：本模块是结构性辅助，不是法律意见。条款的解释与可执行性取决于适用法律与完整合同文本。
