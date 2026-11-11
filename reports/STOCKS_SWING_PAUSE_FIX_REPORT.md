# Stocks Swing Pause — P1 Fix Report

**Date:** 2026-06-05 · Source: 48h post-fix audit (`FULL_SYSTEM_AND_TRADE_AUDIT_48H.md`)
**Scope:** `asset_class=stocks AND mode=swing` only. No scoring/threshold/stop-TP
changes. No crypto changes. No data deleted.

## 1. Why
The 48h audit found **stocks swing was the single biggest confirmed loss
bucket: −12R, 0 wins / 12 losses (PF 0.00)** — swing longs faded into the
AVGO-led semiconductor pullback. Root cause is mode/selection/timing, not
stops or gates. Action: cap stocks-swing A/B to watchlist/research until
reviewed, so it stops generating actionable (Telegram-pushed) losing trades
while staying fully visible for study.

## 2. What changed (one gate, one banner)
**Gate C — `src/stocks/agents/trade_idea_agent.py` (`StockTradeIdeaAgent.run`).**
Added after the existing market-closed Gate A, mirroring the same
demote-not-reject pattern used by the legal / post-earnings / market-closed
gates:

```python
if mode == "swing":
    marker = "stocks_swing_paused_after_48h_audit"
    if marker not in cap_reasons:
        cap_reasons.append(marker)
    if tier in ("A", "B"):
        original_tier = tier
        tier = "C"
        cap_reasons.append(
            f"tier demoted {original_tier}→C: stocks_swing_paused_after_48h_audit "
            "(−12R, 0W/12L) — watchlist/research only until reviewed")
    avoid_conditions.append(
        "stocks swing temporarily paused (48h audit: −12R, 0W/12L) — "
        "watchlist/research only, not an actionable A/B entry.")
```

- Stocks-swing A/B candidates → **C** (cap value never lifts a tier; it only
  demotes), carrying `cap_reason = stocks_swing_paused_after_48h_audit`.
- The signal is **not deleted** — it is registered/visible as C/watchlist.
- C-tier is, by existing design, **not Telegram-actionable** (the stocks
  monitor only alerts A/B). So demoting to C ⇒ **no A/B Telegram alert** for
  stocks swing, with zero change to the monitor's selection/cooldown/dedup.

**Report banner — `src/stocks/reports/stocks_report_builder.py`.** When
`result.mode == "swing"`, the report now prints, up top:

> **STOCKS SWING — watchlist / research only.** Stocks swing is temporarily
> watchlist-only due to 48h audit: −12R, 0W/12L. Swing A/B candidates are
> capped to C (no Telegram A/B alerts) until reviewed; they remain listed
> below for research.

## 3. Scope guarantees (what is NOT touched)
| Surface | Behavior | Test |
|---|---|---|
| stocks **intraday** | unaffected (A stays A) | `test_intraday_not_swing_paused` |
| stocks **invest** | unaffected (A stays A) | `test_invest_not_swing_paused`, `test_invest_not_affected_by_market_closed` |
| **crypto** (all modes incl. swing) | untouched — gate is in the stocks agent only | n/a (stocks-only code path) |
| stops / TP geometry | unchanged | — |
| global A/B thresholds | unchanged | — |
| monitor cooldown / dedup | unchanged | covered in PART 2 report |

## 4. Tests (in `tests/test_stocks_swing_pause.py`, all green)
- `test_swing_Atier_demoted_to_C` — swing A → C + cap_reason present.
- `test_swing_Btier_demoted_to_C` — swing B → C + cap_reason present.
- `test_swing_demotion_records_demote_reason` — `tier demoted A→C` recorded.
- `test_swing_existing_C_still_capped_not_deleted` — C swing stays present (1
  idea, not deleted) + cap_reason.
- `test_swing_carries_watchlist_avoid_note` — watchlist/research avoid note.
- `test_intraday_not_swing_paused`, `test_invest_not_swing_paused` — scope.
- `test_report_renders_swing_watchlist_note` — banner + "−12R, 0W/12L".
- `test_report_intraday_has_no_swing_note` — banner is swing-only.
- Updated `tests/test_stocks_market_closed_stale.py`:
  `test_swing_not_affected_by_market_closed_gate` (swing capping is by Gate C,
  not the market-closed reason) + new `test_invest_not_affected_by_market_closed`.

## 5. Reversal
To re-enable stocks swing after review: delete the `if mode == "swing":` block
in `trade_idea_agent.run()` and the swing banner in the report builder. No data
migration needed — historical swing signals are intact.
