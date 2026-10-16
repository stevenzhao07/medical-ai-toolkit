# -*- coding: utf-8 -*-
"""
lifecycle_modules.py — 医疗器械全生命周期扩展模块清单（法规专项层）
========================================================================
背景：原矩阵 10 仓覆盖「AI 治理层 + 数据互操作层 + 交付门禁」，
但医疗器械本体的产品生命周期（设计→风险→注册→临床→生物相容→灭菌/清洁→
生产→标签/UDI→上市后）大面积缺口。本文件按全生命周期补齐 11 个模块，
使矩阵从「AI 专项」升级为「医疗产业全生命周期」工具箱。

设计原则（同 lgd-skeleton/1.0）：
- 零依赖（仅 Python 3.8+ 标准库），可离线跑；
- 事实断言全部一手核实（法规名/时限/标准号以官方文本为准）；
- 不确定处显式标 TO_BE_VERIFIED，不装懂；
- 纯技术贡献，@stevenzhao07 署名，MedXpert 仅作 affiliation。
"""

MODULES = [
    {
    "id": "udi-hospital-trace",
    "title": "院内 UDI 解析/建档/召回追溯（GS1·HIBCC·ICCBBA）",
    "layer": "L2",
    "license": "Apache-2.0",
    "entry": "udi_hospital_trace.py",
    "description": "医院端 UDI 工作流：条码解析（GS1 AIDC/HIBCC/ICCBBA/裸 GTIN-14，含 mod-10 校验位）、入院建档（A1/A2/A3 责任字段 + 患者假名化）、按器械键召回追溯（时间线输出）。零依赖纯标准库。",
    "keywords": [
        "udi",
        "gs1",
        "gtin",
        "hibcc",
        "iccbba",
        "召回追溯",
        "入院建档",
        "医院端"
    ],
    "file_patterns": [
        "udi_hospital_trace.py"
    ],
    "intents": [
        "解析UDI",
        "入院建档",
        "召回追溯"
    ],
    "provides": [
        "udi-hospital-trace",
        "udi-parse",
        "udi-intake",
        "udi-recall-trace"
    ],
    "cost": "low",
    "lazy": true,
    "nested": true,
    "deps": [],
    "idea": "院内 UDI 全流程：解析→建档→追溯",
    "features": [
        "GS1 GTIN-14 mod-10 校验",
        "HIBCC/ICCBBA 格式解析",
        "A1/A2/A3 责任记录 + 患者假名化",
        "召回追溯时间线"
    ],
    "extension_note": "新增条码格式：在 parse_udi 加分发分支。",
    "usage": "```bash\npython udi_hospital_trace.py --selftest\npython udi_hospital_trace.py --demo\npython udi_hospital_trace.py --parse '(01)00614141234561(21)123456'\n```",
    "extra": "医院端模块；与制造商端 udi-assignment 算法同源。",
    "related": [
        "udi-assignment",
        "hospital-admission-eval",
        "fhir-hospital-interop",
        "vigilance-hospital-report"
    ],
    "upstream": null
},
    {
    "id": "ortho-registry-rwe",
    "title": "骨科登记处随访排程与 RWE 结局事件（OMOP 导出）",
    "layer": "L2",
    "license": "Apache-2.0",
    "entry": "ortho_registry_rwe.py",
    "description": "骨科登记处术后随访排程（6周/3月/1年/2年/5年）、PROM 结局事件采集（有效性校验）、OMOP-CDM v5.4 精简导出。支撑真实世界证据（RWE）收集。",
    "keywords": [
        "registry",
        "rwe",
        "followup",
        "prom",
        "omop",
        "登记处",
        "随访",
        "真实世界"
    ],
    "file_patterns": [
        "ortho_registry_rwe.py"
    ],
    "intents": [
        "随访排程",
        "结局事件",
        "OMOP导出"
    ],
    "provides": [
        "ortho-registry-rwe",
        "followup-schedule",
        "prom-event",
        "omop-lite"
    ],
    "cost": "low",
    "lazy": true,
    "nested": true,
    "deps": [],
    "idea": "登记处随访 + RWE 结局闭环",
    "features": [
        "5 节点随访排程",
        "PROM 0-100 有效性校验",
        "OMOP-CDM v5.4 lite 导出"
    ],
    "extension_note": "新增随访节点：改 FOLLOWUP_POINTS。",
    "usage": "```bash\npython ortho_registry_rwe.py --selftest\npython ortho_registry_rwe.py --schedule 2026-03-10\n```",
    "extra": "与 omop-ortho-toolkit 映射层衔接。",
    "related": [
        "omop-ortho-toolkit",
        "fhir-hospital-interop",
        "hospital-llm-training"
    ],
    "upstream": null
},
    {
    "id": "vigilance-hospital-report",
    "title": "医院不良事件上报与监管时限（NMPA/EU/FDA）",
    "layer": "L2",
    "license": "Apache-2.0",
    "entry": "vigilance_hospital_report.py",
    "description": "医院向 MAH/监管上报不良事件的时限感知工具：NMPA 20 工作日、EU MDR 15 天、FDA 30 天（含工作日计算），事件录入含严重度校验与事件 ID。",
    "keywords": [
        "vigilance",
        "adverse-event",
        "不良事件",
        "上报时限",
        "nmpa",
        "mdr",
        "fda"
    ],
    "file_patterns": [
        "vigilance_hospital_report.py"
    ],
    "intents": [
        "不良事件上报",
        "监管时限"
    ],
    "provides": [
        "vigilance-hospital-report",
        "ae-deadline",
        "ae-record"
    ],
    "cost": "low",
    "lazy": true,
    "nested": true,
    "deps": [],
    "idea": "医院不良事件上报时限感知",
    "features": [
        "三辖区工作日时限",
        "严重度校验",
        "事件状态机"
    ],
    "extension_note": "新增辖区时限：改 DEADLINES。",
    "usage": "```bash\npython vigilance_hospital_report.py --selftest\npython vigilance_hospital_report.py --deadline 2026-10-05\n```",
    "extra": "与制造商端 pms-vigilance 构成双向上报链。",
    "related": [
        "pms-vigilance",
        "udi-hospital-trace",
        "fhir-hospital-interop"
    ],
    "upstream": null
},
    {
    "id": "fhir-hospital-interop",
    "title": "FHIR R4 资源生成 + ICD-10/ICPM 编码参考",
    "layer": "L2",
    "license": "Apache-2.0",
    "entry": "fhir_hospital_interop.py",
    "description": "医院信息互操作：FHIR R4 Patient/Device(UDI)/Procedure 资源生成（确定性 ID），骨科 ICD-10/ICPM 编码参考查询。",
    "keywords": [
        "fhir",
        "r4",
        "hl7",
        "icd10",
        "icpm",
        "互操作",
        "编码"
    ],
    "file_patterns": [
        "fhir_hospital_interop.py"
    ],
    "intents": [
        "FHIR资源",
        "编码查询"
    ],
    "provides": [
        "fhir-hospital-interop",
        "fhir-patient",
        "fhir-device",
        "fhir-procedure",
        "coding-lookup"
    ],
    "cost": "low",
    "lazy": true,
    "nested": true,
    "deps": [],
    "idea": "FHIR R4 资源生成 + 骨科编码参考",
    "features": [
        "Patient/Device/Procedure 资源",
        "UDI 标识",
        "ICD-10/ICPM 查询"
    ],
    "extension_note": "新增资源类型：扩展 fhir_resource 分发。",
    "usage": "```bash\npython fhir_hospital_interop.py --selftest\npython fhir_hospital_interop.py --resource Device --json '{\"udi\":\"(01)00614141234561\"}'\n```",
    "extra": "与 fhir-ortho-toolkit 同源；不替代官方 FHIR 服务器。",
    "related": [
        "fhir-ortho-toolkit",
        "udi-hospital-trace",
        "omop-ortho-toolkit"
    ],
    "upstream": null
},
    {
    "id": "equipment-asset-management",
    "title": "医院设备台账/维护校准排程/报废判断",
    "layer": "L2",
    "license": "Apache-2.0",
    "entry": "equipment_asset_management.py",
    "description": "设备科核心：设备台账登记（A1/A2/A3 决策记录）、预防性维护到期排程、校准/计量到期状态（expired/due-soon/ok）、报废判断。",
    "keywords": [
        "equipment",
        "asset",
        "pm",
        "calibration",
        "metrology",
        "设备台账",
        "校准",
        "报废"
    ],
    "file_patterns": [
        "equipment_asset_management.py"
    ],
    "intents": [
        "设备台账",
        "维护排程",
        "校准到期",
        "报废"
    ],
    "provides": [
        "equipment-asset-management",
        "pm-due",
        "cal-status",
        "retire-check"
    ],
    "cost": "low",
    "lazy": true,
    "nested": true,
    "deps": [],
    "idea": "设备科台账 + PM/校准 + 报废闭环",
    "features": [
        "PM 到期排程",
        "校准状态三态",
        "报废判断"
    ],
    "extension_note": "新增维护周期：改 pm_schedule 参数。",
    "usage": "```bash\npython equipment_asset_management.py --selftest\npython equipment_asset_management.py --pm 2026-01-15\n```",
    "extra": "与 sterilization-validation 校准逻辑同源。",
    "related": [
        "sterilization-validation",
        "supplier-audit"
    ],
    "upstream": null
},
    {
    "id": "supplier-audit",
    "title": "供应商审核清单/资质到期/分级",
    "layer": "L2",
    "license": "Apache-2.0",
    "entry": "supplier_audit.py",
    "description": "供应链质量：6 项供应商审核清单（ISO13485/营业执照/GSP/质量协议/审核报告/召回史）、资质证照到期跟踪（90 天预警窗）、审核分级 A/B/C/D。",
    "keywords": [
        "supplier",
        "audit",
        "iso13485",
        "供应链",
        "供应商审核",
        "资质到期"
    ],
    "file_patterns": [
        "supplier_audit.py"
    ],
    "intents": [
        "供应商审核",
        "资质到期"
    ],
    "provides": [
        "supplier-audit",
        "audit-grade",
        "license-expiry"
    ],
    "cost": "low",
    "lazy": true,
    "nested": true,
    "deps": [],
    "idea": "供应商审核 + 资质证照闭环",
    "features": [
        "审核清单 → A/B/C/D",
        "证照 90 天预警"
    ],
    "extension_note": "新增审核项：改 CHECKLIST。",
    "usage": "```bash\npython supplier_audit.py --selftest\npython supplier_audit.py --audit S-01 --json '{\"iso13485\":true}'\n```",
    "extra": "与 manufacturing-gmp 自查逻辑同源。",
    "related": [
        "manufacturing-gmp",
        "equipment-asset-management"
    ],
    "upstream": null
},
    {
    "id": "hospital-admission-eval",
    "title": "医院采购准入评估（证照校验+卫生经济学）",
    "layer": "L2",
    "license": "Apache-2.0",
    "entry": "hospital_admission_eval.py",
    "description": "采购决策支持：三类证照校验（注册证/生产许可/经营许可 + 效期）、卫生经济学粗算（单患者年成本 + 高成本阈值）、综合准入结论。",
    "keywords": [
        "admission",
        "procurement",
        "license",
        "卫生经济学",
        "采购准入",
        "证照校验"
    ],
    "file_patterns": [
        "hospital_admission_eval.py"
    ],
    "intents": [
        "证照校验",
        "卫生经济学",
        "准入结论"
    ],
    "provides": [
        "hospital-admission-eval",
        "license-check",
        "heco",
        "admission-verdict"
    ],
    "cost": "low",
    "lazy": true,
    "nested": true,
    "deps": [],
    "idea": "采购准入：证照 + 经济学双闸",
    "features": [
        "三证校验+效期",
        "单患者年成本",
        "准入结论"
    ],
    "extension_note": "新增证照类型：扩展 license_check。",
    "usage": "```bash\npython hospital_admission_eval.py --selftest\npython hospital_admission_eval.py --verdict --json '{\"reg_cert\":\"NMPA-2024-001\",\"prod_license\":\"P-01\",\"biz_license\":\"B-01\",\"reg_expiry\":\"2027-12-31\",\"price_cny\":50000,\"annual_volume\":20,\"expected_life_years\":5,\"reoperation_rate\":0.05}'\n```",
    "extra": "与 device-regulatory-map 辖区规则同源。",
    "related": [
        "device-regulatory-map",
        "udi-hospital-trace",
        "supplier-audit"
    ],
    "upstream": null
},
    {
    "id": "hospital-llm-training",
    "title": "医院大模型训练工具链（PII 脱敏+LoRA 编排+模型卡）",
    "layer": "L2",
    "license": "Apache-2.0",
    "entry": "hospital_llm_training.py",
    "description": "医院本地大模型训练闭环：合规数据流水线（PII 扫描：姓名/证件/电话/病历号/邮箱 → 密钥化 SHA-256 假名化 → 4/1/1 拆分）、LoRA 微调配置编排（torch 检测，无则 dry-run 不假装训练）、评估、ai-model-passport 模型卡输出。",
    "keywords": [
        "llm",
        "training",
        "lora",
        "pii",
        "pseudonymization",
        "模型卡",
        "脱敏",
        "微调",
        "医院大模型"
    ],
    "file_patterns": [
        "hospital_llm_training.py"
    ],
    "intents": [
        "数据脱敏",
        "LoRA微调",
        "模型卡"
    ],
    "provides": [
        "hospital-llm-training",
        "pii-pipeline",
        "lora-config",
        "model-card"
    ],
    "cost": "low",
    "lazy": true,
    "nested": true,
    "deps": [],
    "idea": "医院合规训练：数据→微调→评估→模型卡",
    "features": [
        "PII 五类正则扫描",
        "密钥化假名化",
        "4/1/1 拆分",
        "LoRA 编排（torch 检测 dry-run）",
        "模型卡输出"
    ],
    "extension_note": "新增 PII 模式：改 PII_PATTERNS。",
    "usage": "```bash\npython hospital_llm_training.py --selftest\npython hospital_llm_training.py --demo\npython hospital_llm_training.py --prepare --json '[{\"note\":\"患者 张伟 13812345678\"}]'\n```",
    "extra": "真训练需 torch+GPU（家用机可跑）；工具链承担工程化/合规/评估/治理四件事。",
    "related": [
        "omop-ortho-toolkit",
        "ml-validation-toolkit",
        "ai-model-passport",
        "ai-governance-checklist"
    ],
    "upstream": null
},
    # ------------------------------------------------------------------ P0 核心四件
    {
        "id": "design-controls-toolkit",
        "title": "医疗器械设计控制工具包（DHF/DMR/设计转换/人因挂点）",
        "layer": "L1",
        "license": "Apache-2.0",
        "entry": "scripts/design_controls.py",
        "description": "把 ISO 13485 §7.3 设计开发控制与 21 CFR 820.30 设计控制落成可运行的自检清单生成器：设计输入/输出、评审、验证(V&V)、确认、设计转换、变更控制、DHF/DMR 索引，含 IEC 62366-1 人因工程挂点。适用于 II/III 类器械与 SaMD 的设计阶段质量体系搭建。",
        "keywords": ["design-controls", "dhf", "dmr", "设计控制", "设计转换", "iso13485", "820.30", "human-factors"],
        "file_patterns": ["design_controls.py"],
        "intents": ["设计控制自查", "DHF 建立", "设计验证确认", "人因工程"],
        "provides": ["design-controls-toolkit", "design-controls", "dhf-checklist", "v&v-plan"],
        "cost": "low",
        "lazy": True,
        "nested": True,
        "deps": [],
        "idea": "设计控制清单生成器（ISO 13485 7.3 + 820.30 + IEC 62366 挂点）",
        "features": [
            "设计控制全流程清单：策划/输入/输出/评审/验证/确认/转换/更改（ISO 13485 §7.3.2–7.3.10）",
            "DHF/DMR 索引生成：每条设计记录对应到生命周期阶段",
            "人因挂点：IEC 62366-1 可用性工程关键活动提示（非替代标准）",
            "零依赖 + CLI：按阶段过滤输出 Markdown 清单",
        ],
        "extension_note": "新增控制项：在 DESIGN_CATALOG 加一项，清单自动扩。",
        "usage": "```bash\npython scripts/design_controls.py --demo\npython scripts/design_controls.py --stage 验证\n```",
        "extra": "定位为「设计阶段质量体系脚手架」：清单依据 ISO 13485:2016 §7.3 与 FDA 820.30 的通用要求整理，具体产品须按目标辖区法规二次裁剪。不构成法规建议。",
        "related": ["iso14971-risk-file", "iec62304-software", "device-regulatory-map"],
        "upstream": "OpenRegulatory/templates",
    },
    {
        "id": "iso14971-risk-file",
        "title": "风险管理文件生成器（ISO 14971 风险分析/评价/控制）",
        "layer": "L1",
        "license": "Apache-2.0",
        "entry": "scripts/risk_file.py",
        "description": "按 ISO 14971:2019（+ ISO/TR 24971 应用指南）生成风险管理文件骨架：危害登记表、5×5 概率×严重度风险矩阵、可接受性准则、风险控制措施跟踪、剩余风险与受益-风险分析。把「风险管理贯穿生命周期」落成一条命令。",
        "keywords": ["iso14971", "risk-management", "风险管理", "风险矩阵", "剩余风险", "benefit-risk"],
        "file_patterns": ["risk_file.py"],
        "intents": ["风险管理文件", "风险分析", "风险评价矩阵", "剩余风险"],
        "provides": ["iso14971-risk-file", "risk-matrix", "risk-report", "fmea-lite"],
        "cost": "low",
        "lazy": True,
        "nested": True,
        "deps": [],
        "idea": "ISO 14971 风险管理文件生成器（矩阵 + 控制跟踪 + 剩余风险）",
        "features": [
            "风险矩阵：概率 P1–P5 × 严重度 S1–S5，可接受性准则可配置（默认按 ISO 14971 精神）",
            "危害登记：add/list 子命令维护危害-处境-伤害三联表",
            "控制跟踪：每条风险的控制措施、实施状态、残余 P/S 复评",
            "受益-风险结论段自动汇总（不替代评审委员会判定）",
        ],
        "extension_note": "新增风险源类别：在 HAZARD_CATEGORIES 加一行。",
        "usage": "```bash\npython scripts/risk_file.py --demo\npython scripts/risk_file.py add --hazard '植入物断裂' --p 3 --s 5\n```",
        "extra": "风险准则（什么算可接受）由制造商自行定义并在文件中声明——本工具默认准则仅为示例起点。ISO/TR 24971 为应用指南，不是标准本体。",
        "related": ["design-controls-toolkit", "iec62304-software", "pms-vigilance"],
        "upstream": "OpenRegulatory/templates",
    },
    {
        "id": "sterilization-validation",
        "title": "灭菌与清洁验证计算器（EO/湿热/辐照/清洁/内毒素）",
        "layer": "L1",
        "license": "Apache-2.0",
        "entry": "scripts/sterilization_val.py",
        "description": "医疗器械灭菌与清洁验证的常用计算器：EO 灭菌 BI 存活分数与过度杀灭法判据、湿热灭菌 F0 累积、辐照灭菌 ISO 11137 Method 1 VDmax 剂量设定、清洁验证残留限值（PDE/单位面积法/10 ppm 经验法）、细菌内毒素限值（K/M 法）。覆盖骨科植入物清洁验证/内毒素检验的真实工程场景。",
        "keywords": ["sterilization", "eo", "f0", "iso11137", "iso17665", "iso11135", "cleaning-validation", "endotoxin", "灭菌验证", "清洁验证", "内毒素"],
        "file_patterns": ["sterilization_val.py"],
        "intents": ["灭菌验证计算", "F0 计算", "清洁验证限值", "内毒素限值"],
        "provides": ["sterilization-validation", "f0-calc", "cleaning-limit", "endotoxin-limit"],
        "cost": "low",
        "lazy": True,
        "nested": True,
        "deps": [],
        "idea": "灭菌/清洁验证计算器（EO/湿热/辐照 + 清洁残留 + 内毒素限值）",
        "features": [
            "EO：BI 存活分数 N=N0×10^(-t/D)，半周期过度杀灭 6 log 判据（SAL 10^-6）",
            "湿热：F0=Δt×10^((T-121.1)/z) 逐段累积，支持温度-时间序列输入",
            "辐照：ISO 11137 Method 1 VDmax=D10×log10(N0/SAL)，支持自定义生物负载",
            "清洁验证：PDE→单位面积擦拭限值 / 冲洗限值 + 10 ppm 经验法对照",
            "内毒素：K/M 法限值（K 按给药途径：静脉 5、椎管内 0.2 EU/kg/h）",
        ],
        "extension_note": "新增计算模型：在 MODELS 注册表加一个函数即可。",
        "usage": "```bash\npython scripts/sterilization_val.py --demo\npython scripts/sterilization_val.py --f0 121.5:10,118:5\npython scripts/sterilization_val.py --eo --d 2.8 --t 4\npython scripts/sterilization_val.py --endotoxin --route iv --dose 0.5\n```",
        "extra": "计算模型依据公开标准的通用公式整理（ISO 11135/11137/17665、PDA TR29 清洁验证思路、药典细菌内毒素检查法）。落地具体产品须结合已验证的 D 值/z 值/生物负载数据与官方文本复核。",
        "related": ["manufacturing-gmp", "biocompatibility-iso10993", "design-controls-toolkit"],
        "upstream": None,  # 无既定上游目标（作品集自研；README 不渲染「上游投稿目标」行）
    },
    {
        "id": "manufacturing-gmp",
        "title": "生产质量管理与过程确认（GMP 条款对照 + IQ/OQ/PQ）",
        "layer": "L1",
        "license": "CC-BY-4.0",
        "entry": "scripts/gmp_toolkit.py",
        "description": "医疗器械生产质量管理规范（GMP）自查工具：2014 版条款框架清单 + 版本差异对照（载入两版条款 JSON 自动 diff）+ 过程确认 IQ/OQ/PQ 检查单生成。服务「2025 修订版 vs 2014 版 GMP 差异研究」与生产现场体系自查。",
        "keywords": ["gmp", "生产质量管理", "过程确认", "iq", "oq", "pq", "iso13485", "生产"],
        "file_patterns": ["gmp_toolkit.py"],
        "intents": ["GMP 自查", "版本差异对照", "过程确认方案"],
        "provides": ["manufacturing-gmp", "gmp-checklist", "version-diff", "iq-oq-pq"],
        "cost": "low",
        "lazy": True,
        "nested": True,
        "deps": [],
        "idea": "GMP 条款对照 + 过程确认（IQ/OQ/PQ）工具箱",
        "features": [
            "GMP 条款框架清单（2014 版章节结构，2025 修订关注项以 TO_BE_VERIFIED 占位，不虚构条款号）",
            "版本差异：--diff old.json new.json 自动比对条款增删改",
            "IQ/OQ/PQ 三阶段检查单生成（安装/运行/性能确认）",
            "零依赖 + CLI",
        ],
        "extension_note": "新增条款：在 GMP_CHAPTERS 加一项；差异对照只需维护条款 JSON。",
        "usage": "```bash\npython scripts/gmp_toolkit.py --demo\npython scripts/gmp_toolkit.py --pq\npython scripts/gmp_toolkit.py --diff gmp2014.json gmp2025.json\n```",
        "extra": "条款内容以官方发布文本为准；本工具不复制法规全文，只提供结构清单与差异计算能力。2025 修订版具体差异项需按官方通告逐条填入（TO_BE_VERIFIED 占位）。",
        "related": ["sterilization-validation", "design-controls-toolkit", "device-regulatory-map"],
        "upstream": None,  # 无既定上游目标（作品集自研）
    },
    {
        "id": "pms-vigilance",
        "title": "上市后监督与警戒工具（报告时限/召回分级/PSUR）",
        "layer": "L1",
        "license": "Apache-2.0",
        "entry": "scripts/pms_report.py",
        "description": "上市后监督（PMS）与警戒（Vigilance）时限计算与合规工具：NMPA 不良事件报告（死亡 7 日/严重伤害 20 日/群体 12 小时）、EU MDR Art.87（2/10/15 天）、FDA MDR（30 日/5 工作日/806 召回 10 工作日）、召回分级时限表（NMPA 一级 1 日起/FDA Class I–III）、PSUR/定期风险评价周期。输入获知日期，输出各辖区截止日。",
        "keywords": ["pms", "vigilance", "不良事件", "警戒", "召回", "psur", "pmcf", "mdr", "fsca"],
        "file_patterns": ["pms_report.py"],
        "intents": ["不良事件报告时限", "召回分级", "PSUR 周期", "FSCA"],
        "provides": ["pms-vigilance", "report-deadline", "recall-levels", "psur-cycle"],
        "cost": "low",
        "lazy": True,
        "nested": True,
        "deps": [],
        "idea": "PMS/警戒时限计算器（NMPA/MDR/FDA 报告与召回时限）",
        "features": [
            "报告时限计算：输入获知日期+辖区+事件类型 → 截止日期（自然日/工作日自动区分）",
            "召回分级表：NMPA 一级/二级/三级（通知/报告/评估时限）与 FDA Class I/II/III",
            "PSUR 周期：EU MDR IIb/III 年度、IIa 两年；NMPA 定期风险评价每满一年 60 日内",
            "已核实事实全部标注法规出处（Art.87 / 21 CFR 803/806 / 总局令第 1 号、第 29 号）",
        ],
        "extension_note": "新增辖区/事件类型：在 REPORTING_RULES 加一项。",
        "usage": "```bash\npython scripts/pms_report.py --demo\npython scripts/pms_report.py --aware 2026-10-01 --jurisdiction EU --event death\npython scripts/pms_report.py --recall --level 1 --jurisdiction CN\n```",
        "extra": "时限依据已核实官方文本整理；日/工作日、时区按输入日期本地计算。紧急事件以「立即报告」为第一原则，计算器只做最迟期限兜底。",
        "related": ["iso14971-risk-file", "samd-ra-toolkit", "clinical-evaluation"],
        "upstream": None,  # 无既定上游目标（作品集自研）
    },
    # ------------------------------------------------------------------ L1 其余
    {
        "id": "iec62304-software",
        "title": "医疗器械软件生命周期（IEC 62304 安全分级/过程映射）",
        "layer": "L1",
        "license": "CC-BY-4.0",
        "entry": "scripts/sw_lifecycle.py",
        "description": "IEC 62304:2006+A1:2015 医疗器械软件生命周期工具：软件安全等级 A/B/C 判定器（基于伤害可能性×严重度）、软件开发生命周期过程清单（策划/需求/架构/单元/集成/系统测试/发布/维护）、与 Agile/CI 实践的映射建议、SOUP 第三方组件管理检查点。",
        "keywords": ["iec62304", "software-lifecycle", "软件安全等级", "soup", "医疗软件", "agile"],
        "file_patterns": ["sw_lifecycle.py"],
        "intents": ["软件安全分级", "62304 自查", "SOUP 管理"],
        "provides": ["iec62304-software", "safety-class", "sw-checklist", "soup-register"],
        "cost": "low",
        "lazy": True,
        "nested": True,
        "deps": [],
        "idea": "IEC 62304 软件安全分级判定 + 生命周期过程清单",
        "features": [
            "安全分级判定：伤害严重度 × 可能性 → Class A/B/C（62304 §4.3 精神）",
            "过程清单：§5–§8 策划/需求/架构/详细设计/单元/集成/系统测试/发布/维护",
            "Agile 映射：sprint/DoD 与 V&V 证据的对应建议",
            "SOUP 登记：第三方组件（版本/已知异常/风险评估）检查点",
        ],
        "extension_note": "新增过程项：在 SW_PROCESSES 加一项。",
        "usage": "```bash\npython scripts/sw_lifecycle.py --demo\npython scripts/sw_lifecycle.py --classify --severity 4 --probability 3\n```",
        "extra": "分级判定为工程辅助：最终等级须结合风险管理文件（ISO 14971）输出判定。标准原文以 IEC 官方版本为准。",
        "related": ["samd-ra-toolkit", "design-controls-toolkit", "cybersecurity-medical"],
        "upstream": None,  # 无既定上游目标（作品集自研）
    },
    {
        "id": "device-regulatory-map",
        "title": "通用器械跨辖区监管映射（分类/路径/时限）",
        "layer": "L1",
        "license": "CC-BY-4.0",
        "entry": "scripts/device_reg_map.py",
        "description": "非软件类医疗器械的跨辖区监管映射：分类规则（NMPA《医疗器械分类规则》+ 分类目录、EU MDR Annex VIII 22 条分类规则、FDA 21 CFR 862–892 专科分类 + 860 程序、PMDA 药机法 Ⅰ–Ⅳ）、注册路径（注册/备案/510(k)/De Novo/PMA/THP）、代表机构要求（MAH/EC REP/US Agent）与典型周期经验值。",
        "keywords": ["regulatory", "classification", "分类规则", "nmpa", "mdr", "fda", "pmda", "mdsap", "注册"],
        "file_patterns": ["device_reg_map.py"],
        "intents": ["器械分类", "注册路径", "辖区对比"],
        "provides": ["device-regulatory-map", "classification-rules", "pathway-map"],
        "cost": "low",
        "lazy": True,
        "nested": True,
        "deps": [],
        "idea": "通用器械跨辖区分类与路径映射（补 SaMD 之外的通用件）",
        "features": [
            "分类规则索引：EU MDR Annex VIII（22 条）、FDA 21 CFR 862–892、NMPA 分类规则+目录、PMDA Ⅰ–Ⅳ",
            "路径对比：注册申报 vs 备案、510(k)/De Novo/PMA、CE 符合性评估路线",
            "代表机构：MAH / EC REP / US Agent 职责对照",
            "周期经验值显式标注「非法定时限」",
        ],
        "extension_note": "新增辖区：在 JURISDICTIONS 字典加一项。",
        "usage": "```bash\npython scripts/device_reg_map.py --demo\npython scripts/device_reg_map.py --jurisdiction EU\n```",
        "extra": "与 samd-ra-toolkit 互补：本仓管通用器械，samd 仓管 SaMD/AIaMD。分类结论须以官方分类目录/规则原文复核。",
        "related": ["samd-ra-toolkit", "udi-assignment", "clinical-evaluation"],
        "upstream": "OpenRegulatory/templates",
    },
    {
        "id": "clinical-evaluation",
        "title": "临床评价与 PMCF 规划器（CER 路径/同品种比对）",
        "layer": "L1",
        "license": "CC-BY-4.0",
        "entry": "scripts/cer_planner.py",
        "description": "临床评价（CER）路径规划与 PMCF 计划生成：同品种比对（EU MDR Annex XIV + MEDDEV 2.7.1 rev.4）、临床试验路径、NMPA 临床评价指导原则路径、FDA 510(k) 实质等效；PMCF 计划模板（终点/人群/随访/统计）与 PSUR/CER 更新触发条件。",
        "keywords": ["cer", "clinical-evaluation", "pmcf", "临床评价", "同品种", "psur"],
        "file_patterns": ["cer_planner.py"],
        "intents": ["临床评价路径", "同品种比对", "PMCF 计划"],
        "provides": ["clinical-evaluation", "cer-path", "pmcf-plan", "equivalence"],
        "cost": "low",
        "lazy": True,
        "nested": True,
        "deps": [],
        "idea": "CER 路径规划 + PMCF 计划生成（同品种/临床试验两条路）",
        "features": [
            "路径判定器：按器械类别/创新性/同品种可得性给出路径建议与证据缺口",
            "同品种比对要素清单（特性/差异/等同性论证/文献检索策略）",
            "PMCF 计划模板：终点、人群、随访时长、统计方法、报告周期",
            "更新触发：变更/不良事件趋势/新文献 → CER 更新评估",
        ],
        "extension_note": "新增辖区路径：在 CER_PATHS 加一项。",
        "usage": "```bash\npython scripts/cer_planner.py --demo\npython scripts/cer_planner.py --pmcf\n```",
        "extra": "同品种路径的等同性论证是注册审评核心难点，本工具只做结构化规划，不替代临床专家论证。",
        "related": ["device-regulatory-map", "pms-vigilance", "ml-validation-toolkit"],
        "upstream": "OpenRegulatory/templates",
    },
    {
        "id": "biocompatibility-iso10993",
        "title": "生物学评价终点矩阵（ISO 10993-1 按接触类型）",
        "layer": "L1",
        "license": "CC-BY-4.0",
        "entry": "scripts/biocompat.py",
        "description": "ISO 10993-1:2018 生物学评价终点判定矩阵：按接触性质（表面/外部接入/植入）× 接触组织（皮肤/粘膜/损伤皮肤/组织/骨/血液/神经）× 接触时限（有限 ≤24h / 24h–30d / >30d）输出需评终点（细胞毒性/致敏/刺激/急性/亚慢性/慢性/遗传毒性/致癌/生殖/植入/血液相容性/降解），并给出化学表征（ISO 10993-18）与 Gap 分析清单。",
        "keywords": ["iso10993", "biocompatibility", "生物相容性", "细胞毒性", "致敏", "化学表征"],
        "file_patterns": ["biocompat.py"],
        "intents": ["生物相容性评价", "终点选择", "10993 矩阵"],
        "provides": ["biocompatibility-iso10993", "endpoint-matrix", "gap-analysis"],
        "cost": "low",
        "lazy": True,
        "nested": True,
        "deps": [],
        "idea": "ISO 10993-1 终点判定矩阵（接触类型×时限→需评终点）",
        "features": [
            "终点矩阵：接触性质 × 接触组织 × 时限 → 必评/条件评终点清单",
            "植入类扩展：骨/组织/血液接触的植入专项终点",
            "化学表征挂点：ISO 10993-18 可浸出物/毒理学风险评估阈值（TTC）提示",
            "Gap 分析：已有报告 vs 需评终点缺口输出",
        ],
        "extension_note": "新增终点：在 ENDPOINT_MATRIX 加一行。",
        "usage": "```bash\npython scripts/biocompat.py --demo\npython scripts/biocompat.py --nature implant --tissue bone --duration permanent\n```",
        "extra": "矩阵按 ISO 10993-1:2018 通用框架整理；具体产品的终点减免须以毒理学风险评估（TRA/化学表征）论证。",
        "related": ["sterilization-validation", "design-controls-toolkit", "manufacturing-gmp"],
        "upstream": None,  # 无既定上游目标（作品集自研）
    },
    {
        "id": "udi-assignment",
        "title": "UDI 赋码工具（GS1 DI/PI + 辖区数据库字段）",
        "layer": "L3",
        "license": "CC0",
        "entry": "scripts/udi_assign.py",
        "description": "医疗器械唯一标识（UDI）赋码参考实现：GS1 GTIN-14 校验位计算（mod-10）、DI/PI 拆分（生产日期/批号/序列号/有效期）、HIBCC/ICCBBA 体系说明、FDA GUDID / NMPA 器械 UDI 数据库 / EUDAMED 三侧必填字段对照。补 fhir-ortho-toolkit（数据侧）与 multilingual-ifu（标签侧）之间的赋码缺口。",
        "keywords": ["udi", "gs1", "gtin", "hibcc", "iccbba", "gudid", "eudamed", "唯一标识"],
        "file_patterns": ["udi_assign.py"],
        "intents": ["UDI 赋码", "GTIN 校验位", "DI/PI 拆分", "UDI 数据库字段"],
        "provides": ["udi-assignment", "gtin-check-digit", "di-pi-split", "udi-db-fields"],
        "cost": "low",
        "lazy": True,
        "nested": True,
        "deps": [],
        "idea": "UDI 赋码工具（GS1 校验位 + DI/PI + 三侧数据库字段）",
        "features": [
            "GS1 GTIN-13/14 校验位计算（mod-10 算法，可验证）",
            "DI/PI 拆分与 carrierHRF 生成（(01)DI(11)日期(10)批号…）",
            "三侧数据库字段对照：FDA GUDID / NMPA UDI / EUDAMED UDI/Device",
            "零依赖 + CLI：可直接用于赋码脚本集成",
        ],
        "extension_note": "新增赋码体系：在 ISSUERS 注册表加一项。",
        "usage": "```bash\npython scripts/udi_assign.py --demo\npython scripts/udi_assign.py --gtin 0987654321098\npython scripts/udi_assign.py --carrier --di 09876543210987 --lot A1 --exp 20280101\n```",
        "extra": "校验位算法为公开数学；各辖区 UDI 数据库字段以官方最新指南为准（GUDID/NMPA 数据库填报口径可能更新，TO_BE_VERIFIED 占位）。",
        "related": ["fhir-ortho-toolkit", "multilingual-ifu", "device-regulatory-map"],
        "upstream": "GS1 / HIBCC / ICCBBA（社区）",
    },
    {
        "id": "cybersecurity-medical",
        "title": "医疗器械网络安全工具箱（IEC 81001-5-1 + SBOM）",
        "layer": "L1",
        "license": "Apache-2.0",
        "entry": "scripts/cyber_check.py",
        "description": "医疗器械网络安全合规工具：IEC 81001-5-1 安全开发生命周期检查单、FDA 预市网络安全指南（2023）要点清单、威胁建模提示（STRIDE 医疗适配）、SBOM（SPDX/CycloneDX）检查与组件漏洞关注项、安全更新与沟通计划模板。",
        "keywords": ["cybersecurity", "iec81001", "sbom", "spdx", "cyclonedx", "网络安全", "威胁建模"],
        "file_patterns": ["cyber_check.py"],
        "intents": ["网络安全自查", "SBOM 检查", "威胁建模"],
        "provides": ["cybersecurity-medical", "cyber-checklist", "sbom-check", "threat-model"],
        "cost": "low",
        "lazy": True,
        "nested": True,
        "deps": [],
        "idea": "医疗器械网络安全检查单 + SBOM 校验（81001-5-1/FDA 2023）",
        "features": [
            "81001-5-1 检查单：安全需求/架构/实现/验证/维护/退役全生命周期",
            "FDA 预市网络安全要点：SBOM、漏洞披露、安全更新能力",
            "SBOM 校验：SPDX/CycloneDX 字段完整性检查（本地 JSON）",
            "STRIDE 医疗适配威胁建模提示卡",
        ],
        "extension_note": "新增检查项：在 CYBER_CATALOG 加一项。",
        "usage": "```bash\npython scripts/cyber_check.py --demo\npython scripts/cyber_check.py --checklist   # SBOM 校验需准备本地文件: --sbom <your-sbom.json>\n```",
        "extra": "与 delivery-guard 互补：delivery-guard 管交付门禁（密钥泄漏等），本仓管产品网络安全体系（81001-5-1/FDA 指南）。",
        "related": ["delivery-guard", "iec62304-software", "samd-ra-toolkit"],
        "upstream": None,  # 无既定上游目标（作品集自研）
    },
]
