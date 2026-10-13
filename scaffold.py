#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scaffold.py — MedXpert 医疗 AI 开源仓「可插拔骨架」生成器
=========================================================
把任意模块按 lgd-skeleton/1.0 契约生成一致的结构文件：
  module.json · AGENTS.md · CLAUDE.md · llms.txt · README.md
  LICENSE · .gitignore · plugins/.gitkeep

用法：
  python scaffold.py                     # 生成缺失的骨架文件（已存在则跳过，不覆盖）
  python scaffold.py --force             # 强制覆盖已存在的骨架文件（慎用）
  python scaffold.py --only ai-a3-laws   # 只处理指定模块

说明：
  - 本生成器是「rea scaffold idea」的手动移植（manual port），保证各仓骨架同构。
  - 安全默认（2026-10-13 第四轮复审修复）：**已存在的文件默认跳过、不覆盖**——因为
    README.md / module.json 在首次生成后会被手工精修（免责声明措辞、术语白话化、
    门禁计数等），无条件覆盖会把精修成果回退成模板。需要重置模板时显式 --force。
  - 不触碰 scripts/*.py 等实质代码；只产出契约骨架文件。
  - 红线：纯技术贡献，@stevenzhao07 署名，MedXpert 仅作 affiliation 披露。
"""
from __future__ import annotations
import json
import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
REPOS_DIR = os.path.join(ROOT, "repos")

DISCLOSURE = (
    "> **Contributed by [@stevenzhao07](https://github.com/stevenzhao07) · "
    "Affiliation: MedXpert (medical-device RA & regulatory consultancy) · "
    "Pure technical input, no commercial promotion.**"
)

LICENSE_TEXTS = {
    "Apache-2.0": """                                 Apache License
                           Version 2.0, January 2004
                        http://www.apache.org/licenses/

   Copyright 2026 MedXpert (美达信医疗科技)

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
""",
    "CC0": """Creative Commons CC0 1.0 Universal
Public Domain Dedication

SPDX-License-Identifier: CC0-1.0

To the extent permitted by law, the author(s) have dedicated all copyright
and related rights in the work to the public domain via CC0 1.0 Universal.
https://creativecommons.org/publicdomain/zero/1.0/

This repository is provided "as-is", without warranty of any kind.
""",
    "CC-BY-4.0": """Creative Commons Attribution 4.0 International

SPDX-License-Identifier: CC-BY-4.0

You may use, remix, and redistribute this work for any purpose, including
commercial, provided you give appropriate credit to @stevenzhao07 / MedXpert,
provide a link to the license, and indicate if changes were made.
https://creativecommons.org/licenses/by/4.0/

This repository is provided "as-is", without warranty of any kind.
""",
}

LICENSE_FILE_BY_LICENSE = {
    "Apache-2.0": "LICENSE",
    "CC0": "LICENSE",
    "CC-BY-4.0": "LICENSE",
}


def module_json(m: dict) -> str:
    obj = {
        "id": m["id"],
        "title": m["title"],
        "description": m["description"],
        "triggers": {
            "keywords": m["keywords"],
            "file_patterns": m["file_patterns"],
            "intents": m["intents"],
        },
        "provides": m["provides"],
        "skills": [],
        "needs_backends": [],
        "license": m["license"],
        "upstream": m.get("upstream"),
        "cost": m["cost"],
        "lazy": m["lazy"],
        "nested": m["nested"],
        "entry": m["entry"],
        "deps": m.get("deps", []),
        # 2026-10-12 复审修复：extension_note 进 module.json，成为 CONTRIBUTING
        # 「加能力」段的单一事实源（manifest 派发时从本字段读，不再落默认文案）。
        "extension_note": m.get("extension_note", "新增能力只需在主体代码注册表加一行，无需改主流程。"),
        "generated_by": "lgd-skeleton/1.0 (manual port from rea scaffold)",
        "idea": m["idea"],
    }
    return json.dumps(obj, ensure_ascii=False, indent=2) + "\n"


def agents_md(m: dict) -> str:
    ext = m.get("extension_note", "新增能力只需在主体代码注册表加一行，无需改主流程。")
    return f"""# AGENTS.md · {m['id']}

> 机器可发现入口（AI 编码代理 / Codex / Claude / Cursor）。单一事实源：本文件。

## 这是什么
{m['description']}

## 运行
```bash
python {m['entry']} --demo
python {m['entry']} --help
```

## 扩展契约（lgd-skeleton/1.0）
- **一切即插件**：仅依赖声明式 `module.json`，零配置。
- **按需装（lazy）**：仅 triggers 命中时加载。
- **可嵌套（nested）**：可被 `medical-ai-toolkit` 总入口路由。
- **扩展点**：`plugins/`({ext})

## 红线
纯技术贡献，不含商业营销；MedXpert 仅作为贡献者署名（@stevenzhao07）。
"""


def claude_md(m: dict) -> str:
    return f"""# CLAUDE.md
本文件指向 [AGENTS.md](./AGENTS.md)（单一事实源）。AI 编码代理请读 AGENTS.md。
"""


def llms_txt(m: dict) -> str:
    return f"""{m['id']}
========================
可插拔模块（lgd-skeleton/1.0）。{m['title']}。
入口: {m['entry']}
元数据: module.json
总入口: medical-ai-toolkit
关联: {', '.join(m.get('related', [])) or '—'}
许可: {m['license']} · 贡献者: @stevenzhao07 (MedXpert)
"""


def readme_md(m: dict) -> str:
    features = "\n".join(f"- {f}" for f in m["features"])
    related = "\n".join(
        f"- [{r}](https://github.com/stevenzhao07/{r})" for r in m.get("related", [])
    ) or "- —"
    upstream_line = ""
    if m.get("upstream"):
        upstream_line = f"\n**上游投稿目标**：{m['upstream']}"
    extra = m.get("extra", "")
    return f"""# {m['id']}

{DISCLOSURE}

{m['description']}

这是 MedXpert 把"医疗 AI 信任"方法论工程化落地的可插拔模块之一——把抽象的合规要求变成一条可重复运行的命令或参考实现。方法论四要素（白话版）：**治理守护者 XCGS** ＝ 为 AI 留下可核验的治理证据；**立法者 A³ Laws** ＝ 给自主系统划权限 / 监督 / 追责三条硬边界；**护照官 AI 护照** ＝ 为模型签发可追溯的身份凭证；**人机共存** ＝ 明确人类与 AI 的分工与兜底。

---

## 可插拔模块契约（lgd-skeleton/1.0）

本仓库是一个 **`lgd-skeleton/1.0` 可插拔模块**：

- **一切即插件**：仅依赖声明式 `module.json`，零配置；
- **按需装（lazy）**：仅 triggers 命中时加载；
- **可嵌套（nested）**：可被 `medical-ai-toolkit` 总入口路由发现；
- **扩展点**：`plugins/`({m.get('extension_note', '新增能力只需在主体代码注册表加一行')})。

机器可发现入口：`AGENTS.md` · `CLAUDE.md` · `llms.txt`。

## 特性

{features}
{upstream_line}

## 内容说明

{extra}

## 免责声明

本工具仅提供结构化模板与计算能力，**不构成法规建议、临床建议或产品合规结论**。具体产品的注册、临床评价、灭菌验证、风险分析、软件分级等决策，须由合资格人员依据目标辖区（NMPA / FDA / EU MDR / PMDA）最新法规文本作出；条款与限值以官方发布文本为准。使用本工具产生的一切后果由使用者自行承担。

## 使用

{m['usage']}

## 快速开始（30 秒）

```bash
git clone https://github.com/stevenzhao07/{m['id']}.git && cd {m['id']}
python {m['entry']} --demo
```

> 想参与或遇到问题？[提 Issue](https://github.com/stevenzhao07/{m['id']}/issues) · 完整《AI 参与指南》见 [medical-ai-toolkit](https://github.com/stevenzhao07/medical-ai-toolkit)。

## 路由（总入口）

本模块由 **[medical-ai-toolkit](https://github.com/stevenzhao07/medical-ai-toolkit)** 作为 `lgd-skeleton/1.0` 总入口自动路由发现。

## 关联模块

{related}

## 许可

{m['license']} — 见 [LICENSE](./LICENSE)。

## 关联（方法论来源）

- 理念溯源：个人专家关于医疗 AI 信任与治理的公开方法论（个人观点，不构成标准）
- 同账号系列：见 `medical-ai-toolkit` 导航
"""


def gitignore() -> str:
    return """# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# Virtual environments
.venv/
venv/
env/

# Generated artifacts
*.jsonl
ledger.jsonl
index.json
*.report.md
# 运行期生成的登记簿/输出（outsider/gold 跑 README 命令会产生，勿跟踪）
risk_register.json
passport.json
ortho_concept_set.sql
harness_report.md

# Editor / OS
.idea/
.vscode/
.DS_Store
*.swp
"""


def gitkeep(ext: str) -> str:
    return f"""# 扩展点（plugins/）
{ext}
"""


def repo_ci_yml(entry: str) -> str:
    """单仓独立克隆的 CI 冒烟（demo + help）。

    2026-10-13 第四轮复审新增：此前 21 个子仓均无 CI，子仓独立 push 时无任何
    质量门禁。本模板给每个子仓一份零依赖的最小冒烟 workflow。门户仓
    （medical-ai-toolkit）另有 .github/workflows/harness.yml，不用本模板。
    """
    e = entry or "scripts/__main__.py"
    return (
        "name: smoke\n"
        "on:\n"
        "  push:\n"
        "    branches: [main]\n"
        "  pull_request:\n"
        "permissions:\n"
        "  contents: read\n"
        "concurrency:\n"
        "  group: ${{ github.workflow }}-${{ github.ref }}\n"
        "  cancel-in-progress: true\n"
        "jobs:\n"
        "  smoke:\n"
        "    runs-on: ubuntu-latest\n"
        "    timeout-minutes: 5\n"
        "    steps:\n"
        "      - uses: actions/checkout@v4\n"
        "      - uses: actions/setup-python@v5\n"
        "        with:\n"
        "          python-version: '3.12'\n"
        "      - name: CLI smoke (demo + help)\n"
        "        run: |\n"
        f"          python {e} --demo\n"
        f"          python {e} --help\n"
    )


def contributing_md(m: dict) -> str:
    """每仓自包含的精简《AI 参与指南》（指向根门户完整版）。"""
    return f"""# CONTRIBUTING · {m['id']}（lgd-skeleton/1.0 可插拔模块）

> 完整《AI 参与指南》见根门户：https://github.com/stevenzhao07/medical-ai-toolkit/blob/main/AI_PARTICIPATION.md
> 红线：纯技术贡献；MedXpert 仅作署名（@stevenzhao07）；不挂机构自推；发布前需仓库所有者「go」。

## 30 秒上手
```bash
git clone https://github.com/stevenzhao07/{m['id']}.git && cd {m['id']}
python {m['entry']} --demo
python {m['entry']} --help
```

## 分支命名
- **AI 代理**：`agent/` `codex/` `claude/` `copilot/` `cursor/` `ai/` + 简述（如 `agent/add-fhir-observation`）
- **人类**：`feat/` `fix/` `human/` + 简述
- 一次 PR 只做一件事（one PR one task）。

## AI 自标识（写进 commit trailer + PR 正文）
```
Agent-Model: <模型名>
Agent-Task: <一句话任务>
Agent-Limitation: <已知限制 / 待校验项>
```

## 加能力（一切即插件，不动主码）
{m.get('extension_note', '新增能力只需在主体代码注册表加一行。')}

## 本地自检（CI 门禁）
**单仓独立克隆**：只能跑 `python {m['entry']} --demo` / `--help` 冒烟——`harness.py`
（6 维测试）只存在于根门户，不在本仓（2026-10-12 复审修复：原指引直接让单仓跑
`python harness.py`，必然 file not found）。

**完整 6 维自检**（适配性/准确性/流畅性/外人实跑/易用性/语义回归 gold）：
```bash
git clone https://github.com/stevenzhao07/medical-ai-toolkit.git portal-dev && cd portal-dev
# 开发态布局：把你的改动同步进 portal-dev/repos/{m['id']}/ 后
python harness.py --module {m['id']}
```
（CI 同款；gold 语义回归全绿再提 PR。）

## 路由 / 总入口
本模块由 **[medical-ai-toolkit](https://github.com/stevenzhao07/medical-ai-toolkit)** 自动路由发现。
有新想法？`python idea_scaffold.py "<想法>"` → 命中复用 / 否则自动建骨架并自检（在门户开发态运行）。
"""


# ---------------------------------------------------------------------------
# 模块清单（9 个标准模块 + 11 个生命周期模块，由 lifecycle_modules.py 注入；
# delivery-guard 已手工完成，跳过。2026-10-12：21 仓矩阵的 scaffold 事实源）
# ---------------------------------------------------------------------------
MANIFEST = [
    {
        "id": "multilingual-ifu",
        "title": "骨科器械 IFU 多语种对照语料（14 语种 = zh 母版 + 13 外语 × 7 段结构）",
        "layer": "L5",
        "license": "CC-BY-4.0",
        "entry": "scripts/ifu_index.py",
        "description": "把骨科植入物/器械使用说明（IFU）做成中→英/德/日/阿/法/西/意/葡/俄/韩/泰/印尼/越 13 外语对照的开源语料库（骨科植入物为参考示例，框架适用全部医疗器械），每段严格对齐 7 段结构（产品标识/预期用途/禁忌症/警告/清洁灭菌/追溯/不良事件）。13 外语覆盖是本模块的主要差异化方向（多数同类项目仅英文）。",
        "keywords": ["ifu", "multilingual", "多语种", "骨科", "orthopedics", "labeling", "翻译", "本地化"],
        "file_patterns": ["ortho-ifu.*.md", "ifu_index.py"],
        "intents": ["多语种IFU", "标签本地化", "骨科翻译"],
        "provides": ["multilingual-ifu", "ifu", "multilingual", "ortho-i18n"],
        "cost": "low",
        "lazy": True,
        "nested": True,
        "deps": [],
        "idea": "骨科 IFU 多语种对照（12 外语 + 中文母版）",
        "features": [
            "14 个语言版本（zh 母版 + 13 外语 en/de/ja/ar/fr/es/it/pt/ru/ko/th/id/vi），均遵循 7 段对齐结构",
            "CC BY 4.0 可署名再分发，对商业主体友好",
            "可插拔校验：`scripts/ifu_index.py` 自动清点 14 个语料完整性、段数、字数并产出 `index.json`",
            "弱品牌披露：顶部 HTML 注释含 CC BY 4.0 + @stevenzhao07 关联披露",
        ],
        "extension_note": "新增语种：复制 `ortho-ifu.zh.md` 为 `ortho-ifu.<lang>.md` 并对齐 7 段；校验脚本自动纳入。",
        "usage": "```bash\n# 校验全部语料完整性并生成 index.json\npython scripts/ifu_index.py --lang-dir . --out index.json\n```",
        "extra": "语料覆盖髋/膝关节置换相关骨科植入物与器械的使用说明要点，定位为「对照模板」而非某具体产品的注册标签；落地具体产品前须按目标辖区（NMPA/FDA/EU MDR/PMDA）法规二次审校。",
        "related": ["samd-ra-toolkit", "medical-ai-toolkit"],
        "upstream": "OpenRegulatory/templates（多语种）",
    },
    {
        "id": "ai-a3-laws",
        "title": "A³ Laws 运行时约束库（自主系统的三条安全边界）",
        "layer": "L2",
        "license": "CC0",
        "entry": "scripts/a3_laws.py",
        "description": "把「立法者（A³ Laws）」理念工程化为可部署的运行时约束库：对每一次自主决策做三定律校验——A1 权限边界（Authority）、A2 自主边界（人类监督）、A3 追责边界（可归因日志）。返回违规清单，可嵌入门禁或 Agent 循环。（对应『运行时约束』能力缺口。）",
        "keywords": ["a3-laws", "runtime", "constraint", "autonomy", "human-oversight", "accountability", "自主系统"],
        "file_patterns": ["a3_laws.py"],
        "intents": ["运行时约束", "自主边界", "人类监督"],
        "provides": ["ai-a3-laws", "a3", "runtime-constraint", "autonomy-guard"],
        "cost": "low",
        "lazy": True,
        "nested": True,
        "deps": [],
        "idea": "A³ Laws 运行时约束（Authority / Autonomy / Accountability）",
        "features": [
            "三条定律：`A1 Authority`（动作须在 authority_scope 白名单）、`A2 Autonomy`（高风险动作须 human_review=True）、`A3 Accountability`（须含 actor_id + decision_id 且可日志）",
            "零依赖：仅 Python 3.8+ 标准库",
            "可嵌门禁：`A3Guard.check(decision)` 返回 `list[Violation]`，退出码友好",
            "CLI：`python scripts/a3_laws.py --demo` 跑内置样例",
        ],
        "extension_note": "新增定律：在 `LAWS` 注册表加一个 `(law_id, fn)` 即可，主流程自动遍历。",
        "usage": "```bash\n# 跑内置样例（展示「通过 / 阻断」两种结果）\npython scripts/a3_laws.py --demo\n```\n\n也可用 `--json` 传入自定义决策做校验（须为 JSON 对象）：\n\n```bash\npython scripts/a3_laws.py --json '{\"action\":\"prescribe\",\"authority_scope\":[\"prescribe\"],\"actor_id\":\"agent-1\",\"decision_id\":\"d-1\",\"human_review\":true}'\n# 退出码：0 = 无违规；1 = 有违规（逐条打印）；2 = 输入非法（非 JSON / 非对象）\n```\n\n字段：`action`（动作）、`authority_scope`（A1 授权白名单）、`human_review`（A2，高风险动作须为 true）、`actor_id` / `decision_id`（A3 可追责标识）。",
        "extra": "A¹/A²/A³ 三定律对应「立法者」方法论：给自主系统划安全边界，而不是事后审计。它不自称标准，定位为可复用的参考实现，欢迎上游（OWASP AI Exchange）采纳。",
        "related": ["delivery-guard", "ai-model-passport", "ai-governance-checklist"],
        "upstream": "OWASP AI Exchange",
    },
    {
        "id": "ai-model-passport",
        "title": "AI 护照身份档案参考实现（身份/溯源/追责）",
        "layer": "L2/L3",
        "license": "CC0",
        "entry": "scripts/ai_passport.py",
        "description": "把「护照官（AI 护照制度）」理念做成可部署的参考实现：为每一个 AI 系统签发一份机器可读的『AI 护照』JSON（身份、模型卡引用、训练数据、预期用途、风险分级、符合性声明、签发哈希），支持签发与验证。（对应『AI 护照系统』能力缺口。）",
        "keywords": ["ai-passport", "passport", "identity", "provenance", "traceability", "AI护照"],
        "file_patterns": ["ai_passport.py"],
        "intents": ["AI护照", "身份档案", "溯源追责"],
        "provides": ["ai-model-passport", "passport", "ai-identity", "provenance"],
        "cost": "low",
        "lazy": True,
        "nested": True,
        "deps": [],
        "idea": "AI 护照制度（身份/溯源/追责）参考实现",
        "features": [
            "护照 schema：passport_id / issuer / model / intended_use / risk_class(I–IV) / training_data_refs / conformance_claims / issued_at / hash",
            "签发：`issue()` 对规范化 JSON 计算 SHA-256 作为防篡改指纹",
            "验证：`verify()` 校验指纹 + 必填字段 + 风险分级合法",
            "零依赖 + CLI：`issue` / `verify` 子命令",
        ],
        "extension_note": "新增符合性声明类型：在 `CONFORMANCE_CLAIMS` 枚举扩展，验证器自动校验。",
        "usage": "```bash\npython scripts/ai_passport.py issue --name ortho-ai --risk-class II\npython scripts/ai_passport.py verify passport.json\n```",
        "extra": "AI 护照 = 给 AI 系统一张『身份证』，让监管、医院、患者都能查到它从哪来、能干什么、风险多高。本仓由 Medxpert-org/ai-passport-spec（public）迁至 @stevenzhao07 统一账号。",
        "related": ["ai-a3-laws", "ai-governance-checklist", "delivery-guard"],
        "upstream": None,  # 无既定上游目标（作品集自研）
    },
    {
        "id": "samd-ra-toolkit",
        "title": "SaMD / AIaMD 法规质量体系工具包（跨辖区映射）",
        "layer": "L1",
        "license": "CC-BY-4.0",
        "entry": "scripts/samd_map.py",
        "description": "Software as a Medical Device（SaMD / AIaMD）的注册与质量体系工具包：SaMD 判定树 + IEC 62304 / ISO 14971(AI) / EU AI Act 映射 + PCCP 模板骨架 + AI-CER 骨架 + **跨辖区差异表（NMPA / EU MDR / FDA / PMDA）**。（对应『跨辖区监管映射模板』能力缺口。）",
        "keywords": ["samd", "aiamd", "NMPA", "FDA", "MDR", "PMDA", "regulatory", "SaMD判定", "监管映射"],
        "file_patterns": ["samd_map.py"],
        "intents": ["SaMD路径", "跨辖区监管", "法规映射"],
        "provides": ["samd-ra-toolkit", "samd", "ra-kit", "regulatory-map"],
        "cost": "low",
        "lazy": True,
        "nested": True,
        "deps": [],
        "idea": "SaMD/AIaMD 法规质量体系 + 跨辖区（NMPA/MDR/FDA/PMDA）差异映射",
        "features": [
            "跨辖区矩阵：NMPA / EU MDR / FDA / PMDA 的分类、路径、主管/公告机构、关键文档、典型周期",
            "SaMD 判定树：按风险类别（I–IV）给出辖区落地建议",
            "模板骨架：PCCP（ Predetermined Change Control Plan）、AI-CER 章节占位",
            "零依赖 + CLI：`python scripts/samd_map.py --jurisdiction EU`",
        ],
        "extension_note": "新增辖区：在 `JURISDICTIONS` 字典加一项，跨辖区表自动扩展。",
        "usage": "```bash\npython scripts/samd_map.py --jurisdiction ALL\npython scripts/samd_map.py --risk-class III --jurisdiction FDA\n```",
        "extra": "本仓定位为「法规工程师的工作台」，把分散在各辖区的 SaMD 要求聚到一张可检索的表。自创内容 CC BY 4.0；投向上游 OpenRegulatory/templates。",
        "related": ["ai-governance-checklist", "ml-validation-toolkit", "medical-ai-toolkit"],
        "upstream": "OpenRegulatory/templates",
    },
    {
        "id": "ai-governance-checklist",
        "title": "医疗 AI 治理聚合仓（模型卡/数据卡/人类监督检查单）",
        "layer": "L2",
        "license": "CC-BY-4.0",
        "entry": "scripts/gov_checklist.py",
        "description": "医疗 AI 治理的聚合开源仓：模型卡 / 数据卡模板 + 人类监督（human-in-the-loop）检查单 + 公平性测试骨架 + OWASP AI Exchange 医疗章节输入。把「人机共存」理念落到治理清单。",
        "keywords": ["ai-governance", "model-card", "data-card", "human-oversight", "fairness", "治理", "checklist"],
        "file_patterns": ["gov_checklist.py", "templates/model_card.md", "templates/data_card.md"],
        "intents": ["AI治理", "模型卡", "人类监督", "公平性"],
        "provides": ["ai-governance-checklist", "governance", "model-card", "checklist"],
        "cost": "low",
        "lazy": True,
        "nested": True,
        "deps": [],
        "idea": "医疗 AI 治理：模型卡/数据卡 + 人类监督 + 公平性（人机共存落地）",
        "features": [
            "治理检查单生成器：`gov_checklist.py` 从控制目录输出 Markdown 自检清单（模型卡/数据卡/人类监督/公平性/安全/溯源/监测）",
            "模板：`templates/model_card.md` + `templates/data_card.md` 可直接复制填",
            "人类监督检查单：高风险决策须人在回路的判定项",
            "零依赖 + CLI：按类别过滤输出",
        ],
        "extension_note": "新增控制项：在 `CONTROL_CATALOG` 加一项，检查单自动扩。",
        "usage": "```bash\npython scripts/gov_checklist.py --all\npython scripts/gov_checklist.py --category human-oversight\n```",
        "extra": "本仓混合许可：自创模板 CC BY 4.0；投向上游 OWASP AI Exchange（医疗章节）、aiverify-foundation（骨科公平性插件）。标准轨道用个人专家 Xinghua Zhao 弱品牌。",
        "related": ["ai-a3-laws", "ai-model-passport", "ml-validation-toolkit"],
        "upstream": "OWASP AI Exchange / aiverify-foundation",
    },
    {
        "id": "fhir-ortho-toolkit",
        "title": "骨科植入物 UDI 的 HL7 FHIR 轮廓（Spec 仓）",
        "layer": "L3",
        "license": "CC0",
        "entry": "scripts/fhir_ortho.py",
        "description": "骨科植入物唯一标识（UDI）的 HL7 FHIR R4 轮廓参考实现：Device（含 UDI carrier）、Patient、Procedure（THA/TKA）、Observation 的资源构造器与示例。定位为规范（spec）仓，投 HL7 社区。",
        "keywords": ["fhir", "ortho", "udi", "hl7", "device", "骨科", "互操作"],
        "file_patterns": ["fhir_ortho.py"],
        "intents": ["FHIR轮廓", "骨科UDI", "互操作"],
        "provides": ["fhir-ortho-toolkit", "fhir", "udi", "ortho-profile"],
        "cost": "low",
        "lazy": True,
        "nested": True,
        "deps": [],
        "idea": "骨科植入物 UDI 的 FHIR R4 轮廓（Device/Patient/Procedure/Observation）",
        "features": [
            "资源构造器：Device(UDI) / Patient / Procedure(THA,TKA) / Observation 返回规范 FHIR R4 dict",
            "示例输出：CLI `--resource Device --example` 打印可校验的 JSON",
            "UDI carrier 建模：DI/PI 拆分 + carrierHRF/carrierAIDC",
            "零依赖 + 规范仓姿态（CC0，便于 HL7 社区直接采用）",
        ],
        "extension_note": "新增轮廓：在 `BUILDERS` 注册表加一个资源构造器即可。",
        "usage": "```bash\npython scripts/fhir_ortho.py --resource Device --example\npython scripts/fhir_ortho.py --resource Procedure --example\n```",
        "extra": "本仓是「规范（spec）仓」而非产品：把骨科 UDI 怎么映射到 FHIR 讲清楚，供 HL7 社区 chat.fhir.org 征询与 IG PR。标准轨道用个人专家 Xinghua Zhao 弱品牌。",
        "related": ["omop-ortho-toolkit", "medical-ai-toolkit"],
        "upstream": "HL7 community / chat.fhir.org",
    },
    {
        "id": "omop-ortho-toolkit",
        "title": "骨科登记 → OMOP CDM ETL 提案与示例（OHDSI）",
        "layer": "L3",
        "license": "Apache-2.0",
        "entry": "scripts/omop_ortho.py",
        "description": "把骨科手术登记（关节置换 TKA/THA、植入物）映射到 OHDSI OMOP CDM 的 ETL 提案与示例：源代码（CPT/SNOMED）→ OMOP 概念集，产出概念集 SQL 骨架。投 OHDSI CDM WG。",
        "keywords": ["omop", "ohdsi", "cdm", "etl", "ortho", "登记", "概念集"],
        "file_patterns": ["omop_ortho.py"],
        "intents": ["OMOP映射", "骨科登记", "ETL"],
        "provides": ["omop-ortho-toolkit", "omop", "etl", "concept-set"],
        "cost": "low",
        "lazy": True,
        "nested": True,
        "deps": [],
        "idea": "骨科登记 → OMOP CDM ETL 提案 + 概念集示例",
        "features": [
            "概念集：TKA(CPT 27447) / THA(CPT 27130) / 植入物 等源代码 → OMOP vocabulary 映射",
            "ETL 骨架：`--emit-sql` 产出 concept_set 的 INSERT 占位（concept_id 标注待 vocab 校验）",
            "诚实标注：OMOP standard concept_id 须以本地 vocab 复核，脚本显式标记待校验项",
            "零依赖 + CLI",
        ],
        "extension_note": "新增术式：在 `PROCEDURE_MAP` 加源代码→名称，SQL 骨架自动扩。",
        "usage": "```bash\npython scripts/omop_ortho.py --list\npython scripts/omop_ortho.py --emit-sql --out ortho_concept_set.sql\n```",
        "extra": "本仓是提案（proposal）而非已验证的 vocab：concept_id 以 `(27447 -> ?)` 占位并标注『需以本地 OMOP vocabulary 复核』，避免误导。投 OHDSI CDM WG，用个人专家 Xinghua Zhao 弱品牌。",
        "related": ["fhir-ortho-toolkit", "medical-ai-toolkit"],
        "upstream": "OHDSI CDM WG",
    },
    {
        "id": "ml-validation-toolkit",
        "title": "医疗 AI 模型验证包（性能/校准/公平性，零依赖）",
        "layer": "L4",
        "license": "Apache-2.0",
        "entry": "scripts/ml_validation.py",
        "description": "医疗 AI 模型的验证工具包：给定 y_true / y_pred（可选 subgroup），计算 AUC、Accuracy、Precision/Recall/F1、Brier 校准误差，以及子组公平性缺口（人口均等等差 / 机会均等等差）。仅 Python 标准库实现，便于离线审计。",
        "keywords": ["ml-validation", "auc", "calibration", "fairness", "model-validation", "验证", "公平性"],
        "file_patterns": ["ml_validation.py"],
        "intents": ["模型验证", "公平性测试", "校准"],
        "provides": ["ml-validation-toolkit", "ml-validation", "fairness", "calibration"],
        "cost": "low",
        "lazy": True,
        "nested": True,
        "deps": [],
        "idea": "医疗 AI 模型验证（性能/校准/子组公平性，零依赖）",
        "features": [
            "指标：AUC（rank）、Accuracy、Precision/Recall/F1、Brier 校准误差",
            "公平性：子组人口均等 / 机会均等等差（demographic parity / equal opportunity gap）",
            "零依赖：仅标准库，可离线审计（不依赖 sklearn）",
            "CLI：`python scripts/ml_validation.py --data data.csv`",
        ],
        "extension_note": "新增指标：在 `METRICS` 注册表加一个 `(name, fn)` 即可。",
        "usage": "```bash\n# 自带演示数据，无需外部文件\npython scripts/ml_validation.py --demo\n```\n\n用自己的数据：准备含 `y_true,y_pred` 列的 CSV（参考仓库 `sample.csv`），再 `python scripts/ml_validation.py --data sample.csv --subgroup col`。",
        "extra": "本仓是 MLOps 验证的轻量模板：把『模型够不够好、对不同人群是否公平』量化出来，接 `delivery-guard` 门禁做发布前验证。",
        "related": ["delivery-guard", "ai-governance-checklist", "samd-ra-toolkit"],
        "upstream": None,  # 无既定上游目标（作品集自研）
    },
]

# 生命周期扩展模块（医疗器械全生命周期，非仅骨科/AI）——由 lifecycle_modules.py 注入
# 2026-10-12 三方复审 P0 修复：import 失败不再静默降级。曾因静默 except 导致
# 门户单仓 scaffold 只生成 9 个标准模块、11 个生命周期模块静默丢失（假完成）。
_LIFECYCLE_PATH = os.path.join(ROOT, "lifecycle_modules.py")
try:
    from lifecycle_modules import MODULES as EXTRA_MODULES
except ImportError as _e:
    raise SystemExit(
        f"[scaffold] 致命：{_LIFECYCLE_PATH} 缺失或无法导入（{_e}）。"
        "缺它只能生成 9 个标准模块，11 个生命周期模块会静默丢失——"
        "请从开发态 contrib/ 复制 lifecycle_modules.py 到本目录后重跑。"
    )

MANIFEST = MANIFEST + EXTRA_MODULES

SKIP = {"delivery-guard"}


def main() -> int:
    only = None
    force = "--force" in sys.argv
    if "--only" in sys.argv:
        only = sys.argv[sys.argv.index("--only") + 1]
    # 2026-10-12 复审修复：原写法 `if m["id"] != only` 把 --only 指定模块**排除**掉，
    # 语义反转。正确语义：--only X = 只生成 X。
    modules = [m for m in MANIFEST if m["id"] == only] if only else MANIFEST
    modules = [m for m in modules if m["id"] not in SKIP]
    if only and not modules:
        print(f"[warn] --only {only} 不在 MANIFEST（或在 SKIP {sorted(SKIP)}），未生成任何仓。")
        return 2
    written = skipped = 0
    for m in modules:
        repo = os.path.join(REPOS_DIR, m["id"])
        os.makedirs(os.path.join(repo, "scripts"), exist_ok=True)
        os.makedirs(os.path.join(repo, "plugins"), exist_ok=True)
        files = {
            "module.json": module_json(m),
            "AGENTS.md": agents_md(m),
            "CLAUDE.md": claude_md(m),
            "llms.txt": llms_txt(m),
            "README.md": readme_md(m),
            "CONTRIBUTING.md": contributing_md(m),
            "LICENSE": LICENSE_TEXTS[m["license"]],
            ".gitignore": gitignore(),
            "plugins/.gitkeep": gitkeep(m.get("extension_note", "新增能力只需在主体代码注册表加一行。")),
            # 单仓 CI 冒烟（门户仓另有 harness.yml，跳过）
            ".github/workflows/smoke.yml": repo_ci_yml(m.get("entry", "")) if m["id"] != "medical-ai-toolkit" else None,
        }
        w = s = 0
        for name, content in files.items():
            if content is None:
                continue
            p = os.path.join(repo, name)
            # 安全默认：已存在即跳过（README/module.json 会被手工精修，勿回退）
            if os.path.exists(p) and not force:
                s += 1
                continue
            os.makedirs(os.path.dirname(p), exist_ok=True)
            with open(p, "w", encoding="utf-8", newline="\n") as f:
                f.write(content)
            w += 1
        written += w
        skipped += s
        print(f"[ok] {m['id']}  (写入 {w} · 跳过已存在 {s})")
    tail = "（--force 已强制覆盖）" if force else "（已存在文件均跳过，未覆盖）"
    print(f"\n完成：处理 {len(modules)} 个仓骨架{tail}；写入 {written} · 跳过 {skipped}。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
