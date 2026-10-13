#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
router.py — intent→module 自动路由（懒加载 + 嵌套 / 套娃）
=========================================================
MedXpert lgd-skeleton/1.0 的"大脑"：AI 拿到任务描述 → 匹配 module.json
→ 命中才加载该模块全文（progressive disclosure）→ 返回 entry + deps。

设计要点：
  - 初始化只扫 module.json 元数据（~20 token/模块），不载 README/SKILL 全文。
  - 命中后才 load() 全文（懒加载，省上下文/积分/提速）。
  - 支持嵌套：root 路由（medical-ai-toolkit）聚合子模块；needs_backends
    标记的模块（如 github-module）在涉及该后端时自动加载。
  - 靠 AGENTS.md "nearest wins + 子目录拼接" 实现套娃，无需 glue code。

用法：
  python router.py "我想做骨科IFU多语种对照"
  python router.py --list
  python router.py --load ai-a3-laws
  python router.py --needs github
"""
from __future__ import annotations
import argparse
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
REPOS_DIR = os.path.join(ROOT, "repos")
ROOT_ROUTER = os.path.join(ROOT, "repos", "medical-ai-toolkit", "skeleton.json")
# 门户独立克隆态回退：本仓根 skeleton.json（2026-10-12 复审修复，
# 原 REPOS_DIR 缺失时 router --list 空转，外界看来像"没有模块"）
SELF_ROUTER = os.path.join(ROOT, "skeleton.json")


def _iter_module_jsons():
    """渐进式披露：只扫 module.json 元数据，不读 README/SKILL。"""
    if os.path.isdir(REPOS_DIR):
        for name in sorted(os.listdir(REPOS_DIR)):
            mj = os.path.join(REPOS_DIR, name, "module.json")
            if os.path.isfile(mj):
                try:
                    with open(mj, encoding="utf-8") as f:
                        yield name, json.load(f)
                except Exception:
                    continue
        return
    # 回退：从 skeleton.json 读聚合路由表（字段映射到 module.json 形状）
    for sk in (ROOT_ROUTER, SELF_ROUTER):
        if os.path.isfile(sk):
            try:
                with open(sk, encoding="utf-8") as f:
                    m = json.load(f)
            except Exception:
                continue
            for mod in m.get("modules", []):
                mid = mod.get("id", "")
                if not mid:
                    continue
                yield mid, {
                    "id": mid,
                    "title": mod.get("title", ""),
                    "description": mod.get("description", ""),
                    # 2026-10-12 第四轮复审修复：skeleton.json 的模块项用顶层
                    # keywords/intents/file_patterns（无 triggers 嵌套；file_patterns 可缺），
                    # 必须映射回 module.json 的 triggers 形状，否则独立克隆态
                    # build_index 拿到空 triggers → 路由静默失效（resolve 永不命中）。
                    "triggers": {
                        "keywords": mod.get("keywords", []) or [],
                        "intents": mod.get("intents", []) or [],
                        "file_patterns": mod.get("file_patterns", []) or [],
                    },
                    "provides": mod.get("provides", []),
                    "needs_backends": mod.get("needs_backends", []),
                    "lazy": mod.get("lazy", True),
                    "nested": mod.get("nested", False),
                    "deps": mod.get("deps", []),
                    "entry": mod.get("entry", ""),
                }
            return


def _tokenize(text: str) -> list[str]:
    # 中英混合：拆词 + 单字 + 保留英文 token
    text = text.lower()
    toks = re.findall(r"[a-z0-9]+|[\u4e00-\u9fff]", text)
    return toks


def build_index():
    """构建 intent 索引：keyword/intent/file_pattern → module_id，带权重。"""
    index = []
    for mid, m in _iter_module_jsons():
        trig = m.get("triggers", {})
        keywords = trig.get("keywords", [])
        intents = trig.get("intents", [])
        patterns = trig.get("file_patterns", [])
        provides = m.get("provides", [])
        needs = m.get("needs_backends", [])
        # 权重：intent(3) > keyword(2) > provides(1) > pattern(1)
        weighted = {}
        for k in intents:
            weighted[k.lower()] = weighted.get(k.lower(), 0) + 3
        for k in keywords:
            weighted[k.lower()] = weighted.get(k.lower(), 0) + 2
        for k in provides:
            weighted[k.lower()] = weighted.get(k.lower(), 0) + 1
        for p in patterns:
            weighted[p.lower()] = weighted.get(p.lower(), 0) + 1
        index.append({
            "id": mid,
            "title": m.get("title", ""),
            "description": m.get("description", ""),
            "entry": m.get("entry", ""),
            "lazy": m.get("lazy", True),
            "nested": m.get("nested", False),
            "deps": m.get("deps", []),
            "needs_backends": needs,
            "weighted": weighted,
        })
    return index


def resolve(intent: str, index=None, top: int = 3):
    """按意图文本匹配模块，返回按得分排序的命中列表。"""
    index = index or build_index()
    toks = _tokenize(intent)
    hits = []
    for item in index:
        score = 0
        matched = []
        for tok in toks:
            for key, w in item["weighted"].items():
                if tok == key or tok in key or key in tok:
                    score += w
                    if key not in matched:
                        matched.append(key)
        if score > 0:
            hits.append((score, item, matched))
    hits.sort(key=lambda x: x[0], reverse=True)
    return [{"score": s, "module": it, "matched": mt} for s, it, mt in hits[:top]]


def load(module_id: str) -> dict:
    """懒加载：命中后才读该模块全文（README/AGENTS/SKILL 等）。"""
    repo = os.path.join(REPOS_DIR, module_id)
    out = {"id": module_id, "files": {}}
    for fn in ("module.json", "AGENTS.md", "CLAUDE.md", "llms.txt", "README.md"):
        p = os.path.join(repo, fn)
        if os.path.isfile(p):
            with open(p, encoding="utf-8") as f:
                out["files"][fn] = f.read()
    return out


def route(intent: str):
    """端到端：解析意图 → 返回最佳模块 + entry + 需要的后端骨架。"""
    hits = resolve(intent)
    if not hits:
        return {"matched": False, "intent": intent, "suggestion": "无命中，建议 idea_scaffold.py 新建模块"}
    best = hits[0]["module"]
    # 嵌套：若任务涉及后端（如 github），自动追加该后端模块
    needed = []
    text = intent.lower()
    for backend in ("github", "git", "web", "db", "cloud"):
        if backend in text:
            for item in build_index():
                if backend in [b.lower() for b in item["needs_backends"]]:
                    needed.append(item["id"])
    return {
        "matched": True,
        "intent": intent,
        "best": best["id"],
        "entry": best["entry"],
        "deps": best["deps"],
        "auto_load_backends": sorted(set(needed)),
        "all_hits": [h["module"]["id"] for h in hits],
        "matched_keys": hits[0]["matched"],
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="intent→module 自动路由（懒加载+嵌套）")
    ap.add_argument("intent", nargs="?", help="自然语言任务描述")
    ap.add_argument("--list", action="store_true", help="列出全部已纳管模块")
    ap.add_argument("--load", metavar="MODULE", help="懒加载某模块全文")
    ap.add_argument("--needs", metavar="BACKEND", help="列出需要某后端的模块（如 github）")
    args = ap.parse_args()

    if args.list:
        for it in build_index():
            print(f"  {it['id']:32s} nested={it['nested']!s:5} entry={it['entry']}")
        return 0
    if args.load:
        data = load(args.load)
        # 2026-10-12 复审修复：原 [:4000] 硬截断会产出非法 JSON（下游解析崩），
        # 改为完整输出 + 超长时按文件截断并附标记（每文件内部仍完整）。
        out = json.dumps(data, ensure_ascii=False, indent=2)
        if len(out) > 20000:
            trimmed = {"id": data["id"], "files": {}, "_truncated": True}
            for fn, content in data["files"].items():
                trimmed["files"][fn] = content if len(content) <= 4000 else content[:4000] + "\n…[截断]"
            out = json.dumps(trimmed, ensure_ascii=False, indent=2)
        print(out)
        return 0
    if args.needs:
        for it in build_index():
            if args.needs.lower() in [b.lower() for b in it["needs_backends"]]:
                print(f"  {it['id']}  (needs_backends={it['needs_backends']})")
        return 0
    if not args.intent:
        ap.print_help()
        return 1
    print(json.dumps(route(args.intent), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
