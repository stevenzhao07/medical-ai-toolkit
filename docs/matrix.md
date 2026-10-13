# The matrix — 21 repositories

Each repository is an independent module. There is no monorepo, no shared build, and no dependency between them: a module can be cloned, run and audited on its own. What they share is the [`lgd-skeleton/1.0` contract](./lgd-contract.md) and this routing table.

## Layer 1 — AI governance (9)

| Repository | What it does | Entry | Licence | Intended upstream |
|---|---|---|---|---|
| `samd-ra-toolkit` | SaMD/AIaMD registration and quality-system mapping | `scripts/samd_map.py` | CC-BY-4.0 | OpenRegulatory/templates |
| `ai-governance-checklist` | Governance self-check; model card and data card templates | `scripts/gov_checklist.py` | CC-BY-4.0 | OWASP AI Exchange · AI Verify |
| `ai-a3-laws` | Runtime constraints on autonomous decisions: authority, autonomy, accountability | `scripts/a3_laws.py` | CC0 | OWASP AI Exchange |
| `ai-model-passport` | Model identity, provenance and verification with a signed fingerprint | `scripts/ai_passport.py` | CC0 | — |
| `fhir-ortho-toolkit` | UDI profiles and resource builders for HL7 FHIR R4 | `scripts/fhir_ortho.py` | CC0 | HL7 community |
| `omop-ortho-toolkit` | Concept sets and ETL shape toward OMOP CDM v5.4 | `scripts/omop_ortho.py` | Apache-2.0 | OHDSI CDM WG |
| `ml-validation-toolkit` | Performance, calibration and subgroup fairness without scikit-learn | `scripts/ml_validation.py` | Apache-2.0 | — |
| `delivery-guard` | 17 pre-delivery gates plus a dual SHA-256 provenance ledger | `scripts/delivery_guard.py` | Apache-2.0 | — |
| `multilingual-ifu` | An IFU template in 14 language versions with a structural completeness check | `scripts/ifu_index.py` | CC-BY-4.0 | OpenRegulatory/templates |

## Layer 2 — device lifecycle (11)

| Repository | Stage | Entry | Licence | Main standard |
|---|---|---|---|---|
| `design-controls-toolkit` | Design controls | `scripts/design_controls.py` | Apache-2.0 | ISO 13485 §7.3 · 21 CFR 820.30 · IEC 62366-1 |
| `iso14971-risk-file` | Risk management | `scripts/risk_file.py` | Apache-2.0 | ISO 14971 · TR 24971 |
| `iec62304-software` | Software lifecycle | `scripts/sw_lifecycle.py` | CC-BY-4.0 | IEC 62304 |
| `device-regulatory-map` | Classification and route mapping | `scripts/device_reg_map.py` | CC-BY-4.0 | NMPA · EU MDR · FDA · PMDA |
| `clinical-evaluation` | Clinical evaluation | `scripts/cer_planner.py` | CC-BY-4.0 | MDR Art.61 · MDCG · CER + PMCF |
| `biocompatibility-iso10993` | Biocompatibility | `scripts/biocompat.py` | CC-BY-4.0 | ISO 10993-1 |
| `sterilization-validation` | Sterilisation and cleaning | `scripts/sterilization_val.py` | Apache-2.0 | ISO 11135 · 11137 · 17665 |
| `manufacturing-gmp` | Production quality | `scripts/gmp_toolkit.py` | CC-BY-4.0 | GMP 2025 revision · IQ/OQ/PQ |
| `udi-assignment` | UDI assignment | `scripts/udi_assign.py` | CC0 | GS1 · HIBCC · ICCBBA · 21 CFR 830 |
| `pms-vigilance` | Post-market surveillance | `scripts/pms_report.py` | Apache-2.0 | NMPA Order No.1 & No.29 · MDR Art.87 |
| `cybersecurity-medical` | Cybersecurity | `scripts/cyber_check.py` | Apache-2.0 | IEC 81001-5-1 · SBOM · STRIDE |

## Portal (1)

| Repository | What it does | Entry | Licence |
|---|---|---|---|
| `medical-ai-toolkit` | Routing table, machine-discoverable manifests, self-test harness, documentation | `scripts/discover.py` | CC-BY-4.0 |

## Trying any module

Every module follows the same three commands:

```bash
git clone https://github.com/stevenzhao07/<repository>.git
cd <repository>
python <entry> --demo
```

`--help` lists the real options; `--json` (where supported) emits machine-readable output.

## Where the chain joins

The 11 lifecycle modules are ordered: **design controls → risk management → software lifecycle → classification → clinical evaluation → biocompatibility → sterilisation → production → UDI → post-market surveillance → cybersecurity.** Each stage's output is the next stage's input in practice, but the modules do not call each other — they share a contract, not a call graph. That keeps each one auditable in isolation, which matters more here than convenience.

---

## 中文

每个仓库都是一个独立模块。没有 monorepo、没有共享构建、彼此没有依赖：单个模块可以被单独克隆、运行与审计。它们共享的是 [`lgd-skeleton/1.0` 契约](./lgd-contract.md)与这张路由表。

（各仓「做什么 / 入口 / 许可 / 主线标准」见上方英文两张表；字段一一对应。）

**第一层 —— AI 治理（9）**：`samd-ra-toolkit`（SaMD 注册与质量体系映射）、`ai-governance-checklist`（治理自检 + 模型卡/数据卡模板）、`ai-a3-laws`（权限–自主–追责运行时约束）、`ai-model-passport`（模型身份、溯源与指纹验证）、`fhir-ortho-toolkit`（FHIR R4 UDI 轮廓与资源构造器）、`omop-ortho-toolkit`（OMOP CDM v5.4 概念集与 ETL 形状）、`ml-validation-toolkit`（性能/校准/亚组公平性，不依赖 scikit-learn）、`delivery-guard`（17 道交付门禁 + 双 SHA-256 权属台账）、`multilingual-ifu`（IFU 14 个语言版本 + 结构完整性校验）。

**第二层 —— 器械生命周期（11）**：`design-controls-toolkit`（设计控制）、`iso14971-risk-file`（风险管理）、`iec62304-software`（软件生命周期）、`device-regulatory-map`（分类与路径映射）、`clinical-evaluation`（临床评价）、`biocompatibility-iso10993`（生物相容性）、`sterilization-validation`（灭菌与清洁）、`manufacturing-gmp`（生产质量）、`udi-assignment`（UDI 赋码）、`pms-vigilance`（上市后警戒）、`cybersecurity-medical`（网络安全）。

**门户（1）**：`medical-ai-toolkit` —— 路由表、机器可发现清单、自检框架、文档。

**试任一模块**（三条命令，全矩阵一致）：

```bash
git clone https://github.com/stevenzhao07/<仓库名>.git
cd <仓库名>
python <入口> --demo
```

`--help` 列出真实选项；支持 `--json` 的模块可输出机器可读格式。

**链条如何衔接**：11 个生命周期模块是有序的 —— **设计控制 → 风险管理 → 软件生命周期 → 分类 → 临床评价 → 生物相容性 → 灭菌 → 生产 → UDI → 上市后警戒 → 网络安全**。实践中上一阶段的产出是下一阶段的输入，但模块之间**不互相调用** —— 它们共享的是契约，不是调用图。这让每个模块都能被独立审计，在此场景下比省事更重要。
