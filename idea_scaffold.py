#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
idea_scaffold.py — 说想法即自动搭建
====================================
AI 收到一句自然语言想法 → 解析意图 → 命中现有模块则复用，否则生成新模块规范
→ 调 scaffold .emit 建仓骨架（lgd-skeleton/1.0）→ 跑 harness 自检。

演示"最低参与门槛"原则：人/AI 只要说一句话，骨架自动就位。

用法：
  python idea_scaffold.py "给AI做一个运行时约束库，三定律"
  python idea_scaffold.py "我想做骨科IFU多语种对照"   # 命中现有 → 复用建议
"""
from __future__ import annotations
import argparse
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import scaffold as S  # 复用 emit 函数（module_json/agents_md/...）
from router import resolve, load
from harness import evaluate_module

ROOT = os.path.dirname(os.path.abspath(__file__))
REPOS_DIR = os.path.join(ROOT, "repos")


def _slugify(text: str) -> str:
    """想法 → 仓名 slug（通用描述性 kebab-case）。

    2026-10-12 用户决策：slug 优先通用描述性（利于 SEO/传播），
    MedXpert 品牌只留 README/描述/affiliation 披露——故不再加 medxpert- 前缀。
    """
    text = text.lower()
    text = re.sub(r"[^a-z0-9\u4e00-\u9fff]+", " ", text)
    # 简单中文→英文关键词映射（覆盖我们领域常见词）
    map_zh = {
        "骨科": "ortho", "植入": "implant", "器械": "device", "法规": "ra",
        "监管": "reg", "多语种": "multilingual", "翻译": "i18n", "标签": "label",
        "护照": "passport", "身份": "identity", "溯源": "provenance",
        "约束": "constraint", "运行时": "runtime", "治理": "governance",
        "验证": "validation", "公平": "fairness", "互操作": "interop",
        "登记": "registry", "映射": "map",
    }
    for zh, en in map_zh.items():
        text = text.replace(zh, " " + en + " ")
    toks = [t for t in re.findall(r"[a-z0-9]+", text) if len(t) > 1]
    slug = "-".join(toks[:4]) if toks else "auto-idea"
    return slug[:48]


def _extract_keywords(text: str) -> list[str]:
    toks = re.findall(r"[a-z0-9]+|[\u4e00-\u9fff]", text.lower())
    # 去掉停用词
    stop = {"的", "一个", "做", "想", "我", "你", "他", "给", "和", "与", "及", "是", "要", "a", "the", "to", "of", "for", "with"}
    return [t for t in toks if t not in stop and len(t) > 1][:12]


def generate_spec(idea: str) -> dict:
    slug = _slugify(idea)
    kws = _extract_keywords(idea)
    return {
        "id": slug,
        "title": idea[:60],
        "description": f"由想法自动生成的模块：{idea}",
        "keywords": kws,
        "file_patterns": [f"{slug.split('-')[-1]}.py"],
        "intents": kws[:5],
        "provides": [slug],
        "license": "CC0",
        "entry": "scripts/main.py",
        "features": ["（自动生成骨架，待填充实质内容）"],
        "extension_note": "新增能力在主体代码注册表加一行。",
        "usage": f"```bash\npython scripts/main.py --help\npython scripts/main.py --demo\n```",
        "extra": "auto-scaffolded",
        "related": [],
        "deps": [],
        "cost": "low",
        "lazy": True,
        "nested": True,
        "idea": idea,
        "layer": "AUTO",
    }


def _write_placeholder_entry(repo: str, entry: str):
    path = os.path.join(repo, entry)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(
            "#!/usr/bin/env python3\n"
            "# auto-scaffolded entry — 待填充实质逻辑\n"
            "import argparse, sys\n"
            "def main():\n"
            "    ap = argparse.ArgumentParser()\n"
            "    ap.add_argument('--demo', action='store_true')\n"
            "    a = ap.parse_args()\n"
            "    if a.demo:\n"
            "        print('[demo] 模块骨架就绪，待实现业务逻辑')\n"
            "    else:\n"
            "        ap.print_help()\n"
            "    return 0\n"
            "if __name__ == '__main__':\n"
            "    raise SystemExit(main())\n"
        )


def build(spec: dict) -> str:
    repo = os.path.join(REPOS_DIR, spec["id"])
    os.makedirs(os.path.join(repo, "plugins"), exist_ok=True)
    files = {
        "module.json": S.module_json(spec),
        "AGENTS.md": S.agents_md(spec),
        "CLAUDE.md": S.claude_md(spec),
        "llms.txt": S.llms_txt(spec),
        "README.md": S.readme_md(spec),
        # 2026-10-12 复审修复：新建仓原先漏 CONTRIBUTING.md（与 scaffold.py
        # 全量生成的仓不一致，新人到自动仓找不到参与指南）。
        "CONTRIBUTING.md": S.contributing_md(spec),
        "LICENSE": S.LICENSE_TEXTS.get(spec["license"], S.LICENSE_TEXTS["CC0"]),
        ".gitignore": S.gitignore(),
        "plugins/.gitkeep": S.gitkeep(spec.get("extension_note", "")),
    }
    for name, content in files.items():
        with open(os.path.join(repo, name), "w", encoding="utf-8") as f:
            f.write(content)
    _write_placeholder_entry(repo, spec["entry"])
    return repo


def main() -> int:
    ap = argparse.ArgumentParser(description="说想法即自动搭建")
    ap.add_argument("idea", help="自然语言想法")
    ap.add_argument("--no-harness", action="store_true", help="建完不跑 harness")
    args = ap.parse_args()

    idea = args.idea
    hits = resolve(idea)
    if hits:
        best = hits[0]
        print(f"[命中] 想法命中现有模块 → 复用 {best['module']['id']}")
        print(f"  匹配键：{best['matched']} · entry：{best['module']['entry']}")
        print(f"  建议：router.load('{best['module']['id']}') 后直接调用，无需新建。")
        return 0

    spec = generate_spec(idea)
    repo = build(spec)
    print(f"[新建] 已生成骨架 → {spec['id']}")
    print(f"  路径：{repo}")
    if not args.no_harness:
        res = evaluate_module(spec["id"])
        print(f"[自检] {spec['id']} — {'✅' if res['ok'] else '❌'} "
              f"({res.get('passed')}/{res.get('total')})")
        for dim, v in res.get("dimensions", {}).items():
            if not v["pass"]:
                print(f"  ❌ {dim}: {v['detail']}")
        # 2026-10-12 复审修复：自检失败必须返非 0（原恒返 0，
        # CI/调用方无法感知骨架质量不过关）。
        if not res["ok"]:
            print("[自检] 未过——骨架已生成但质量门禁未过，请按上方 ❌ 项修补。")
            return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
