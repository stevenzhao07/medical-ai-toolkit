# medical-ai-toolkit

> **Contributed by [@stevenzhao07](https://github.com/stevenzhao07) · Affiliation: MedXpert (medical-device RA & regulatory consultancy) · Pure technical input, no commercial promotion.**

**一句话**：这是入口。跑 `python scripts/discover.py --demo` 会打印全矩阵路由表（当前 **20** 个子模块，矩阵共 **21** 仓）。

MedXpert 把「医疗 AI 从合规到临床落地」的全套能力，以 **`lgd-skeleton/1.0` 可插拔模块**沉淀在 `@stevenzhao07`，并与骨科 RA 专长叠成 **骨科 + 医疗 AI** 双引擎。本仓是 **总入口与方法论门户**：自动路由发现 20 个子模块，横跨 **AI 治理层（9 仓）** 与 **器械本体全生命周期（11 仓）**。

---

## 可插拔骨架（lgd-skeleton/1.0）

本仓是 `lgd-skeleton/1.0` 总入口（`skeleton.json` 中 `loads_as_module: true`）：

- **一切即插件**：每个子模块仅依赖声明式 `module.json`，零配置；
- **按需装（lazy）**：仅 triggers 命中时加载；
- **可嵌套（nested）**：子模块可被本总入口路由发现；
- **机器可发现**：`AGENTS.md` · `CLAUDE.md` · `llms.txt` · `discover.py`。

运行路由发现：

```bash
python scripts/discover.py --demo          # 打印全矩阵路由表（20 个子模块）
```

## 免责声明

本工具仅提供结构化模板与计算能力，**不构成法规建议、临床建议或产品合规结论**。具体产品的注册、临床评价、灭菌验证、风险分析、软件分级等决策，须由合资格人员依据目标辖区（NMPA / FDA / EU MDR / PMDA）最新法规文本作出；条款与限值以官方发布文本为准。使用本工具产生的一切后果由使用者自行承担。

## 使用

```bash
# 路由发现（自动列出 20 个子模块）
python scripts/discover.py --demo

# 查看机器可发现清单（Windows 可用 type / Get-Content 代替 cat）
python scripts/discover.py --json
cat skeleton.json
cat llms.txt
```

## 快速开始（30 秒）

```bash
git clone https://github.com/stevenzhao07/medical-ai-toolkit.git && cd medical-ai-toolkit
python scripts/discover.py --demo
```

> 想参与或遇到问题？[提 Issue](https://github.com/stevenzhao07/medical-ai-toolkit/issues) · 完整《AI 参与指南》见 [AI_PARTICIPATION.md](./AI_PARTICIPATION.md)。

## 矩阵一：AI 治理层（9 仓）× 五层全栈

| 层 | 模块仓库 | 定位 | 覆盖度 |
|---|---|---|---|
| **L1 法规质量体系** | [samd-ra-toolkit](https://github.com/stevenzhao07/samd-ra-toolkit) | ✅✅ 核心 | ✅ 中文/骨科视角稀缺 |
| **L2 AI 治理可信** | [ai-governance-checklist](https://github.com/stevenzhao07/ai-governance-checklist) · [ai-a3-laws](https://github.com/stevenzhao07/ai-a3-laws) · [ai-model-passport](https://github.com/stevenzhao07/ai-model-passport) | ✅ 已实现 | ✅ 医疗垂直稀缺 |
| **L3 数据互操作** | [fhir-ortho-toolkit](https://github.com/stevenzhao07/fhir-ortho-toolkit) · [omop-ortho-toolkit](https://github.com/stevenzhao07/omop-ortho-toolkit) | ✅ RA/数据 | ✅✅ 骨科特定极稀缺 |
| **L4 工程验证** | [ml-validation-toolkit](https://github.com/stevenzhao07/ml-validation-toolkit) · [delivery-guard](https://github.com/stevenzhao07/delivery-guard) | ⚠️ 工程支撑 | ⚠️ |
| **L5 多语种本地化** | [multilingual-ifu](https://github.com/stevenzhao07/multilingual-ifu) | ✅✅ 多语种 | ✅✅✅ 稀缺 |

## 矩阵二：器械本体全生命周期（11 仓）

从设计控制到上市后警戒，覆盖 ISO 13485 / ISO 14971 / IEC 62304 / ISO 10993 / ISO 11135·11137·17665 / ISO 81001-5-1 主线：

| 阶段 | 模块仓库 | 主线标准/法规 |
|---|---|---|
| 设计控制 | [design-controls-toolkit](https://github.com/stevenzhao07/design-controls-toolkit) | ISO 13485 §7.3 / QMSR |
| 风险管理 | [iso14971-risk-file](https://github.com/stevenzhao07/iso14971-risk-file) | ISO 14971 / TR 24971 |
| 软件生命周期 | [iec62304-software](https://github.com/stevenzhao07/iec62304-software) | IEC 62304 |
| 注册/分类映射 | [device-regulatory-map](https://github.com/stevenzhao07/device-regulatory-map) | NMPA / EU MDR / FDA / PMDA |
| 临床评价 | [clinical-evaluation](https://github.com/stevenzhao07/clinical-evaluation) | MDR Art.61 / MDCG / CER+PMCF |
| 生物相容性 | [biocompatibility-iso10993](https://github.com/stevenzhao07/biocompatibility-iso10993) | ISO 10993-1 终点矩阵 |
| 灭菌与清洁 | [sterilization-validation](https://github.com/stevenzhao07/sterilization-validation) | ISO 11135 / 11137 / 17665 |
| 生产质量 | [manufacturing-gmp](https://github.com/stevenzhao07/manufacturing-gmp) | 2025 版 GMP / IQ·OQ·PQ |
| UDI 赋码 | [udi-assignment](https://github.com/stevenzhao07/udi-assignment) | GS1 / 21 CFR 830 / EUDAMED |
| 上市后警戒 | [pms-vigilance](https://github.com/stevenzhao07/pms-vigilance) | 令第1号 / 令第29号 / MDR Art.87 |
| 网络安全 | [cybersecurity-medical](https://github.com/stevenzhao07/cybersecurity-medical) | IEC 81001-5-1 / SBOM / STRIDE |

## 方法论来源（四支柱）

医疗 AI 信任的落地实践源自「治理守护者 XCGS / 立法者 A³ Laws / 护照官 AI 护照 / 人机共存」四支柱方法论（个人专家线，弱品牌；开源仓仅作工程化参考实现，不自称标准）。

## 路由表（全部 21 仓）

| 仓库 | 入口 | 许可 | 上游投稿 |
|---|---|---|---|
| samd-ra-toolkit | scripts/samd_map.py | CC-BY-4.0 | OpenRegulatory |
| ai-governance-checklist | scripts/gov_checklist.py | CC-BY-4.0 | OWASP/aiverify |
| ai-a3-laws | scripts/a3_laws.py | CC0 | OWASP AI Exchange |
| ai-model-passport | scripts/ai_passport.py | CC0 | —（作品集） |
| fhir-ortho-toolkit | scripts/fhir_ortho.py | CC0 | HL7 |
| omop-ortho-toolkit | scripts/omop_ortho.py | Apache-2.0 | OHDSI |
| ml-validation-toolkit | scripts/ml_validation.py | Apache-2.0 | —（作品集） |
| delivery-guard | scripts/delivery_guard.py | Apache-2.0 | —（作品集） |
| multilingual-ifu | scripts/ifu_index.py | CC-BY-4.0 | OpenRegulatory |
| design-controls-toolkit | scripts/design_controls.py | Apache-2.0 | OpenRegulatory |
| iso14971-risk-file | scripts/risk_file.py | Apache-2.0 | OpenRegulatory |
| iec62304-software | scripts/sw_lifecycle.py | CC-BY-4.0 | —（作品集） |
| device-regulatory-map | scripts/device_reg_map.py | CC-BY-4.0 | OpenRegulatory |
| clinical-evaluation | scripts/cer_planner.py | CC-BY-4.0 | OpenRegulatory |
| biocompatibility-iso10993 | scripts/biocompat.py | CC-BY-4.0 | —（作品集） |
| sterilization-validation | scripts/sterilization_val.py | Apache-2.0 | —（作品集） |
| manufacturing-gmp | scripts/gmp_toolkit.py | CC-BY-4.0 | —（作品集） |
| udi-assignment | scripts/udi_assign.py | CC0 | GS1/HIBCC/ICCBBA |
| pms-vigilance | scripts/pms_report.py | Apache-2.0 | —（作品集） |
| cybersecurity-medical | scripts/cyber_check.py | Apache-2.0 | —（作品集） |
| **medical-ai-toolkit**（本仓） | scripts/discover.py | CC-BY-4.0 | — |

## 许可

CC BY 4.0 — 见 [LICENSE](./LICENSE)。各子模块许可见其仓库（混合：CC0 / CC-BY-4.0 / Apache-2.0）。

## 关联（方法论来源）

- 理念溯源：个人专家关于医疗 AI 信任与治理的公开方法论（个人观点，不构成标准）
- 同账号系列：见上表 21 仓
