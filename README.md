# medical-ai-toolkit

> **Single navigation portal** for an open, zero-dependency toolkit covering the **full lifecycle of medical-device AI**, built on **LGD** — a declarative, industry-neutral skeleton where every capability is an independently loadable module. Medical devices are the reference domain; the skeleton itself is industry-neutral.

> Contributed by [@stevenzhao07](https://github.com/stevenzhao07) — maintained as an individual open-source project on medical-device RA & AI governance. Pure technical input, no commercial promotion.

---

## ⚠️ Read this first — verification honesty

We use a **four-tier verification convention** and never overstate maturity. Each module's README carries a status badge.

| Tier | Meaning | What it does NOT mean |
|---|---|---|
| 🟢 **CI** | GitHub Actions automated checks pass | not expert-reviewed, not clinically validated |
| 🟡 **Functional self-test** | module ships a runnable self-test | not third-party audited |
| 🔵 **Expert review** | a domain expert signed off | currently **pending** across the toolkit |
| ⚪ **Official source verification** | regulatory constant traced to a dated official source | not a guarantee the source is current |

> **These are reference implementations and decision-support tools — not medical devices, not certified submissions, not clinical advice.** Always confirm outputs against the current official text in your jurisdiction.

## Quick start

1. **Pick a domain** from the matrix below.
2. Open the linked module repo → read its README → run its self-test.
3. Contribute via Issue/PR (see [CONTRIBUTING.md](./CONTRIBUTING.md)).

Run the portal's own router demo to see the full module list:

```bash
python scripts/discover.py --demo
```

## 快速开始

1. 从下方矩阵**选择领域**。
2. 打开对应模块仓库 → 读其 README → 运行自测。
3. 通过 Issue/PR 贡献（见 [CONTRIBUTING.md](./CONTRIBUTING.md)）。

运行门户自带的路由演示，查看完整模块清单：

```bash
python scripts/discover.py --demo
```

## 🗂 Tool matrix (25 repositories, verified 2026-10-13)

> Note: an earlier version of this README stated "21 repositories". The accurate count as of 2026-10-13 is **25**. This correction is part of the current portal PR.

### AI governance & trust methodology
| Module | What it does | Verification |
|---|---|---|
| [ai-a3-laws](https://github.com/stevenzhao07/ai-a3-laws) | Runtime constraint library: A1 authority / A2 human-oversight / A3 accountability | 🟢+🟡 · 🔵⚪ pending |
| [ai-governance-checklist](https://github.com/stevenzhao07/ai-governance-checklist) | Model-card / data-card / human-oversight / fairness checklists | 🟢+🟡 · 🔵⚪ pending |
| [ai-model-passport](https://github.com/stevenzhao07/ai-model-passport) | Machine-readable AI passport JSON (sign + verify) | 🟢+🟡 · 🔵⚪ pending |
| [delivery-guard](https://github.com/stevenzhao07/delivery-guard) | 17-gate pre-release checker + dual SHA-256 provenance ledger | 🟢+🟡 · 🔵⚪ pending |

### Medical-device lifecycle (QMS / RA)
| Module | What it does | Verification |
|---|---|---|
| [design-controls-toolkit](https://github.com/stevenzhao07/design-controls-toolkit) | ISO 13485 §7.3 / 21 CFR 820.30 design-control self-check generator | 🟢+🟡 · 🔵⚪ pending |
| [device-regulatory-map](https://github.com/stevenzhao07/device-regulatory-map) | Cross-jurisdiction classification & path map (NMPA/EU MDR/FDA/PMDA) | 🟢+🟡 · ⚪ partial |
| [iec62304-software](https://github.com/stevenzhao07/iec62304-software) | Software safety class A/B/C + lifecycle checklist | 🟢+🟡 · 🔵⚪ pending |
| [iso14971-risk-file](https://github.com/stevenzhao07/iso14971-risk-file) | Risk-management file skeleton (ISO 14971:2019) | 🟢+🟡 · 🔵⚪ pending |
| [manufacturing-gmp](https://github.com/stevenzhao07/manufacturing-gmp) | GMP self-check + 2025-vs-2014 diff (NMPA #107 verified 2026-10-12) | 🟢+🟡 · ⚪ dated |
| [clinical-evaluation](https://github.com/stevenzhao07/clinical-evaluation) | CER path planner + PMCF plan generator | 🟢+🟡 · 🔵⚪ pending |
| [biocompatibility-iso10993](https://github.com/stevenzhao07/biocompatibility-iso10993) | ISO 10993-1:2018 endpoint matrix | 🟢+🟡 · 🔵⚪ pending |
| [sterilization-validation](https://github.com/stevenzhao07/sterilization-validation) | EO/F0/irradiation/cleaning/endotoxin calculators | 🟢+🟡 · 🔵⚪ pending |
| [pms-vigilance](https://github.com/stevenzhao07/pms-vigilance) | PMS/Vigilance deadline calculators (NMPA/EU MDR/FDA) | 🟢+🟡 · ⚪ partial |
| [udi-assignment](https://github.com/stevenzhao07/udi-assignment) | GS1 GTIN-14 / HIBCC / ICCBBA UDI reference | 🟢+🟡 · 🔵⚪ pending |
| [cybersecurity-medical](https://github.com/stevenzhao07/cybersecurity-medical) | IEC 81001-5-1 / FDA premarket cyber / SBOM checks | 🟢+🟡 · 🔵⚪ pending |

### AI / ML tooling
| Module | What it does | Verification |
|---|---|---|
| [ml-validation-toolkit](https://github.com/stevenzhao07/ml-validation-toolkit) | AUC / calibration / subgroup-fairness (stdlib only) | 🟢+🟡 · 🔵⚪ pending |
| [samd-ra-toolkit](https://github.com/stevenzhao07/samd-ra-toolkit) | SaMD/AIaMD RA + cross-jurisdiction diff | 🟢+🟡 · 🔵⚪ pending |

### Interop / data / labeling
| Module | What it does | Verification |
|---|---|---|
| [fhir-ortho-toolkit](https://github.com/stevenzhao07/fhir-ortho-toolkit) | HL7 FHIR R4 profiles for ortho UDI | 🟢+🟡 · 🔵⚪ pending |
| [omop-ortho-toolkit](https://github.com/stevenzhao07/omop-ortho-toolkit) | Ortho registry → OMOP CDM ETL proposal | 🟢+🟡 · 🔵⚪ pending |
| [multilingual-ifu](https://github.com/stevenzhao07/multilingual-ifu) | 13-language IFU aligned corpus | 🟢+🟡 · 🔵⚪ pending |

### Cross-domain / ecosystem
| Module | What it does | Note |
|---|---|---|
| [silent-failure-catalog](https://github.com/stevenzhao07/silent-failure-catalog) | Catalog of passing-but-empty validation, with reproductions | associated w/ @zhaoxinghua09-cell |
| [uibc-core](https://github.com/stevenzhao07/uibc-core) | Executable bounded-lifecycle autonomy protocol | Apache-2.0; upstream @zhaoxinghua09-cell |
| [awesome-healthcare-agents](https://github.com/stevenzhao07/awesome-healthcare-agents) | Curated list of healthcare AI agents | MIT; community list |

## ▶️ Running a module

Each module is a **zero-dependency Python CLI** (or reference corpus). Typical pattern:

```bash
cd <module>
python <module>.py --help
python <module>.py --selftest      # 端到端断言 + 负对照（2026-10-14 起 21/21 模块已实现）
```

The portal itself runs a 6-dimension self-test harness:

```bash
python harness.py --module medical-ai-toolkit   # 仅在门户本仓（目录名须为 medical-ai-toolkit）可跑
```

## 📦 CI status (transparency)

- `harness` workflow: the **PR branch `opt/portal-nav` re-ran green on 2026-10-13 11:03Z** (run `38387590604`, success). On `main`, the last green was 2026-10-13 02:55Z; earlier same-day runs (02:22Z, 02:28Z, 02:37Z) **failed** and were fixed before the green run. We keep this visible rather than hiding it. The PR's own earlier failing run `38384747668` (on commit `54c2fbf9`) was caused by a README usage-section heading that the harness's usability gate did not recognise; it is fixed in the current head `08b8bf2d`.
- `pages-build-deployment`: present but **GitHub Pages is not currently published** for this repo (`pages_config: None`). The earlier README implied Pages was live — that claim is being corrected here.

## 🤝 Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md), [GOOD_FIRST_ISSUES.md](./GOOD_FIRST_ISSUES.md), and the issue/PR templates under `.github/`. All changes go through a branch + PR; nothing merges to `main` without review.

To contribute: **fork** the repository, **clone** it locally, then open an issue or pull request.

## 📄 License

**This repository (`medical-ai-toolkit`) is licensed under CC BY 4.0** (see `LICENSE`). Across the account the licenses are **mixed per repository** — Apache-2.0, CC BY 4.0, CC0, and MIT — and the authoritative terms are those in each repo's own `LICENSE`. Always check the specific repository's `LICENSE`; no single account-wide license is asserted. (A unified attribution/provenance note is pending owner approval.)

## 🤖 Attribution & AI assistance

This reorganisation's specification was drafted with ChatGPT and reviewed by the account owner; execution was performed by a WorkBuddy agent on the owner's machine. AI is assistive only and does not replace domain-expert review or official-source verification. (Full provenance note pending a separate PR.)

## ✅ 支持的用途 / ❌ 不支持的用途 / 🌍 支持的辖区

> 本节为 2026-10-14 全量实跑审计后新增，用于消除「对外宣称 vs 实现」的口径歧义。

### ✅ 支持的用途
- 参考实现与能力演示（须附本节免责说明）
- 生命周期方法论导航、工程计算的**粗算**参考
- 内部评审、培训与方案讨论的辅助材料

### ❌ 不支持的用途
- **不得**作为注册申报、合规结论、临床或生产决策的依据
- 本项目自述为 *non-medical-device / non-certified submission / non-clinical advice*
- 🔵 专家评审全线 pending；独立数值验算仅覆盖计算主干（28 项，1 项不一致已登记）

### 🌍 支持的辖区
| 形式 | 取值 | 说明 |
|---|---|---|
| 已实现（代码层） | `CN` / `US` / `EU` / `JP` | 别名互通：`NMPA`=`CN`、`FDA`=`US`、`MDR`/`CE`=`EU`、`PMDA`=`JP` |
| **未实现** | `ASEAN`（东南亚）/ `LATAM`（拉美） | 21/21 模块明确拒绝 |

> ⚠️ 官网 medxpert.cn 所述「及东南亚、拉美等多市场」为**人工咨询服务的覆盖承诺**，**不代表**本开源工具已实现该辖区的计算能力。

### ✅ 验证方式
```bash
python <module>.py --selftest          # 端到端自测（含负对照）
python harness.py --module medical-ai-toolkit   # 门户自测（仅门户本仓可跑）
```
