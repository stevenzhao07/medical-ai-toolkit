# AI 参与指南（人和 AI 都能 5 分钟上手）

> 配套：`scaffold.py`（骨架生成）· `router.py`（intent→module 路由）· `idea_scaffold.py`（说想法即搭建）· `harness.py`（6 维度自动测试）
> 适用：本账号 `@stevenzhao07` 全部开源仓（lgd-skeleton/1.0 可插拔模块）
> 原则：**参与门槛降到最低——人说一句话、AI 说一句话，都能自动搭起来并跑测试。**

---

## 0. 红线（任何贡献都不可违反）

1. **纯技术贡献**，不含商业营销；MedXpert 仅作贡献者署名（@stevenzhao07）。
2. **不挂机构自推**（不代任何机构主张标准或背书）。
3. **标准轨道以个人专家 Xinghua Zhao 名义参与**（不代机构主张标准或背书）；Tier A 开源可署名 MedXpert。
4. **对外发布前须仓库所有者「go」**（建仓/Issue/fork/PR 等对外动作须经所有者确认后执行）。

---

## 1. 给人类贡献者：30 秒上手

```bash
# 1) fork + clone
git clone https://github.com/stevenzhao07/<repo>.git && cd <repo>
# 2) 看效果（每个仓都内置 --demo）
python <entry> --demo        # entry 见该仓 module.json 的 "entry" 字段
# 3) 冒烟自检（单仓只能到这步——harness.py 只在门户开发态，见 §4）
python <entry> --help
```

**贡献流程**
1. 分支命名（前缀表见 §2）：`feat/...`、`fix/...`、`human/...`。
2. **一次 PR 只做一件事**（one PR one task）。
3. 提交前在门户开发态跑 `harness.py --module <repo>`，6 维度全过再提 PR（单仓独立克隆无 harness.py，见 §4）。
4. PR 正文写清：改了什么 / 为什么 / 跑了什么命令 / 已知限制。
5. 只动你自己分支，绝不碰 `vendor/`、`secrets`、他人模块的内部实现。

---

## 2. 给 AI 编码代理：自主贡献协议

