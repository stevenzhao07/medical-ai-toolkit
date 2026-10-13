---
name: ml-validation-toolkit
description: 医疗 AI 模型的验证工具包：给定 y_true / y_pred（可选 subgroup），计算 AUC、Accuracy、Precision/Recall/F1、Brier 校准误差，以及子组公平性缺口（人口均等等差 / 机会均等等差）。仅 Python 标准库实现，便于离线审计。
---
# 医疗 AI 模型验证包（性能/校准/公平性，零依赖）

医疗 AI 模型的验证工具包：给定 y_true / y_pred（可选 subgroup），计算 AUC、Accuracy、Precision/Recall/F1、Brier 校准误差，以及子组公平性缺口（人口均等等差 / 机会均等等差）。仅 Python 标准库实现，便于离线审计。

## 用法
```bash
git clone https://github.com/stevenzhao07/ml-validation-toolkit.git && cd ml-validation-toolkit
python scripts/ml_validation.py --demo
```

## 提供能力
ml-validation-toolkit, ml-validation, fairness, calibration

## 关联
- 仓库: https://github.com/stevenzhao07/ml-validation-toolkit
- AI 参与指南: https://github.com/stevenzhao07/medical-ai-toolkit/blob/main/AI_PARTICIPATION.md
