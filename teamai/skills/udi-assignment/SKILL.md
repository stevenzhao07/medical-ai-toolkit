---
name: udi-assignment
description: 医疗器械唯一标识（UDI）赋码参考实现：GS1 GTIN-14 校验位计算（mod-10）、DI/PI 拆分（生产日期/批号/序列号/有效期）、HIBCC/ICCBBA 体系说明、FDA GUDID / NMPA 器械 UDI 数据库 / EUDAMED 三侧必填字段对照。补 fhir-ortho-toolkit（数据侧）与 multilingual-ifu（标签侧）之间的赋码缺口。
---
# UDI 赋码工具（GS1 DI/PI + 辖区数据库字段）

医疗器械唯一标识（UDI）赋码参考实现：GS1 GTIN-14 校验位计算（mod-10）、DI/PI 拆分（生产日期/批号/序列号/有效期）、HIBCC/ICCBBA 体系说明、FDA GUDID / NMPA 器械 UDI 数据库 / EUDAMED 三侧必填字段对照。补 fhir-ortho-toolkit（数据侧）与 multilingual-ifu（标签侧）之间的赋码缺口。

## 用法
```bash
git clone https://github.com/stevenzhao07/udi-assignment.git && cd udi-assignment
python scripts/udi_assign.py --demo
```

## 提供能力
udi-assignment, gtin-check-digit, di-pi-split, udi-db-fields

## 关联
- 仓库: https://github.com/stevenzhao07/udi-assignment
- AI 参与指南: https://github.com/stevenzhao07/medical-ai-toolkit/blob/main/AI_PARTICIPATION.md