> 目标：AI 拿到一句任务描述，自己选模块、自己搭、自己测，**用户不介入**；只有「对外发布」才升级到人确认。
> 依据标准：[AGENTS.md（OpenAI 2025-08 发布，2025-12-09 捐 Linux Foundation 的 AAIF，60K+ 仓采用）](https://openai.com/index/agentic-ai-foundation)、[conventionalbranch.org 的 AI 分支前缀规范](https://conventionalbranch.org/zh-hant/)。

### 2.1 AI 自主工作流（标准动作）

```
1. 读根 AGENTS.md / 本仓 AGENTS.md（单一事实源）
2. 路由：python router.py "<任务描述>"   → 命中现有模块则加载其全文
3. 若任务 = 新想法：python idea_scaffold.py "<想法>"  → 命中复用 / 否则自动建骨架
4. 改代码（只动 plugins/ 或 module.json 注册表，不改主流程）
5. 自检：python harness.py --module <repo>
6. 建分支 + 提交 + 开 PR（按下方自标识规则）
```

### 2.2 分支命名（AI 来源前缀）

按 [conventionalbranch.org](https://conventionalbranch.org/zh-hant/) 的 AI Agent Source Prefixes：

| 前缀 | 含义 | 示例 |
|---|---|---|
| `agent/` | 任意 AI 代理（通用） | `agent/add-fhir-observation` |
| `codex/` | OpenAI Codex | `codex/fix-demo-crash` |
| `claude/` | Claude Code | `claude/expand-checklist` |
| `copilot/` | GitHub Copilot | `copilot/add-ja-locale` |
| `cursor/` | Cursor | `cursor/emit-passport` |
| `ai/` | 任意 AI（v1.1.0 起） | `ai/assess-idea` |

> 人类贡献者用 `feat/` `fix/` `human/` 或普通 conventional 前缀。**主干 `main` 不加前缀。**

### 2.3 AI 自标识（必填，放进 commit trailer + PR 正文）

参考社区实践（[51cto 提交规范](https://blog.51cto.com/u_16099267/14841721)、[Yaked1/ai-lab-codex-workbench CONTRIBUTING](https://github.com/Yaked1/ai-lab-codex-workbench/blob/main/CONTRIBUTING.md)）：

```
提交信息：
<type>(<scope>): <简述>

Agent-Model: <模型名，如 gpt-5 / claude-opus / qwen3.5>
Agent-Task:  <任务 id 或一句话>
Agent-Decision: <关键决策与理由>
Agent-Limitation: <已知限制 / 待校验项>
```

PR 正文首行加一句：`> 本 PR 由 AI 编码代理生成（模型：<名>），人工复核后再合。`

### 2.4 Reading Order（新人/新 Agent 该按什么顺序读）

```
1. AGENTS.md        ← 这个仓是干嘛的、怎么跑（30 秒）
2. module.json      ← 机器可发现的元数据（triggers/provides/entry）
3. README.md        ← 人读的使用说明 + 路由说明
4. scripts/*.py     ← 实际实现（零依赖，标准库即可跑）
5. plugins/         ← 扩展点（加一行注册即生效）
6. CONTRIBUTING.md  ← 本文件（如何参与）
```

### 2.5 docs-as-code（防止文档漂移）

- 文档即代码：模板/清单改了，脚本输出要同步改；反之亦然。
- 任何「能力」都要在 `module.json` 的 `provides` 里登记，否则 AI 路由不到。
- 改了 `provides`/`triggers`/`intents`，必须重跑 `harness.py`（会校验 schema）。

---

## 3. 如何加一个模块 / 插件（扩展契约）

**lgd-skeleton/1.0 的核心承诺：一切即插件——主流程零改动。**

### 3.1 加一个「插件」（最小动作，不动主码）

进任意仓的 `plugins/` 目录，按 `module.json` 的扩展点说明加文件，并在注册表加一行。示例：
- `ai-a3-laws`：在 `LAWS` 注册表加 `(law_id, fn)` 即新增一条定律。
- `samd-ra-toolkit`：在 `JURISDICTIONS` 字典加一项即新增辖区。
- `multilingual-ifu`：复制 `ortho-ifu.zh.md` 为 `ortho-ifu.<lang>.md` 并对齐 7 段，校验脚本自动纳入。

### 3.2 加一个「新模块」（说想法即搭建）

```bash
python idea_scaffold.py "骨科 IFU 多语种对照 + 日文版"
# → 命中现有 multilingual-ifu 则复用；否则生成新 module 骨架
# → 自动调 scaffold.py 建 module.json/AGENTS.md/CLAUDE.md/llms.txt/README.md
# → 自动跑 harness.py 自检
```

生成的模块天然可被 `medical-ai-toolkit` 总入口路由发现（嵌套）。

---

## 4. 本地自检（harness.py · 6 维度）

| 维度 | 测什么 | 不过会怎样 |
|---|---|---|
| 适配性 fit | module.json schema / triggers / provides 合法 | AI 无法路由你 |
| 准确性 accuracy | `entry --demo` 输出非空且含关键字段 | 外人跑不动 demo |
| 流畅性 fluency | `entry --help` 不崩 | 代理调用即挂 |
| 外人实跑 outsider | README「使用」段命令全部能 smoke 跑 | 陌生人 clone 即卡 |
| 易用性 usability | 有使用段 + entry + CTA | 不知怎么用/怎么参与 |
| 语义回归 gold | gold_set.json 逐条过（当前 **21 条 = 21 个模块 × 1 条金样本**；此前文档称「218 条」与实测不符，已于 2026-10-14 勘误；缺 gold 硬性判负） | 回归坏了没人知 |

**布局说明（2026-10-12 复审修复）**：`harness.py` 只存在于门户开发态（21 仓平级
`repos/` 布局）。单仓独立克隆跑 `python harness.py` 会 file not found——这是
已知边界，不是 bug；单仓请用 `--demo`/`--help` 冒烟，完整 6 维自检按：
```bash
git clone https://github.com/stevenzhao07/medical-ai-toolkit.git portal-dev && cd portal-dev
# 把你的改动同步进 portal-dev/repos/<repo>/ 后：
python harness.py --module <repo>
python harness.py --all                 # 测全部 21 模块（开发态）
python harness.py --report report.md    # 出报告
```

CI：门户仓 `.github/workflows/harness.yml` 跑自身 6 维自测 + discover 路由冒烟
（独立克隆态无 repos/，`--all` 明确 SKIP 返回 0，不崩也不假绿）。

---

## 5. Dev Container / Codespaces（5 分钟零环境上手）

每个仓附带 `.devcontainer/devcontainer.json`（Python 3.12，零额外依赖，因为脚本只用标准库）。点 GitHub 的 **Code → Open with Codespaces** 即获得一个预装好环境的云开发机，打开终端直接 `python <entry> --demo`。

```json
{
  "name": "LGD Skeleton",
  "image": "mcr.microsoft.com/devcontainers/python:3.12",
  "postCreateCommand": "python --version",
  "customizations": {
    "vscode": { "extensions": ["ms-python.python"] }
  }
}
```

> 依据：[Codex CLI in GitHub Codespaces 实践（devcontainer + prebuild + secrets）](https://codex.danielvaughan.com/2026/05/26/codex-cli-github-codespaces-devcontainer-prebuilds-secrets-cloud-agent-workflows)。

---

## 6. 我们遵循的「机器可发现」标准（已核实）

| 标准 | 现状（核实） | 我们在哪用 |
|---|---|---|
| **AGENTS.md** | OpenAI 2025-08 发布；2025-12-09 捐 Linux Foundation **AAIF**；60K+ 仓；「nearest wins」原生嵌套 | 每个仓 + 每个 module 都有；正中套娃需求 |
| **llms.txt / llms-full.txt** | Jeremy Howard（Answer.AI）2024-09-03 提案；Shopify 2026-05 起每店默认发 `/agents.md`+`/llms.txt`+`/llms-full.txt` | 每仓 emit；根门户 `medical-ai-toolkit` 发总索引 |
| **A2A Agent Card** | Google 2025-04 发布，2025-06 捐 Linux Foundation；150+ 组织；固定路径 `/.well-known/agent.json` | 根门户 emit `agent.json` 描述全部能力 |
| **Spec Kit（SDD）** | GitHub 官方，MIT，135K+ stars，38+ agent 集成；constitution→spec→plan→tasks→implement→converge | 大特性可用 `specify` 补 spec/plan 工件（可选） |
| **Smithery（npm for MCP）** | 100K+ skills / 数千 MCP servers；`npx skills add smithery/cli` | 可选方向：把「说想法即搭建」做成 MCP server 上架 |

> 诚实提示：llms.txt 当前主要服务于「agent 可读性」，尚无主流 AI 平台确认其影响搜索排名（[sherocommerce 分析](https://sherocommerce.com/blogs/insights/llms-txt-and-agents-md-for-ecommerce)）；我们做它是为了**让克隆仓库的 AI 代理自动读懂并调用**，而非 SEO 排名。

---

## 7. FAQ

**Q：我是 AI 代理，能直接改主代码吗？**
A：优先用 `plugins/` + `module.json` 注册表扩展（一切即插件）。确需改主流程时，必须在 PR 正文说明「为何无法用插件实现」，并等人工复核。

**Q：新想法和现有模块撞车怎么办？**
A：`idea_scaffold.py` 会先用 `router.py` 匹配，命中则**复用**现有模块（追加能力），不重复建仓。

**Q：为什么 harness 测出我仓 0/6？**
A：多半是 `entry --demo` 没实现 / README 缺「使用」段 / 缺 CTA / 使用段命令跑不通。补齐即可。这正是自动化测试在抓真问题。

**Q：企业想私有部署怎么办？**
A：fork 核心 → 写自己的 `config/` + 私有 `plugins/` → 合规可审计，不依赖我们。骨架天生跨行业/跨机构/跨国（见 README 的模块契约）。

---

*本指南随 `contrib/` 工具链一同维护；每个仓的 `CONTRIBUTING.md` 由 `scaffold.py` 自动派发本文件内容。*
