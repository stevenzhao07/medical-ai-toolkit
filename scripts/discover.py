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
    ap.add_argument("--selftest", action="store_true", help="跑内置自测（断言 + 负对照 + xfail）")
    ap.add_argument("--json", action="store_true", help="JSON 输出")
    args = ap.parse_args()
    if getattr(args, "selftest", False):
        return _selftest()

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


# ==================== 内置自测（--selftest） ====================
# 由 conformance 补丁于 2026-10-14 生成（生成器 v2）。
# 特性：端到端 CLI 调用 + 内容断言 + 负对照 + xfail（已知缺陷显式标注，不掩盖）。
_SELFTEST_CASES = [(['--demo'], 0, [], [], None), (['--demo', '--json'], 0, [], [], None)]


def _selftest() -> int:
    import os as _os
    import subprocess as _sp
    _here = _os.path.dirname(_os.path.abspath(__file__))
    # 仓库根：脚本位于 <repo>/scripts/ 时取上一级；否则取脚本所在目录
    _root = _os.path.dirname(_here) if _os.path.basename(_here) == "scripts" else _here
    _script = _os.path.abspath(__file__)
    _fail, _xfail, _n = [], [], 0
    for _case in _SELFTEST_CASES:
        _args, _rc, _must, _mustnot = _case[0], _case[1], _case[2], _case[3]
        _reason = _case[4] if len(_case) > 4 else None
        _n += 1
        _p = _sp.run([sys.executable, _script] + _args, capture_output=True, cwd=_root)
        _out = _p.stdout.decode("utf-8", "replace")
        _bad = []
        if _p.returncode != _rc:
            _bad.append(f"rc={_p.returncode} 期望 {_rc}")
        for _m in _must:
            if _m not in _out:
                _bad.append(f"输出缺少 {_m!r}")
        for _m in _mustnot:
            if _m in _out:
                _bad.append(f"输出含禁止内容 {_m!r}")
        if _rc == 0 and not _out.strip():
            _bad.append("rc=0 但输出为空（假绿）")
        if _bad:
            if _reason:
                _xfail.append(f"xfail args={_args}：{'；'.join(_bad)} ← 已知缺陷：{_reason}")
            else:
                _fail.append(f"args={_args}：{'；'.join(_bad)}")
    # 通用负对照：未知参数必须非零
    _n += 1
    _p = _sp.run([sys.executable, _script, "--__nonexistent_flag__"], capture_output=True, cwd=_root)
    if _p.returncode == 0:
        _fail.append("负对照失败：未知参数竟返回 0")
    for _x in _xfail:
        print("[selftest][xfail] " + _x)
    if _fail:
        print(f"[selftest] FAILED {len(_fail)}/{_n}")
        for _f in _fail:
            print("  - " + _f)
        return 1
    print(f"[selftest] PASS {_n - len(_xfail)}/{_n}（含负对照；xfail {len(_xfail)} 项为已知缺陷）")
    return 0


if __name__ == "__main__":
    try:
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8")
            sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass
    raise SystemExit(main())
