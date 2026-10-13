# The `lgd-skeleton/1.0` module contract

A module is a directory with a `module.json` and an entry script. That is the whole contract. Nothing registers itself anywhere, and the core contains no list of modules.

## `module.json` fields

| Field | Required | Meaning |
|---|---|---|
| `id` | yes | Repository/module identifier. Also the key used in the routing table |
| `title` | yes | Human-readable name |
| `description` | yes | One paragraph. Doubles as the repository description and the TeamAI skill description |
| `triggers` | yes | `keywords` / `intents` / `file_patterns`. How a router decides this module is relevant. `keywords` or `intents` must be non-empty |
| `provides` | yes | Capability names this module offers. Used for discovery and for de-duplication |
| `entry` | yes | Path to the CLI, e.g. `scripts/control_review.py` |
| `deps` | yes | Third-party dependencies. `[]` means standard library only — the norm here |
| `license` | yes | SPDX identifier |
| `upstream` | no | An upstream project this work is intended for, or `null` when there is none |
| `cost`, `lazy`, `nested` | no | Loading hints. `lazy` means load only when triggers match |
| `generated_by` | no | Provenance of the scaffold |
| `extension_note` | no | How to extend this module without reading all of it |

## The entry script

Three requirements, all mechanical:

1. `--demo` runs a self-contained sample and exits `0`.
2. `--help` works and exits `0`.
3. Bad input exits `2` with a message on stderr. Never a bare traceback.

Zero third-party dependencies is not a style preference. A compliance artefact has to be auditable offline, and reproducible years after the environment that produced it is gone. `harness.py` enforces this: it parses the entry script's imports with `ast` and fails the module if it imports a third-party package while declaring `deps: []`.

## How the core uses a module

| Core piece | Use of the contract |
|---|---|
| `router.py` | Reads `triggers` only, matches against an intent, and loads the module's full text **only on a match** — roughly 20 tokens per module at rest |
| `harness.py` | Six dimensions: fit (schema + `deps` vs actual imports), accuracy (`--demo` output contains the module's key fields), fluency (`--help`), outsider run (every runnable command in the README), usability, and gold regression against `gold_set.json` |
| `manifest.py` | Aggregates every module into `skeleton.json`, `llms.txt`, `AGENTS.md`, the A2A card and the TeamAI layout |
| `scaffold.py` | Generates a new module from the same contract |

## Adding a domain

1. Copy [`examples/domains/legal-compliance`](../examples/domains/legal-compliance) to `examples/domains/<your-domain>/`.
2. Rewrite `module.json` — `id`, `title`, `description`, `triggers`, `provides`, `entry`, `extension_note`.
3. Rewrite the script, keeping the CLI shape and the zero-dependency rule.
4. Run `python harness.py --module <your-module-id>`.

None of these steps touches the core. That is the design: the reusable parts are the ordering, the gates and the audit trail — not the domain content.

## What is not a module

- A script without `module.json` — nothing can route to it.
- A module that shells out to a service — it stops being offline-auditable.
- A module whose `--demo` needs the network or a credentialed environment.
- A module that only works inside one organisation's private data — that belongs in that organisation's `plugins/`, not here.

---

## 中文

一个模块 = 一个目录 + `module.json` + 一个入口脚本。契约就这么多。没有任何注册表，内核里也不保存模块清单。

**`module.json` 字段**（必填/含义见上表）：`id`、`title`、`description`、`triggers`（`keywords`/`intents`/`file_patterns`，其中 keywords 或 intents 必须非空）、`provides`、`entry`、`deps`、`license` 为必填；`upstream`（无既定目标时写 `null`）、`cost`/`lazy`/`nested`、`generated_by`、`extension_note` 可选。

**入口脚本三条机械要求**：① `--demo` 跑内置样例并退 `0`；② `--help` 可用并退 `0`；③ 输入错误退 `2` 并在 stderr 给出信息，**绝不允许裸 traceback**。

**零第三方依赖不是风格偏好**：合规产物必须能离线审计，并在产出它的环境消失多年后仍可复现。`harness.py` 会强制检查这一点 —— 它用 `ast` 解析入口脚本的 import，若声明 `deps: []` 却引用了第三方包，直接判不合格。

**内核如何使用契约**：`router.py` 只读 `triggers`，命中才载入模块全文（每个模块常驻约 20 token）；`harness.py` 跑 6 个维度（适配/准确/流畅/外人实跑/易用/gold 回归）；`manifest.py` 把全部模块聚合成 `skeleton.json`、`llms.txt`、`AGENTS.md`、A2A 卡与 TeamAI 布局；`scaffold.py` 按同一契约生成新模块。

**加一个领域**：复制 `examples/domains/legal-compliance` → 改写 `module.json` → 改写脚本（保持 CLI 形状与零依赖）→ 跑 `python harness.py --module <id>`。这些步骤**都不触碰内核**。可复用的正是顺序、门禁与审计轨迹，不是领域内容。

**什么不算模块**：没有 `module.json` 的脚本（无法被路由）；依赖外部服务的模块（不再可离线审计）；`--demo` 需要联网或凭据环境的模块；只对某一个内部数据集有效的模块（那属于该组织的私有 `plugins/`）。
