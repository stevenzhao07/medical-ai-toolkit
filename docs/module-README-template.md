# Module README template (unified)

Copy this structure for every tool module. Keep it short; link don't duplicate.

```markdown
# <module-name>

> One-line purpose. <-- 一句话定位

**Contributed by [@stevenzhao07](https://github.com/stevenzhao07).** Open-source reference implementation; technical input only. (Any specific organisational relationship is disclosed separately by the account owner, not auto-added here.)

## What it does
<!-- 2-4 sentences. What decision/output it produces. -->

## Scope & boundaries (适用边界)
<!-- What it does NOT do. Explicitly: not a medical device, not clinical advice. -->

## Quick start (最小运行示例)
`bash
python <module>.py --help
python <module>.py --selftest
`

## Verification status
| Tier | State |
|---|---|
| 🟢 CI | … |
| 🟡 Functional self-test | … |
| 🔵 Expert review | pending / done (by whom, date) |
| ⚪ Official source | … with source + version + verified-on date |

## Regulatory / standards sources (法规与标准来源)
<!-- For every constant: official name, version/edition, URL, verified-on date. -->
- ISO 14971:2019 — https://www.iso.org — verified 2026-xx-xx

## Version
<!-- semver or date. Note breaking changes. -->
v0.1.0 (2026-xx-xx)

## Contributing
See the portal [CONTRIBUTING.md](https://github.com/stevenzhao07/medical-ai-toolkit/blob/main/CONTRIBUTING.md).

## License
See this repository's `LICENSE` file. Licenses vary **per repository** across the `@stevenzhao07` account (Apache-2.0 / CC BY 4.0 / CC0 / MIT) — do not assume one account-wide license. The authoritative terms are always the repo's own `LICENSE`.
```

> Rule: every regulatory constant must carry a **source + version + verified-on date**, or be marked `⚠️ 待核实`. Never state a number as fact without its origin.
