#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_portal.py — 门户生成物自洽检查（零依赖）

校验 manifest.py 生成的多份清单互相一致：
  skeleton.json（总路由表）· .well-known/agent-card.json（A2A）·
  teamai.manifest.json（TeamAI 适配）· llms.txt（根索引）
不一致即返回非 0，供 CI 门禁拦截"陈旧/漏项"的生成物。
"""
from __future__ import annotations
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))


def _read(p):
    with open(os.path.join(ROOT, p), encoding="utf-8") as f:
        return f.read()


def main() -> int:
    errs = []
    sk = json.loads(_read("skeleton.json"))
    ids = [m.get("id", "") for m in sk.get("modules", [])]
    routing = sk.get("routing", {}) or {}
    if sk.get("count") != len(ids):
        errs.append(f"skeleton.count={sk.get('count')} != modules={len(ids)}")
    if len(ids) != len(routing):
        errs.append(f"skeleton modules={len(ids)} != routing={len(routing)}")
    if len(set(ids)) != len(ids):
        errs.append("skeleton modules 存在重复 id")
    if any(not i for i in ids):
        errs.append("skeleton modules 存在空 id")

    card = json.loads(_read(".well-known/agent-card.json"))
    card_ids = {s.get("id", "") for s in card.get("skills", [])}
    if card_ids != set(ids):
        errs.append(f"agent-card skills({len(card_ids)}) 与 skeleton({len(ids)}) 不一致")

    tm = json.loads(_read("teamai.manifest.json"))
    tm_ids = set(((tm.get("mapping", {}) or {}).get("skills", {}) or {}).keys())
    if tm_ids != set(ids):
        errs.append(f"teamai.manifest skills({len(tm_ids)}) 与 skeleton({len(ids)}) 不一致")

    miss = [i for i in ids if not os.path.isfile(
        os.path.join(ROOT, "teamai", "skills", i, "SKILL.md"))]
    if miss:
        errs.append(f"缺 teamai skills 文件 {len(miss)} 个: {miss[:5]}")

    llms = _read("llms.txt")
    not_in = [i for i in ids if i not in llms]
    if not_in:
        errs.append(f"llms.txt 未列模块 {len(not_in)} 个: {not_in[:5]}")

    if errs:
        print("[check_portal] FAIL")
        for e in errs:
            print("  - " + e)
        return 2
    print(f"[check_portal] OK — {len(ids)} 模块，skeleton/agent-card/teamai/llms 四向一致")
    return 0


if __name__ == "__main__":
    try:
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    raise SystemExit(main())
