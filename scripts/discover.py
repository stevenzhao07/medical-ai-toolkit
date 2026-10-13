#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
discover.py — medical-ai-toolkit 路由发现
=============================================
发现 lgd-skeleton/1.0 的全部可插拔模块并输出路由表。
优先读取根门户总路由表 skeleton.json（独立克隆也能用），
回退到本地 repos/ 扫描（开发态）。零依赖（仅 Python 3.8+ 标准库）。
"""
from __future__ import annotations
import sys
import argparse
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(HERE, ".."))
REPOS = os.path.abspath(os.path.join(HERE, "..", ".."))
SELF_ID = "medical-ai-toolkit"


def _from_skeleton() -> list[dict]:
    sk = os.path.join(REPO_ROOT, "skeleton.json")
    if not os.path.isfile(sk):
        return []
    with open(sk, encoding="utf-8") as f:
        m = json.load(f)
    rows = []
    for mod in m.get("modules", []):
        if mod.get("id") == SELF_ID:
            continue
        rows.append({
            "id": mod.get("id", ""),
            "entry": mod.get("entry", ""),
            "license": mod.get("license", ""),
            "url": mod.get("url", ""),
            "provides": mod.get("provides", []),
        })
    return rows


def _from_repos() -> list[dict]:
    rows = []
    if not os.path.isdir(REPOS):
        return rows
    for name in sorted(os.listdir(REPOS)):
        mj = os.path.join(REPOS, name, "module.json")
        if name == SELF_ID or not os.path.isfile(mj):
            continue
        with open(mj, encoding="utf-8") as f:
            m = json.load(f)
        rows.append({
            "id": m.get("id", name),
            "entry": m.get("entry", ""),
            "license": m.get("license", ""),
            "url": f"https://github.com/stevenzhao07/{m.get('id', name)}",
            "provides": m.get("provides", []),
        })
    return rows


def discover() -> list[dict]:
    rows = _from_skeleton()
    if not rows:
        rows = _from_repos()
    return rows


def main() -> int:
    ap = argparse.ArgumentParser(description="MedXpert 医疗 AI 可插拔模块路由发现")
    ap.add_argument("--demo", action="store_true", help="打印路由表（演示）")
    ap.add_argument("--json", action="store_true", help="JSON 输出")
    args = ap.parse_args()

    rows = discover()
    if args.json:
        print(json.dumps(rows, ensure_ascii=False, indent=2))
    else:
        print(f"# MedXpert 医疗 AI 可插拔模块路由表（{len(rows)} 个）\n")
        for r in rows:
            url = r.get("url") or f"https://github.com/stevenzhao07/{r['id']}"
            print(f"- [{r['id']}]({url})  ·  {r.get('entry','')}  ·  {r.get('license','')}")
        print("\n总入口: medical-ai-toolkit（lgd-skeleton/1.0）")
    return 0


if __name__ == "__main__":
    try:
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8")
            sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass
    raise SystemExit(main())
