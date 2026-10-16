# Contributing / 贡献指南

Thank you for considering a contribution to the MedXpert medical-ai-toolkit portfolio. / 感谢你考虑为 MedXpert medical-ai-toolkit 组合贡献。

## Scope / 范围
This repository is the portal/registry of the stevenzhao07 medical-AI toolkit (33 modules). Contributions improving accuracy of regulatory references, adding verifiable modules, or fixing documentation are welcome. / 本仓为 stevenzhao07 医械 AI 工具链（33 模块）门户/注册中心。欢迎改进法规引用的准确性、新增可验证模块或修复文档的贡献。

## Process / 流程
1. Open an issue describing the change (bug / feature / docs). / 先开 issue 描述变更（缺陷/功能/文档）。
2. Fork, make changes, run the module self-test (`--selftest`) — every script ships built-in assertions with negative controls. / Fork 并修改，运行模块自测（`--selftest`）——每个脚本内置带负对照的断言。
3. Submit a pull request referencing the issue. CI (smoke / CodeQL / Scorecard) must pass. / 提交关联 issue 的 PR，CI（smoke/CodeQL/Scorecard）必须通过。

## Standards / 标准
- Bilingual: English first, Chinese complete, both unabridged for any public-facing doc. / 对外文档双语英前中完整、均不缩写。
- Neutral wording only; no placeholder or priority-claim phrasing. / 仅中性措辞，禁止占位/抢注类表述。
- Zero runtime dependencies (stdlib only) unless approved. / 零运行时依赖（仅标准库），除非获批。
- License: Apache-2.0. / 许可证：Apache-2.0。

## Response / 响应
Maintainers will respond within 5 working days. / 维护者将在 5 个工作日内响应。
