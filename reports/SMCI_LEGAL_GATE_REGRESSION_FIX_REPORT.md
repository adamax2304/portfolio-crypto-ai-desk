# SMCI Legal-Gate Regression — Fix Report (PART 17)

**Date:** 2026-06-03
**Severity:** HIGH (safety / data quality)
**Scope:** stocks pipeline only — crypto path untouched.

## Problem

`SystemAuditReport 2026-06-03` flagged SMCI as a *clean actionable A-tier
long* even though the system already knew (PART 3) about the SEC/DOJ
indictment, the class-action filings, and the Ernst & Young auditor
resignation. The headline-risk gate had been wired correctly, but the
candidate kept emerging A-tier with **no legal flag**, no cap_reason,
and was a Telegram-pushable signal.

## Root cause

`CompanyNewsAgent.load_recent_news()` paged news_items with a fixed
`ORDER BY published_at DESC LIMIT 200` per cycle. With Telegram + RSS
producing ~100 fresh rows / 24 h, the March–April 2026 SMCI legal news
was pushed past the 200-row freshness ceiling within ~48 h and **never
reached `detect_legal_risk()`**. PART 3's regex gate was intact, but it
was reading from a window that no longer contained the source.

## Fix — three layers

### 1. Persistent legal-news loader (`src/stocks/legal_risk.py`)

New `load_active_legal_news(db, symbols, lookback_days=90)`:

- Queries `news_items` directly with a LIKE pre-filter for the
  legal-risk keyword set (indicted, indictment, SEC charges, DOJ, fraud
  alleged, class action, restatement, auditor resigns, going concern,
  delisting risk, …).
- Pre-filter joined with `WHERE published_at >= now() - 90 days`.
- Re-validates each candidate row with the PART 3 `LEGAL_RISK_PATTERNS`
  so the LIKE recall doesn't leak false positives.
- Returns a `dict[symbol → list[dict]]` of confirmed legal-news hits.

### 2. Pattern improvements

Tests surfaced two regex gaps:

- **Class-action PR wire format** ("Hagens Berman Files New Securities
  Class Action Against …"). Added
  `r"\b(files?|announces?|reminds?)\b.{0,60}\bclass[- ]action\b"` and
  `r"\bsecurities? class[- ]action\b"`.
- **Auditor resignation phrasing** ("Ernst & Young resigns as Super
  Micro Computer auditor"). Loosened pattern to `resign[a-z]*` and
  added explicit auditor-firm names
  `r"\b(E&Y|Ernst & Young|PwC|Deloitte|KPMG|BDO) resign[a-z]*\b"`.
  Extended the LIKE pre-filter accordingly so the loader actually
  surfaces these rows.

### 3. Wire-up + hard tier demotion (`trade_idea_agent.py`)

Before the per-symbol loop the agent now collects all symbols and calls
`load_active_legal_news()` once. Inside the loop it merges
recent_news + persistent_news (dedup by URL) and runs
`detect_legal_risk(merged_news)`.

When the assessment is `blocking=True` and tier is A or B, the agent
now **actively demotes tier → C** with:

```
cap_reasons.append(
  f"tier demoted {original_tier}→C: active legal/headline risk "
  f"({','.join(sorted(categories))}) — manual review required"
)
```

Score is **preserved** for auditability (we never silently mutate the
scoring signal); the tier reflects the safety override.

## Where the flag is now visible

| Surface | Field / line |
|---|---|
| Scoring agent | unchanged (score retained for audit) |
| StockTradeIdeaAgent output | `tier="C"`, `cap_reasons=[…]`, `avoid_conditions=[…]` |
| `stocks-intraday-report` | "earnings: safe" + Counter-Thesis lists legal_headline_risk + tier-demotion reason |
| Telegram alert context | tier=C → does not Telegram (A/B only) |
| LLM packet (`llm_stocks_packet.md`) | C-tier section, cap_reasons rendered |
| Obsidian dashboards | C-tier row, dashboard-stat dedup unaffected |

## Verification

Live run (2026-06-03 ~15:15 ET intraday cycle):

```
SMCI intraday tier=C dir=long score=82.26 status=waiting_for_entry
cap_reasons:
  - legal_headline_risk: class_action,indictment,securities_fraud
  - tier demoted A→C: active legal/headline risk
    (class_action,indictment,securities_fraud) — manual review required
```

11 new pin-tests in `tests/test_stocks_legal_persistent.py` covering:
auditor-resignation matching, class-action PR phrasing, persistent
loader, end-to-end agent A→C demotion, score preservation, cap_reasons
ordering, no-op path when there is no legal news.

Updated `tests/test_stocks_legal_risk.py:315` from `tier=="A"` to
`tier=="C"` (PART 17 now actively demotes; PART 3 was passive).

## Safety contract — preserved verbatim

- ✅ Do not auto-trade.
- ✅ Do not change global A/B thresholds.
- ✅ Do not change crypto logic.
- ✅ Do not weaken filters.
- ✅ Do not delete historical data.
- ✅ Do not restart scheduler unless explicitly needed (restarted at
  user request after manual verification).

## Files touched

- `src/stocks/legal_risk.py` — `load_active_legal_news()` + pattern
  extensions
- `src/stocks/agents/trade_idea_agent.py` — persistent-news merge +
  hard tier demotion
- `tests/test_stocks_legal_persistent.py` — NEW (11 tests)
- `tests/test_stocks_legal_risk.py` — line 315 expected tier C
