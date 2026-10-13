---
name: pms-vigilance
description: 上市后监督（PMS）与警戒（Vigilance）时限计算与合规工具：NMPA 不良事件报告（死亡 7 日/严重伤害 20 日/群体 12 小时）、EU MDR Art.87（2/10/15 天）、FDA MDR（30 日/5 工作日/806 召回 10 工作日）、召回分级时限表（NMPA 一级 1 日起/FDA Class I–III）、PSUR/定期风险评价周期。输入获知日期，输出各辖区截止日。
---
# 上市后监督与警戒工具（报告时限/召回分级/PSUR）

上市后监督（PMS）与警戒（Vigilance）时限计算与合规工具：NMPA 不良事件报告（死亡 7 日/严重伤害 20 日/群体 12 小时）、EU MDR Art.87（2/10/15 天）、FDA MDR（30 日/5 工作日/806 召回 10 工作日）、召回分级时限表（NMPA 一级 1 日起/FDA Class I–III）、PSUR/定期风险评价周期。输入获知日期，输出各辖区截止日。

## 用法
```bash
git clone https://github.com/stevenzhao07/pms-vigilance.git && cd pms-vigilance
python scripts/pms_report.py --demo
```

## 提供能力
pms-vigilance, report-deadline, recall-levels, psur-cycle

## 关联
- 仓库: https://github.com/stevenzhao07/pms-vigilance
- AI 参与指南: https://github.com/stevenzhao07/medical-ai-toolkit/blob/main/AI_PARTICIPATION.md
