# AGENTS.md · medical-ai-toolkit（根门户 / 总路由）

> 机器可发现入口（AI 编码代理 / Codex / Claude / Cursor）。单一事实源：本文件。

## 这是什么
本仓是 **lgd-skeleton/1.0** 的总入口（根路由）：聚合 @stevenzhao07 全部医疗 AI 可插拔模块，
让 AI 代理克隆即自动发现并调用下面所有模块。核心通用、领域可插拔、跨行业/机构/国家（见 README 的模块契约）。

## 路由（自动发现）
子模块在 `repos/` 下各自带 `module.json` + `AGENTS.md`；本门户用 `skeleton.json` 做总路由表。
AI 代理无需读全部，先读 `skeleton.json` 元数据，按 intent 命中再加载对应模块全文（懒加载）。

## 已纳管模块
- **ai-a3-laws** — `python scripts/a3_laws.py --demo`
- **ai-governance-checklist** — `python scripts/gov_checklist.py --demo`
- **ai-model-passport** — `python scripts/ai_passport.py --demo`
- **biocompatibility-iso10993** — `python scripts/biocompat.py --demo`
- **clinical-evaluation** — `python scripts/cer_planner.py --demo`
- **cybersecurity-medical** — `python scripts/cyber_check.py --demo`
- **delivery-guard** — `python scripts/delivery_guard.py --demo`
- **design-controls-toolkit** — `python scripts/design_controls.py --demo`
- **device-regulatory-map** — `python scripts/device_reg_map.py --demo`
- **fhir-ortho-toolkit** — `python scripts/fhir_ortho.py --demo`
- **iec62304-software** — `python scripts/sw_lifecycle.py --demo`
- **iso14971-risk-file** — `python scripts/risk_file.py --demo`
- **manufacturing-gmp** — `python scripts/gmp_toolkit.py --demo`
- **medical-ai-toolkit** — `python scripts/discover.py --demo`
- **ml-validation-toolkit** — `python scripts/ml_validation.py --demo`
- **multilingual-ifu** — `python scripts/ifu_index.py --demo`
- **omop-ortho-toolkit** — `python scripts/omop_ortho.py --demo`
- **pms-vigilance** — `python scripts/pms_report.py --demo`
- **samd-ra-toolkit** — `python scripts/samd_map.py --demo`
- **sterilization-validation** — `python scripts/sterilization_val.py --demo`
- **udi-assignment** — `python scripts/udi_assign.py --demo`

## 怎么加一个模块（一切即插件）
```bash
python idea_scaffold.py "<想法>"   # 命中复用 / 否则建骨架 + 跑 harness 自检
```
生成的模块天然被本门户路由发现。

## 自检
```bash
python run_all.py --gold     # 一键冒烟 + 6 维质量门禁（含 gold 语义回归）
python harness.py --all           # 6 维度质量门禁
```

## 红线
纯技术贡献，不含商业营销；MedXpert 仅作贡献者署名（@stevenzhao07）；不挂机构自推；发布前需仓库所有者「go」。

## 关联
- 完整《AI 参与指南》：./AI_PARTICIPATION.md
