# Verification policy

Regulations and standards change. A value that was correct a year ago may be wrong today. This document states how factual claims in these modules are sourced, what happens when a source cannot be found, and how to report an error.

## The rule

**Every factual assertion names its source.** A number, a standard number, a clause reference or an effective date is either traceable to a primary text — or marked as unverified. There is no third option, and in particular there is no "plausible value".

## `TO_BE_VERIFIED`

Where a primary text could not be consulted, the item is marked `TO_BE_VERIFIED` in the output rather than filled in. Examples of what this looks like in practice:

- A clause structure is listed, but the specific values expected in the 2025 revision of a regulation are marked for verification instead of being reconstructed from the older revision.
- A jurisdiction's database field list is labelled as subject to the current official guidance.

The marker is deliberately visible in CLI output. A user should be able to see, without reading source code, which parts of an answer rest on a verified source and which do not.

## Source order

1. **Primary** — the standard or regulation itself, or the issuing authority's own publication (NMPA notice, EU MDR text, FDA CFR, PMDA administrative notice, ISO/IEC standard text).
2. **Authoritative secondary** — the issuing authority's own guidance documents, FAQs, or MDCG guidance.
3. **Everything else** — accepted only when layered on top of a primary source, and never the sole basis for a numeric value or a deadline.

Where two jurisdictions disagree, the module states both rather than harmonising them. A toolkit that silently picks one jurisdiction's value is more dangerous than one that shows the disagreement.

## What is deliberately not claimed

- No compliance conclusion. The modules produce structures and calculations, not a determination that a device conforms.
- No interpretation of whether a given regulation applies to your product.
- No reproduction of regulatory texts — the modules carry clause structure and computation, not the law's wording.
- No version currency guarantee. The toolkit records what was verified and when; it cannot know that a regulation changed last week.

## Reporting an error

Corrections are the highest-value contribution to this project. Open an issue using the [Report a factual error](https://github.com/stevenzhao07/medical-ai-toolkit/issues/new/choose) template and include the primary source that contradicts what the module says.

If you believe a value is wrong but cannot cite a source, say so. The item will be marked `TO_BE_VERIFIED` and flagged for review — which is a better outcome than either leaving a wrong number in place or replacing it with another plausible one.

---

## 中文

法规与标准一直在变：去年正确的值，今年可能就是错的。本文说明这些模块里的事实性断言如何溯源、找不到来源时如何处理、以及发现错误怎么报。

**规则**：**每条事实性断言都标出来源**。一个数值、标准号、条款引用或生效日期，要么能追溯到一手文本，要么就标为未核实。**没有第三种选项**，尤其不存在"看起来合理的值"。

**`TO_BE_VERIFIED`**：凡未能查阅一手文本的项，标注 `TO_BE_VERIFIED` 而不是填一个数。例如：某法规 2025 修订版中应有的具体值标为待核验，而不是从旧版反推；某辖区的数据库字段清单注明"以最新官方指南为准"。该标记**刻意出现在 CLI 输出里** —— 使用者无需读源码，就能看出答案里哪些部分有据、哪些没有。

**来源优先级**：① **一手** —— 标准/法规本身，或发布机关的官方出版物（NMPA 公告、EU MDR 文本、FDA CFR、PMDA 通知、ISO/IEC 标准正文）；② **权威二手** —— 发布机关自己的指南、问答、MDCG 指南；③ **其他** —— 仅当叠加在一手来源之上时才采信，且绝不能作为数值或时限的唯一依据。两个辖区不一致时，模块**两个都写**，而不是强行统一 —— 悄悄替用户选一个辖区的值，比展示分歧更危险。

**刻意不做的主张**：不给合规结论（模块产出结构与计算，不判定器械是否符合）；不判断某法规是否适用于你的产品；不复制法规全文（只承载条款结构与计算）；不保证版本时效（记录"何时核实过什么"，但无法知道上周法规是否变了）。

**报错**：纠错是价值最高的贡献。请用 [Report a factual error](https://github.com/stevenzhao07/medical-ai-toolkit/issues/new/choose) 模板提 Issue，并附上与你所指相矛盾的**一手来源**。若你确信有错但找不到来源，也请直接说 —— 该项会被标为 `TO_BE_VERIFIED` 并进入复核，这比"留着错值"或"换成另一个看似合理的值"都好。
