#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""manifest.py — 重算 _portal_sync.json 的门户文件哈希台账（零依赖）

check_portal_sync.py 的报错文案一直写「先跑 manifest.py」，但这个生成器
此前并不在仓里——于是台账一旦与实际文件不一致（例如 lifecycle_modules.py
被修过），任何人都只能手改哈希。本脚本补上这个入口。

范围：只重算台账里**已登记**的文件路径，不擅自扩大范围；
      可以显式追加新路径：python manifest.py extra/path.md ...
"""
from __future__ import annotations

import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REC = os.path.join(HERE, "_portal_sync.json")


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    with open(REC, encoding="utf-8") as f:
        rec = json.load(f)
    files = dict(rec.get("files", {}))
    for extra in sys.argv[1:]:
        files.setdefault(extra, "")
    missing, changed, same = [], [], 0
    for rel, old in sorted(files.items()):
        p = os.path.join(HERE, rel)
        if not os.path.isfile(p):
            missing.append(rel)
            continue
        new = sha256(p)
        if new != old:
            changed.append(rel)
        else:
            same += 1
        files[rel] = new
    rec["files"] = {k: files[k] for k in sorted(files)}
    with open(REC, "w", encoding="utf-8") as f:
        json.dump(rec, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print("[manifest] 未变 %d；重算 %d %s；缺失 %s"
          % (same, len(changed), changed or "", missing or "无"))
    return 0 if not missing else 1


if __name__ == "__main__":
    raise SystemExit(main())
