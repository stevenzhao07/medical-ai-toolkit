#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
harness.py — 全自动化测试 Harness（6 维度）
==========================================
每个模块建仓/改动后自动跑，作 CI 质量门禁。

6 维度：
  适配性 fit        module.json schema 合法、triggers/provides 非空
  准确性 accuracy   entry --demo 输出非空且含该模块关键字段（KEY_FIELDS）
  流畅性 fluency    entry --help 不崩、退出码正常、无死锁
  外人实跑 outsider 从干净视角跑通 README 用法段全部可跑命令（非仅第一条），
                   带 <占位符> 或缺输入文件的命令明确跳过并记录，不假跑
  易用性 usability  README 有用法段（中英标题均认）、entry 文件存在、有 CTA
  语义回归 gold     跑 gold_set.json 每条真实任务，校验 expect 子串 / regex / not_contains

布局说明（2026-10-12 三方复审 P0 修复）：
  开发态（contrib/）：21 仓平级位于 ./repos/，harness 在此跑 --all。
  独立克隆态（门户单仓）：无 repos/ 目录，--all 明确 SKIP（返回 0 + 提示），
  不崩溃也不假绿；门户单仓 CI 改用 scripts/discover.py --demo 路由冒烟。
  --module 双布局回退：repos/<id> 不存在时，若 <id> 即本仓（门户自测）则测仓根。

gold 金规（2026-10-12 复审修复）：
  1. expect_rc 缺省 = [0]——每条任务都校验退出码，不因缺字段免检；
  2. setup 判负——setup 命令失败即该任务失败（rc=125），不许未准备态假绿；
  3. 124（超时）不缓存——超时是环境态，不记忆化，避免连带任务假失败；
  4. 拒绝真空通过——gold_set.json 缺失 或 某模块无 gold 任务 → 硬性判负，
     杜绝「gold 维度恒真」的假绿（第四轮复审修复）。
  5. 清理兜底——任务 cleanup 失败绝不终止门禁判定。受限/沙箱环境（如
     safe-delete 守卫）可能在删除时抛 BaseException（SystemExit 等），故
     _cleanup 兜 `except BaseException`；残留文件由 .gitignore 兜
     （第四轮终验修复：此前本机曾因此 rc=1 且报告写不出）。

用法：
  python harness.py --all
  python harness.py --module ai-a3-laws
  python harness.py --report report.md
