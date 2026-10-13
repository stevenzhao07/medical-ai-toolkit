#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_portal_sync.py — 门户副本哈希校验（零依赖）

manifest.py 生成 _portal_sync.json，记录各门户文件（工具副本 + 生成物）的
SHA256。本脚本在门户独立克隆态校验「文件当前哈希 == 记录哈希」，捕获：
  - 门户内文件被手工编辑 / 传输损坏 / 编码变化
  - 重跑 manifest 后漏同步
不一致即返回非 0，供 CI 门禁拦截。
"""
from __future__ import annotations
import hashlib
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))


def _sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    rec_path = os.path.join(ROOT, "_portal_sync.json")
    if not os.path.isfile(rec_path):
        print("[check_portal_sync] FAIL：_portal_sync.json 缺失（先跑 manifest.py）")
        return 1
    with open(rec_path, encoding="utf-8") as f:
        rec = json.load(f)
    files = rec.get("files", {})
    if not files:
        print("[check_portal_sync] FAIL：_portal_sync.json 无 files 记录")
        return 1
    missing, mismatch, ok = [], [], 0
    for rel in sorted(files):
        p = os.path.join(ROOT, rel)
        if not os.path.isfile(p):
            missing.append(rel)
            continue
        if _sha256(p) == files[rel]:
            ok += 1
        else:
            mismatch.append(rel)
    if missing or mismatch:
        print("[check_portal_sync] FAIL：一致 %d/%d；缺失 %s；哈希不符 %s"
              % (ok, len(files), missing, mismatch))
        return 1
    print("[check_portal_sync] OK — %d/%d 门户文件哈希一致" % (ok, len(files)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
