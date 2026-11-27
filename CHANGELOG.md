# Changelog

本仓遵循 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/) 与 [语义化版本](https://semver.org/lang/zh-CN/)。

## [Unreleased]

## [Unreleased] — 2026-11-27 更正

### Fixed
- `lifecycle_modules.py` 里 16 处 `true`、8 处 `null` 是 JSON 字面量，Python 下直接 `NameError`——
  该文件从提交起就导入即崩，而 `check_portal_sync.py` 仍在为它记录哈希，等于台账替一个跑不起来的文件背书。
  已改为 `True` / `None`，并补 `run_all.py` 的 schema 断言（字段齐、id 唯一），防止同类问题再混进来。
- 补上 `manifest.py`：`check_portal_sync.py` 的报错文案一直写「先跑 manifest.py」，但该生成器并不在仓里，
  台账一旦不一致（例如上面的修复）谁都无法重建。现可 `python manifest.py` 重算已登记路径的哈希。
- `README` 里「`python harness.py --module medical-ai-toolkit` 仅在门户本仓可跑」是一条**假指令**：
  实测返回 `rc=2`「模块不在 repos（且非本仓自测）」。已删除，改为指向真正可跑的 `python run_all.py`。

### Changed
- `run_all.py` 三分支：`./repos/` 存在→全量 demo（原行为不变）；单克隆→**仓内自足冒烟**
  （路由 demo / 四向一致 / 哈希台账 / 路由清单 / 扩展模块清单，5 项，任一红即 rc=2）；
  `--full`／`--gold` 仍强制要求 `./repos/`，缺失则明确 SKIP 返回 0（不假绿）。
  动机：外部匿名探针对本仓一直判 `skip`，把「没有东西可跑」和「有东西但没跑」混为一谈。
  冒烟输出末行明写「未覆盖：19 个扩展模块尚无独立公开仓」，不假装覆盖。


> 首次纳入版本化记录。**尚未打 tag / 发 Release**（须所有者批准后执行）。

### Added
- `--selftest`：端到端自测（真实调用 + 内容断言 + **负对照**），可脱离门户单仓运行。
- `SECURITY.md`、`CODE_OF_CONDUCT.md`：补齐社区治理文件。
- `module.json` 增加机器可读的 `stage` / `stage_name`，标明本模块在医疗器械生命周期中的位置。

### Changed
- 文档勘误：移除与实际实现不符的表述（详见项目级 `PROJECT_ATTRIBUTION.md` 与门户 README）。
