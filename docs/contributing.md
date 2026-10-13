# Contributing

Four ways in, in ascending order of effort. The first one is the most valuable.

## 1. Report an error

Regulations change, so a value that was right a year ago may be wrong today. Use the [Report a factual error](https://github.com/stevenzhao07/medical-ai-toolkit/issues/new/choose) template and include the primary source that contradicts what the module says. If you cannot cite one, say so — the item gets marked `TO_BE_VERIFIED` rather than left wrong. See [verification-policy.md](./verification-policy.md).

## 2. Try it and report what broke

Run a module against your own device, ledger or dataset and describe where it stopped being useful. "It assumed X, my case is Y" is a complete and useful report.

## 3. Contribute a fix or a module

Workflow:

```bash
git clone https://github.com/stevenzhao07/<repository>.git
cd <repository>
git checkout -b <prefix>/<short-description>
```

Branch prefixes in use: `agent/`, `codex/`, `claude/`, `copilot/`, `cursor/`, `human/` (pick the one that describes who wrote the change). AI-assisted contributions are welcome and are held to exactly the same standard as any other — the prefix is a provenance marker, not a lesser category.

Before pushing:

```bash
python harness.py --module <module-id>       # 6-dimension gate, including gold regression
python run_all.py --gold                     # or the full local sweep
```

A change to a rule, a value or an output string will usually require a matching entry in `gold_set.json`. If the gold gate fails, that is the reason; do not disable the check.

Commit messages: a one-line summary in the imperative mood, then a short paragraph on what changed and why. If the change touches a regulatory value, name the source in the message.

### What will not be accepted

- Third-party dependencies added to a module without a specific reason stated in the PR.
- A module whose `--demo` requires the network or a credential.
- A numeric value or deadline without a stated source.
- Marketing language, self-assessment of quality, or competitive claims. See the design notes: no badge walls, no emoji headings, no "better than X" without a measurement.

## 4. Claim a module as maintainer

Standards change continuously, so keeping one module current — tracking the standard, updating values, answering corrections — is ongoing work. It is better done by someone who uses that module than by someone who once wrote it.

Use the [Claim a module](https://github.com/stevenzhao07/medical-ai-toolkit/issues/new/choose) template. Say which module, and name the first thing you would change: a concrete first change is more convincing than a general offer. Arrangements range from co-maintainer to sole maintainer of that repository.

## Other industries

LGD's core is domain-neutral; the medical matrix is the worked example. Two non-medical modules already exist under [`examples/domains/`](../examples/domains) — legal compliance and finance controls — built on the identical contract with no medical code. A third domain is a welcome contribution, and the same offer to maintain what you build applies.

---

## 中文

四种方式，门槛由低到高。**第一种价值最高。**

**1 · 报错**：法规在变，去年正确的值今年可能已错。请用 [Report a factual error](https://github.com/stevenzhao07/medical-ai-toolkit/issues/new/choose) 模板并附一手来源；找不到来源也请直说 —— 该项会标 `TO_BE_VERIFIED`，而不是留着错值。详见 [verification-policy.md](./verification-policy.md)。

**2 · 试用并反馈**：用你自己的器械、台账或数据集跑一个模块，说明它在哪里开始不好用。"它假设了 X，而我这里是 Y"就是一个完整且有价值的报告。

**3 · 贡献修复或模块**：分支前缀用 `agent/`、`codex/`、`claude/`、`copilot/`、`cursor/`、`human/`（选能描述"谁写的"的那个）。**AI 参与的贡献同样欢迎，且与人工贡献同一标准** —— 前缀是溯源标记，不是降格类别。推送前跑 `python harness.py --module <id>`（含 gold 回归）；改动规则、数值或输出字符串，通常需要同步 `gold_set.json` 里的条目 —— 如果 gold 门禁失败，原因就在这里，**不要去关掉检查**。

**不接受的内容**：无明确理由的第三方依赖；`--demo` 需要联网或凭据的模块；**没有来源的数值或时限**；营销语言、自评质量、竞争性宣称（不堆 badge、不用 emoji 标题、没有测量数据就不说"比 X 好"）。

**4 · 认领模块当维护者**：标准持续在变，让一个模块保持最新（跟踪标准、更新数值、回应纠错）是持续工作，交给**每天用它的人**比交给"当初写过它的人"更合适。请用 [Claim a module](https://github.com/stevenzhao07/medical-ai-toolkit/issues/new/choose) 模板，说明认领哪个，并**点出你要改的第一件事** —— 一个具体的首改动，比泛泛的表态有说服力得多。合作方式从"共同维护"到"该仓独任维护者"都可以。

**其他行业**：LGD 内核与行业无关，医疗矩阵只是已做出来的样例。`examples/domains/` 下已有两个非医疗模块（法律合规、财务内控），用的是完全相同的契约、不含任何医疗代码。第三个领域同样欢迎，并且同样欢迎你长期维护自己建的东西。
