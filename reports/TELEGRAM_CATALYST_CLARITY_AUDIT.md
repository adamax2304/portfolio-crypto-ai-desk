# Telegram Catalyst Clarity Audit (PART 8)

**Date:** 2026-06-15 · Read-only. Builds on the prior Telegram standardization.

## Current state of catalyst context in Telegram

| Question | Current answer |
|---|---|
| Does message say catalyst-backed vs technical-only? | ❌ no explicit label |
| Fresh catalyst timestamp? | ❌ not in message |
| Source type (official/news/social)? | ❌ not shown |
| Funding/OI flags? | ❌ not in current message body |
| Warns when catalyst missing? | ⚠️ partial — no-news short caution exists (added in scalp/standardization work) |
| No-news short caution? | ✅ `⚠️ NO-NEWS / NO-DERIV SHORT` (implemented) |
| Scalp says technical / low-confidence? | ✅ `⚠️ LOW-CONFIDENCE SCALP` (implemented) |

So today's Telegram messages carry the **risk cautions** but not the **positive catalyst context** (the operator can't tell from the message whether a long is catalyst-backed or pure technical).

## Recommended short labels (NOT implemented — needs approval)

Add to setup + paper-entry templates a compact 3-line catalyst block:
```
Catalyst: fresh official | recent news | social | none
Funding/OI: confirmed | missing | conflicting
Move type: catalyst-backed | technical momentum | chase risk
```
Concrete examples:
```
Catalyst: recent news (3h, CoinDesk)
Funding/OI: confirmed (OI up, funding normal)
Move type: catalyst-backed
```
```
Catalyst: none
Funding/OI: confirmed (no squeeze)
Move type: technical momentum
```

All three lines are derivable from existing fields (`news_supported`, `importance_score`, `source_quality`, `funding_context`, `oi_context`). This is a **label-only, additive** change.

## Recommendation

Implement the 3-line catalyst block as an additive template change **only after operator approval** (it changes message content). It does not touch scoring/TP/SL/routing. Documented in the safe fix plan; not implemented in this pass.