"""
from __future__ import annotations
import argparse
import json
import os
import re
import shutil
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
REPOS_DIR = os.path.join(ROOT, "repos")
GOLD_PATH = os.path.join(ROOT, "gold_set.json")
SELF_ID = os.path.basename(ROOT)


def load_gold_set() -> dict:
    if not os.path.isfile(GOLD_PATH):
        return {}
    with open(GOLD_PATH, encoding="utf-8") as f:
        return json.load(f)


# 每模块 --demo 必须命中的关键字段（正则）。用于 accuracy 维度增强（不只判非空）。
KEY_FIELDS = {
    "ai-a3-laws": [r"A[123]", r"\[PASS\]", r"\[BLOCK\]"],
    "ai-governance-checklist": [r"model-card", r"human-oversight", r"fairness"],
    "ai-model-passport": [r'"hash":\s*"[0-9a-f]{64}"', r"risk_class"],
    "delivery-guard": [r"dual_fingerprint", r"license_present"],
    "fhir-ortho-toolkit": [r"udiCarrier", r"nmpa-udi"],
    "medical-ai-toolkit": [r"lgd-skeleton/1\.0", r"ai-a3-laws"],
    "ml-validation-toolkit": [r"auc", r"人口均等等差"],
    "multilingual-ifu": [r"产品标识", r"支持语种"],
    "omop-ortho-toolkit": [r"CPT4", r"TO_BE_VALIDATED"],
    "samd-ra-toolkit": [r"MDCG", r"AI Office", r"内部统一风险刻度"],
}


# README「用法段」标题识别（二/三级标题，中英双语）。
# 2026-10-13：门户 README 按用户要求改为「英文在前、中文在后」双语版后，
# 标题从 `## 使用` 变成 `### Quick start` / `### 快速开始`，原字面量匹配
# `"## 使用"` 直接判负 —— CI 精确抓到该回归。此处放宽为双语通用标题，
# 但「必须真的存在可跑用法段」这一语义不放宽。
USAGE_RE = re.compile(
    r"^#{2,3}[ \t]*(?:使用|用法|快速开始|快速上手|上手|"
    r"Usage|Quick[ \t]*[Ss]tart|Getting[ \t]*[Ss]tarted|Quickstart)[ \t]*$",
    re.M | re.I,
)


def _resolve_repo(mid: str) -> str | None:
    """双布局回退：repos/<id> → 仓根本身（门户自测）→ None。"""
    cand = os.path.join(REPOS_DIR, mid)
    if os.path.isfile(os.path.join(cand, "module.json")):
        return cand
    if mid == SELF_ID and os.path.isfile(os.path.join(ROOT, "module.json")):
        return ROOT
    return None


def _find_entry(repo: str, mj: dict) -> str | None:
    entry = mj.get("entry", "")
    if entry and os.path.isfile(os.path.join(repo, entry)):
        return entry
    # fallback：扫描 scripts/*.py（跳过 _ 前缀的私有/生成辅助脚本，
    # 如 gold setup 用的 scripts/_mk_gold_*.py，避免误当成入口）
    sp = os.path.join(repo, "scripts")
    if os.path.isdir(sp):
        for f in sorted(os.listdir(sp)):
            if f.endswith(".py") and not f.startswith("_"):
                return os.path.join("scripts", f)
    return None


def _run(cmd_tail: list[str], repo: str, timeout: int = 60):
    env = dict(os.environ)
    env.setdefault("PYTHONIOENCODING", "utf-8")  # Windows 控制台 GBK 兜底
    try:
        r = subprocess.run(
            [sys.executable, *cmd_tail], cwd=repo,
            capture_output=True, text=True,
            encoding="utf-8", errors="replace", timeout=timeout,
            env=env,
        )
        return r.returncode, r.stdout, r.stderr
    except subprocess.TimeoutExpired:
        return 124, "", "TIMEOUT"
    except Exception as e:  # noqa
        return 1, "", str(e)


def _third_party_imports(path: str | None) -> set[str] | None:
    """AST 解析 entry：返回非标准库、非同目录本地模块的顶层 import 集合。

    解析失败返回 None（语法问题另由交付门禁/语法检查负责，此处不重复判负）。
    （2026-10-13 残余 P2：fit 维度此前不看 deps，与 entry 实际依赖脱节。）
    """
    if not path or not os.path.isfile(path):
        return None
    import ast
    try:
        with open(path, encoding="utf-8") as f:
            tree = ast.parse(f.read())
    except Exception:
        return None
    std = set(getattr(sys, "stdlib_module_names", ()))
    here = os.path.dirname(path)
    mods: set[str] = set()
    for n in ast.walk(tree):
        if isinstance(n, ast.Import):
            for a in n.names:
                mods.add(a.name.split(".")[0])
        elif isinstance(n, ast.ImportFrom):
            if n.level == 0 and n.module:
                mods.add(n.module.split(".")[0])
    return {m for m in mods
            if m not in std and m != "__future__"
            and not os.path.isfile(os.path.join(here, m + ".py"))}


def check_fit(mj: dict, repo: str = "", entry: str | None = None) -> tuple[bool, str]:
    """适配性：schema 合法 + 关键字段非空 + deps 与 entry 实际第三方依赖一致。"""
    errs = []
    notes = []
    for f in ("id", "title", "description", "triggers", "provides"):
        if not mj.get(f):
            errs.append(f"缺字段 {f}")
    trig = mj.get("triggers", {}) or {}
    if not (trig.get("keywords") or trig.get("intents")):
        errs.append("triggers 空（AI 无法路由）")
    if not mj.get("provides"):
        errs.append("provides 空")

    # deps 解析（残余 P2）：类型 + 与 entry 实际第三方 import 的一致性
    deps = mj.get("deps", [])
    if not isinstance(deps, list):
        errs.append("deps 须为列表")
        deps = []
    nonstr = [d for d in deps if not isinstance(d, str)]
    if nonstr:
        errs.append(f"deps 含非字符串项 {nonstr[:3]}")
    third = _third_party_imports(os.path.join(repo, entry)) if (repo and entry) else None
    if third is not None:
        if third and not deps:
            errs.append(f"entry 依赖第三方 {sorted(third)} 但 deps 为空（自相矛盾）")
        elif deps and not third:
            notes.append(f"声明 deps={deps} 但 entry 未见第三方 import（疑为可选依赖）")
        elif not third:
            notes.append("零依赖（仅标准库）")
    detail = "; ".join(errs) if errs else ("OK" + ("；" + "；".join(notes) if notes else ""))
    return (not errs), detail


def check_accuracy(repo: str, entry: str | None) -> tuple[bool, str]:
    """准确性：--demo 输出非空 + 命中该模块关键字段（KEY_FIELDS）。"""
    if not entry:
        return False, "无 entry"
    code, out, err = _run([entry, "--demo"], repo)
    if code != 0:
        return False, f"--demo 退出码 {code}: {err[:200]}"
    if not out.strip():
        return False, "--demo 输出为空"
    mid = os.path.basename(repo)
    missing = [k for k in KEY_FIELDS.get(mid, []) if not re.search(k, out)]
    if missing:
        return False, f"缺关键字段 {missing}"
    return True, f"输出 {len(out)} 字符 · 关键字段齐"


def _cleanup(repo: str, paths: list[str]) -> None:
    for cp in paths or []:
        p = os.path.join(repo, cp)
        try:
            if os.path.isdir(p):
                shutil.rmtree(p, ignore_errors=True)
            elif os.path.isfile(p):
                os.remove(p)
        except BaseException:
            # 兜底任意异常（含沙箱 safe-delete 守卫可能抛的 SystemExit/自定义异常）：
            # 受限环境下「清理失败」绝不允许终止门禁判定；残留文件由 .gitignore 兜底。
            pass


def check_gold(repo: str, mid: str) -> tuple[bool, str]:
    """语义回归：跑 gold_set.json 中该模块全部任务。

    按 (cmd, setup) 去重缓存输出——多数任务共享同一命令（如 --demo）只跑一次，
    显著减少子进程 spawn（CI 友好）。setup/cleanup 仍按任务执行。
    超时（124）不缓存；setup 失败以 rc=125 判负。
    """
    if not os.path.isfile(GOLD_PATH):
        return False, "gold_set.json 缺失（语义回归维度无法验证，硬性判负）"
    m = load_gold_set().get("modules", {}).get(mid)
    if not m or not m.get("tasks"):
        return False, f"模块 {mid} 无 gold 任务（硬性非空，拒真空通过）"
    tasks = m["tasks"]
    cache: dict[tuple, tuple] = {}

    def output(task: dict) -> tuple[int, str, str]:
        key = (tuple(task["cmd"]), tuple(tuple(sc) for sc in task.get("setup_cmds", [])))
        if key not in cache:
            for sc in task.get("setup_cmds", []):
                sc_code, _, sc_err = _run(sc, repo)
                if sc_code != 0:
                    # 金规 2：setup 失败 = 任务失败（125 区别于命令自身 rc）
                    return 125, "", f"SETUP 失败 [{sc}]: {sc_err[:200]}"
            code, out, err = _run(task["cmd"], repo)
            if code != 124:  # 金规 3：超时不缓存
                cache[key] = (code, out, err)
            return code, out, err
        return cache[key]

    fails = []
    for t in tasks:
        tid = t.get("id", "?")
        code, out, err = output(t)
        text = (out or "") + "\n" + (err or "")
        _cleanup(repo, t.get("cleanup", []))
        if code == 125:
            fails.append(f"{tid}: {err}")
            continue
        expected_rc = t.get("expect_rc", [0])  # 金规 1：缺省即 [0]
        if code not in expected_rc:
            fails.append(f"{tid}: rc={code}∉{expected_rc}")
            continue
        miss = [e for e in t.get("expect", []) if e not in text]
        if miss:
            fails.append(f"{tid}: 缺子串 {miss}")
            continue
        if any(not re.search(rx, text) for rx in t.get("regex", [])):
            fails.append(f"{tid}: regex 未中 {t.get('regex')}")
            continue
        bad = [s for s in t.get("not_contains", []) if s in text]
        if bad:
            fails.append(f"{tid}: 出现禁含 {bad}")
    if fails:
        return False, f"{len(tasks)-len(fails)}/{len(tasks)} 通过; 失败: " + "; ".join(fails[:6])
    return True, f"{len(tasks)}/{len(tasks)} 通过"


def check_fluency(repo: str, entry: str | None) -> tuple[bool, str]:
    """流畅性：--help 不崩、退出码正常。"""
    if not entry:
        return False, "无 entry"
    code, out, err = _run([entry, "--help"], repo)
    if code not in (0, 2):  # argparse --help 常返回 0 或 2
        return False, f"--help 异常退出 {code}: {err[:200]}"
    return True, "help 正常"


def _snapshot(repo: str) -> dict:
    """沙箱快照：记录仓内文件相对路径+大小，检测外人命令副作用。"""
    snap = {}
    for dirpath, dirnames, filenames in os.walk(repo):
        dirnames[:] = [d for d in dirnames if d not in (".git", "__pycache__")]
        for fn in filenames:
            p = os.path.join(dirpath, fn)
            try:
                snap[os.path.relpath(p, repo)] = os.path.getsize(p)
            except OSError:
                pass
    return snap


def _missing_input_files(tail: list[str], repo: str) -> list[str]:
    """识别引用了仓内不存在输入文件的参数（--out 之类输出目标除外）。"""
    missing = []
    for i, a in enumerate(tail):
        if a.startswith("--") or a.startswith("-"):
            continue
        prev = tail[i - 1] if i else ""
        if prev == "--out":
            continue  # 输出目标，允许不存在
        if re.search(r"\.(json|csv|sql|txt|tsv|xlsx?|md)$", a, re.I):
            if not os.path.isfile(os.path.join(repo, a)):
                missing.append(a)
    return missing


def _strip_trailing_comment(cmd: str) -> str:
    """剥离命令行尾的 `#` 注释（README 常见写法），引号内的 # 原样保留。

    2026-10-13：门户 README 的用法段写作
    `python harness.py --module medical-ai-toolkit   # run the 6-dimension self-test`，
    原样传给 subprocess 会把 `run the 6-dimension self-test` 当成参数 → rc=2。
    这种写法在 bash/PowerShell 里都合法，是解析方的错，不是 README 的错。
    """
    out: list[str] = []
    quote = None
    for i, ch in enumerate(cmd):
        if quote:
            if ch == quote:
                quote = None
            out.append(ch)
        elif ch in "\"'":
            quote = ch
            out.append(ch)
        elif ch == "#" and (i == 0 or cmd[i - 1].isspace()):
            break
        else:
            out.append(ch)
    return "".join(out).strip()


def _usage_sections(readme: str) -> list[str]:
    """取出 README 全部「用法段」正文（中英标题均认）。

    双语 README 会同时有英文与中文用法段，故返回全部，由调用方取第一个
    真正含可跑命令的段。截断只认 >=2 级标题（`##` / `###`）——
    代码块里的 `# 注释` 若被当成标题，会把 python 命令切到段外。
    """
    secs = []
    for m in USAGE_RE.finditer(readme):
        rest = readme[m.end():]
        nxt = re.search(r"^#{2,3}[ \t]", rest, re.M)
        secs.append(rest[: nxt.start()] if nxt else rest)
    return secs


def check_outsider(repo: str, readme: str) -> tuple[bool, str]:
    """外人实跑：README 用法段全部可跑命令 smoke 跑通（2026-10-12 修复：
    原先只跑第一条，其余命令坏了也不知道）。带 <占位符> 或缺输入文件的
    命令明确跳过并记入 detail；跑前跑后做沙箱快照，报告副作用文件。"""
    sections = _usage_sections(readme)
    if not sections:
        return False, "README 无用法段（外人不知怎么跑）"
    cmds: list[str] = []
    for s in sections:
        found = [_strip_trailing_comment(c)
                 for c in re.findall(r"python\s+([^\n`]+)", s)]
        found = [c for c in found if c]
        if found:
            cmds = found
            break
    if not cmds:
        return False, "用法段无 python 命令"
    import shlex
    before = _snapshot(repo)
    ran, failed, skipped = 0, [], []
    for c in cmds:
        c = c.strip().strip("`")
        if "--demo" in c or "--help" in c:
            continue
        # 防递归：README 里「跑 harness 自己」的命令已由 CI 第一步直接覆盖，
        # 在 outsider 里再执行会自我递归（子 harness 又跑自己的 outsider）。
        if "harness.py" in c:
            skipped.append(f"{c[:40]}(自测命令，避免递归)")
            continue
        try:
            tail = shlex.split(c)  # 正确处理带引号参数（P2-11 修复）
        except ValueError:
            tail = c.split()
        if tail and tail[0] in ("python", "python3"):
            tail = tail[1:]
        if "<" in c and ">" in c:
            skipped.append(f"{c[:40]}(占位符)")
            continue
        miss = _missing_input_files(tail, repo)
        if miss:
            skipped.append(f"{c[:40]}(缺文件 {miss[0]})")
            continue
        code, _, err = _run(tail, repo)
        ran += 1
        if code != 0:
            failed.append(f"[{c[:50]}] rc={code}: {err[:120]}")
    after = _snapshot(repo)
    side = sorted(set(after) - set(before))
    changed = sorted(p for p in set(before) & set(after) if before[p] != after[p])
    note = ""
    if side or changed:
        note = f" · 副作用(需清理或 .gitignore): 新增{side[:4]} 变更{changed[:4]}"
    skip_note = f" · 跳过 {len(skipped)} 条（占位/缺文件）" if skipped else ""
    if failed:
        return False, f"外人命令失败 {len(failed)}/{ran}: " + " | ".join(failed[:3]) + note + skip_note
    if ran == 0:
        return True, "使用段仅 demo/help/占位（已被准确性/流畅性覆盖）" + note + skip_note
    return True, f"外人命令 {ran}/{ran} 可跑通" + note + skip_note


def check_usability(repo: str, readme: str, entry: str | None) -> tuple[bool, str]:
    """易用性：README 有用法段 + entry 存在 + 有 CTA。"""
    errs = []
    if not USAGE_RE.search(readme):
        errs.append("无用法段")
    if not entry:
        errs.append("无 entry 文件")
    if not re.search(r"(fork|clone|提\s*issue|demo)", readme, re.I):
        errs.append("无 CTA")
    return (not errs), ("; ".join(errs) or "OK")


def evaluate_module(mid: str) -> dict:
    repo = _resolve_repo(mid)
    if not repo:
        return {"id": mid, "ok": False, "error": f"无 module.json（{REPOS_DIR}/{mid} 不存在，且非本仓自测）"}
    mj_path = os.path.join(repo, "module.json")
    with open(mj_path, encoding="utf-8") as f:
        mj = json.load(f)
    entry = _find_entry(repo, mj)
    readme_path = os.path.join(repo, "README.md")
    readme = open(readme_path, encoding="utf-8").read() if os.path.isfile(readme_path) else ""

    dims = {
        "适配性 fit": check_fit(mj, repo, entry),
        "准确性 accuracy": check_accuracy(repo, entry),
        "流畅性 fluency": check_fluency(repo, entry),
        "外人实跑 outsider": check_outsider(repo, readme),
        "易用性 usability": check_usability(repo, readme, entry),
        "语义回归 gold": check_gold(repo, mid),
    }
    passed = sum(1 for ok, _ in dims.values() if ok)
    return {
        "id": mid,
        "ok": passed == len(dims),
        "passed": passed,
        "total": len(dims),
        "dimensions": {k: {"pass": ok, "detail": d} for k, (ok, d) in dims.items()},
    }


def _main() -> int:
    ap = argparse.ArgumentParser(description="6 维度自动测试 Harness（含 gold 语义回归）")
    ap.add_argument("--all", action="store_true", help="测全部模块")
    ap.add_argument("--module", metavar="ID", help="测单个模块")
    ap.add_argument("--report", metavar="PATH", default="harness_report.md", help="报告输出路径")
    args = ap.parse_args()

    targets = []
    if args.module:
        if not _resolve_repo(args.module):
            print(f"[harness] 模块 {args.module} 不在 {REPOS_DIR}（且非本仓自测）",
                  file=sys.stderr)
            return 2
        targets = [args.module]
    elif args.all:
        if not os.path.isdir(REPOS_DIR):
            # 门户独立克隆态：无嵌套 repos/。明确 SKIP，不崩溃也不假绿。
            print(f"[harness] SKIP：{REPOS_DIR} 不存在（独立克隆态）。"
                  "门户单仓 CI 请用 scripts/discover.py --demo 路由冒烟；"
                  "全量测试请在开发态 contrib/ 根运行 --all。")
            return 0
        targets = [d for d in sorted(os.listdir(REPOS_DIR))
                   if os.path.isfile(os.path.join(REPOS_DIR, d, "module.json"))]
    else:
        ap.print_help()
        return 1

    results = [evaluate_module(t) for t in targets]
    ok = sum(1 for r in results if r["ok"])

    # 报告
    lines = ["# Harness 报告（6 维度，含 gold 语义回归）", "",
             f"通过 {ok}/{len(results)} 模块", ""]
    for r in results:
        lines.append(f"## {r['id']} — {'✅' if r['ok'] else '❌'} ({r.get('passed','?')}/{r.get('total','?')})")
        if "error" in r:
            lines.append(f"- 错误：{r['error']}")
        else:
            for dim, v in r["dimensions"].items():
                lines.append(f"- {dim}: {'✅' if v['pass'] else '❌'} — {v['detail']}")
        lines.append("")
    report_path = os.path.join(ROOT, args.report)
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"通过 {ok}/{len(results)} · 报告 → {report_path}")
    # 质量门禁：任一不过则返回非 0（CI 不让合）
    return 0 if ok == len(results) else 2


def main() -> int:
    try:
        return _main()
    except Exception as e:  # noqa：兜底，避免 CI 里裸 traceback
        print(f"[harness] 内部错误: {type(e).__name__}: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    try:
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8")
            sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass
    raise SystemExit(main())
