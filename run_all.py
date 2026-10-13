#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run_all.py — 一键本地全跑（降低新人逐个 clone 的摩擦）
=====================================================
默认遍历 repos/*/ 跑每个模块的 --demo 并汇总；
加 --gold 追加跑完整 6 维 harness（含 gold_set.json 语义回归，条数以 gold_set.json 为准）。

布局说明（2026-10-12 复审修复）：开发态（contrib/）21 仓平级位于 ./repos/；
独立克隆态（门户单仓）无 repos/ 时明确 SKIP（返回 0 + 提示），不崩溃不假绿。

用法：
  python run_all.py            # 只跑各模块 --demo，快速冒烟
  python run_all.py --gold     # 冒烟 + 完整 6 维质量门禁（CI 同款）
"""
from __future__ import annotations
import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
REPOS = os.path.join(ROOT, "repos")


def find_entry(repo: str) -> str | None:
    mj = os.path.join(repo, "module.json")
    if os.path.isfile(mj):
        try:
            e = json.load(open(mj, encoding="utf-8")).get("entry", "")
            if e and os.path.isfile(os.path.join(repo, e)):
                return e
        except Exception:
            pass
    sp = os.path.join(repo, "scripts")
    if os.path.isdir(sp):
        for f in sorted(os.listdir(sp)):
            if f.endswith(".py") and not f.startswith("_"):
                return os.path.join("scripts", f)
    return None


def main() -> int:
    gold = "--gold" in sys.argv or "--all" in sys.argv
    if not os.path.isdir(REPOS):
        print(f"[run_all] SKIP：{REPOS} 不存在（独立克隆态）。"
              "全量冒烟请在开发态 contrib/ 根运行；门户单仓请用 "
              "scripts/discover.py --demo 路由冒烟。")
        return 0
    mods = [d for d in sorted(os.listdir(REPOS))
            if os.path.isfile(os.path.join(REPOS, d, "module.json"))]
    print(f"MedXpert 医疗 AI 开源矩阵 · {len(mods)} 模块本地全跑")
    print("=" * 56)
    ok = 0
    for m in mods:
        repo = os.path.join(REPOS, m)
        entry = find_entry(repo)
        if not entry:
            print(f"[skip] {m}  无 entry")
            continue
        try:
            r = subprocess.run([sys.executable, entry, "--demo"], cwd=repo,
                               capture_output=True, text=True,
                               encoding="utf-8", errors="replace", timeout=60)
            rc = r.returncode
            n = len(r.stdout or "")
        except Exception as exc:  # noqa
            rc, n = 1, 0
            print(f"[FAIL] {m}  异常 {exc}")
            continue
        if rc == 0:
            ok += 1
            print(f"[ OK ] {m}  ({entry} --demo, {n} chars)")
        else:
            print(f"[FAIL] {m}  ({entry} --demo, rc={rc})")
    print("=" * 56)
    print(f"demo 通过 {ok}/{len(mods)}")
    if gold:
        print("\n跑完整 6 维 harness（含 gold 语义回归）...")
        rc = subprocess.run([sys.executable, os.path.join(ROOT, "harness.py"), "--all"]).returncode
        print(f"harness EXIT={rc}（0=全过，2=有失败）")
        return rc
    print("\n提示：加 --gold 跑完整 6 维质量门禁（CI 同款，含 gold 语义回归）")
    return 0 if ok == len(mods) else 2


if __name__ == "__main__":
    try:
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    raise SystemExit(main())
