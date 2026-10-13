# Good First Issues — claimable tasks

These are scoped, external-contributor-friendly tasks. To claim one, comment on the linked Issue (or open one referencing this list) and we'll assign it.

> Status legend: 🔓 open to claim · 🔧 in progress · ✅ done

## Documentation & consistency
| Task | Repo | Difficulty | Notes |
|---|---|---|---|
| Add a `SECURITY.md` to each tool module (copy from portal template) | all modules | 🟢 easy | use `_common/SECURITY.md` as base; adapt scope line |
| Add `CODE_OF_CONDUCT.md` to each module | all modules | 🟢 easy | copy portal CoC |
| Add verification-tier badge to each module README | all modules | 🟢 easy | follow module-README-template |
| Standardise module README to the unified template | all modules | 🟡 medium | one PR per module |
| Fix broken relative links in portal `index.html` | medical-ai-toolkit | 🟢 easy | link-check script welcome |

## Tooling & tests
| Task | Repo | Difficulty | Notes |
|---|---|---|---|
| Add a `--selftest` path where missing | various | 🟡 medium | stdlib assert only |
| Add GitHub Actions CI to a module that lacks it | various | 🟡 medium | mirror portal `harness.yml` pattern |
| Write unit tests for a calculator module (sterilization / pms / udi) | respective | 🟡 medium | stdlib `unittest` |

## Regulatory accuracy (requires source tracing)
| Task | Repo | Difficulty | Notes |
|---|---|---|---|
| Stamp "verified-on" dates on regulatory constants | all | 🟡 medium | must cite official source + version |
| Add PMDA (Japan) column to `device-regulatory-map` | device-regulatory-map | 🟡 medium | source: PMDA 薬機法 |

## Cross-industry extension (reserved interfaces)
| Task | Repo | Difficulty | Notes |
|---|---|---|---|
| Draft `lgd-verticals` skeleton doc for an AI-agent vertical | medical-ai-toolkit | 🟡 medium | keep medical module separate from neutral skeleton |
| Define a neutral "plugin contract" doc | medical-ai-toolkit | 🟢 easy | clarify LGD module interface for non-medical domains |

> 🔵 **Expert review** is not yet available for any task — contributors should not claim expert sign-off. Maintainers will label issues `help-wanted` / `good-first-issue` as they are opened.
