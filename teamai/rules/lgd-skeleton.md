# lgd-skeleton 团队规范（TeamAI rules）

> 由 manifest.py 自动生成，作为 TeamAI `rules/` 同步进各 AI 编码 Agent。

## 路由（一切即插件）
- 本矩阵是 **lgd-skeleton/1.0** 可插拔模块总入口，AI 代理按任务描述自动选模块。
- 先读 `skeleton.json` 元数据，按 intent 命中再懒加载对应模块全文。
- 说想法即自动搭建：`python idea_scaffold.py "<想法>"`（命中复用 / 否则建骨架 + 跑 harness 自检）。

## 红线（必须遵守）
1. 纯技术贡献，不含商业营销；MedXpert 仅作贡献者 affiliation（@stevenzhao07 署名）。
2. 不挂机构自推；不主张标准制定身份（标准轨道用个人专家弱品牌 Xinghua Zhao）。
3. 发布前须仓库所有者「go」；对外落地动作逐次确认。
4. 关联披露：医疗 AI 信任方法论来源（治理守护者 XCGS / 立法者 A³ Laws / 护照官 AI 护照 / 人机共存）。

## 自检
- 全模块自动测试（6 维度，含 gold 语义回归）：`python harness.py --all`
