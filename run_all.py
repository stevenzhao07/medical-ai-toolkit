#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run_all.py — 一键本地全跑（降低新人逐个 clone 的摩擦）
=====================================================
三种情形，三种**如实**的输出：

1. 开发态（./repos/ 存在）：逐个模块跑 --demo 汇总；加 --gold 追加 6 维 harness。
2. 独立克隆态（门户单仓，无 ./repos/）：跑**仓内自足冒烟**——门户自带的五个
   入口（路由 demo、四向一致、哈希台账、路由清单、扩展模块清单 schema）。
   它证明的是「这个仓自己装的东西是活的」，**不**声称 19 个尚未建仓的模块可跑。
3. `--full`：强制要求 ./repos/，缺失就明确 SKIP 并返回 0（不假绿）。

2026-11-27 变更缘由：外部匿名探针对本仓一直判 skip，因为默认分支只认 ./repos/。
但仓内确实有一整套可跑的自检；把「没有东西可跑」和「有东西但没跑」混为一谈，
外人看到的是一行 SKIP，等于这个仓在外人眼里什么都没验证过。

用法：
  python run_all.py            # 有 repos/ 跑全量 demo；没有则跑仓内自足冒烟
  python run_all.py --gold     # 开发态：冒烟 + 完整 6 维质量门禁（CI 同款）
  python run_all.py --full     # 强制全量；没有 repos/ 就 SKIP（不假绿）
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


def full_run(gold: bool) -> int:
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


def _module_schema() -> tuple[bool, str]:
    """扩展模块清单的 schema 断言（只判清单本身，不假装模块可跑）。"""
    try:
        import lifecycle_modules as L
    except Exception as exc:  # noqa
        return False, f"导入失败 {type(exc).__name__}: {exc}"
    mods = getattr(L, "MODULES", None)
    if not isinstance(mods, list) or not mods:
        return False, "MODULES 缺失或为空"
    ids = [m.get("id") for m in mods]
    need = ("id", "title", "layer", "license", "entry", "description")
    bad = [i for i, m in enumerate(mods) if any(k not in m for k in need)]
    if bad:
        return False, f"第 {bad[:3]} 项缺必填字段"
    if len(set(ids)) != len(ids):
        return False, "id 有重复"
    return True, f"{len(mods)} 项、字段齐、id 唯一"


def portal_run() -> int:
    """仓内自足冒烟：只跑本仓自带、且真的会断言的入口。"""
    checks = [
        ("路由 demo", [sys.executable, os.path.join(ROOT, "scripts", "discover.py"), "--demo"]),
        ("四向一致", [sys.executable, os.path.join(ROOT, "scripts", "check_portal.py")]),
        ("哈希台账", [sys.executable, os.path.join(ROOT, "scripts", "check_portal_sync.py")]),
        ("路由清单", [sys.executable, os.path.join(ROOT, "router.py"), "--list"]),
    ]
    print("MedXpert 门户单仓 · 仓内自足冒烟（不含未见仓模块）")
    print("=" * 56)
    ok = 0
    for name, cmd in checks:
        try:
            r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True,
                               encoding="utf-8", errors="replace", timeout=60)
            rc = r.returncode
            tail = [x.strip() for x in (r.stdout or "").splitlines() if x.strip()]
        except Exception as exc:  # noqa
            rc, tail = 1, [f"异常 {type(exc).__name__}: {exc}"]
        print(("  [ OK ] " if rc == 0 else "  [FAIL] ") + name +
              (f"  {tail[-1][:70]}" if tail else ""))
        ok += 1 if rc == 0 else 0
    good, why = _module_schema()
    print(("  [ OK ] " if good else "  [FAIL] ") + "扩展模块清单  " + why)
    ok += 1 if good else 0
    total = len(checks) + 1
    print("=" * 56)
    print(f"仓内自足冒烟 通过 {ok}/{total}；未覆盖：19 个扩展模块尚无独立公开仓")
    if "--full" in sys.argv:
        print("提示：--full 需要 ./repos/ 才跑全量，本仓独立克隆态没有该目录")
    return 0 if ok == total else 2


def main() -> int:
    gold = "--gold" in sys.argv or "--all" in sys.argv
    if os.path.isdir(REPOS):
        return full_run(gold)
    if "--full" in sys.argv or gold:
        print(f"[run_all] SKIP：{REPOS} 不存在（独立克隆态）。"
              "全量冒烟请在开发态 contrib/ 根运行。")
        return 0
    return portal_run()


if __name__ == "__main__":
    try:
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    raise SystemExit(main())
