# Current Trading Playbooks — One-Page Summary

**Date:** 2026-06-09 · Companion to [STRATEGY_PLAYBOOK_AUDIT.md](STRATEGY_PLAYBOOK_AUDIT.md). Numbers are 14d, deduped, A/B only.

## Mode playbooks

| # | Playbook | Status | Regime fit | Best on | Avoid | 14d evidence |
|---|---|---|---|---|---|---|
| 1 | **Crypto scalp** — 2h momentum continuation, ATR zone entry, TP1=+1R | ⚠ **active, low-confidence** | shallow trend / vol normal | binance-listed liquid alts | thin MEXC-only, chop/danger regime | **WR 12% · PF 0.14 · −6R** (n=59, closed=8); 100% expired had +MFE, avg +0.54R |
| 2 | **Crypto intraday** — 24h continuation, catalyst-or-RS confirmation | ✅ actionable | bullish / risk-on transition | catalyst-backed names, RS leaders | no-catalyst longs in chop | overall **WR 33% · PF 1.29 · +4R**; **with news=1: WR 50% · PF 2.75 · +7R** |
| 3 | **Crypto swing** — 7d trend pullback / narrative basket | ✅ **primary** | trending or narrative rotation | ALLO, ZEC, WLD, BANK; narrative basket members | already-vertical 24h moves | **WR 72% · PF 5.80 · +24R** (n=18, closed=18) — strongest mode |
| 4 | **Stocks intraday** — 15m/1h RTH momentum, sector + earnings gated | ✅ **primary** | SPY/QQQ with direction | XOM, LLY, AAPL, AVGO, UNH; short-side: META, AMZN, SPY, QQQ, XLK | NVDA long, SMCI long, SMH long | overall **WR 55% · PF 2.03 · +80R** (n=479); shorts subset **WR 86% · PF 9.00 · +8R** |
| 5 | **Stocks swing** — 7d RS/sector rotation | 🛑 paused | trending market | (re-enable pending) | the pre-pause A-tier-long basket | **WR 11% · PF 0.15 · −33R** before pause |
| 6 | **Stocks invest** — 30d thesis | 🛑 paused | macro thesis | (re-enable pending) | same pipeline as swing | **WR 0% · 0W/24L · −24R** |

## Cross-mode overlays

| Overlay | Lifts | Neutral / negative | 14d evidence |
|---|---|---|---|
| **Catalyst-backed** (`news_supported=1`) | crypto intraday + crypto swing | crypto scalp (0/2 — no edge) | crypto news=1 overall: **WR 50% · PF 2.83 · +11R** (n=26, closed=12) |
| **RS-leader long** (top-decile RS vs BTC) | crypto intraday + crypto swing | overextended late-cycle leaders | embedded in swing 72% WR; recurring: ALLO, ZEC, WLD |
| **Shorts** | crypto bearish-trend, stocks selloff | extreme-negative funding (squeeze) | crypto shorts **WR 40% · PF 2.00 · +9R**; stocks shorts **WR 86% · PF 9.00 · +8R** |

## Decision rules the system follows today

1. **Tier gating** (A/B Telegram-actionable, C watchlist-only).
2. **Mode-specific validity windows**: scalp 2h, intraday 24h, swing 168h, invest 720h.
3. **Sector / regime / catalyst / RS / derivatives weights** in the scoring agent (unchanged).
4. **Active gates** (caps applied at the trade-idea agent stage):
   - `stocks_swing_paused_after_48h_audit` — stocks swing A/B → C.
   - `stocks_invest_paused_after_mode_viability_audit` — stocks invest A/B → C.
   - `market_closed_intraday_planning_only` — stocks intraday A/B → C outside RTH.
   - `stale_post_earnings_setup` — flagged earnings + UNKNOWN severity → C.
5. **Reporting annotations** (banners + Telegram lines):
   - Crypto scalp: low-confidence banner + Telegram annotation.
   - Stocks swing / invest: watchlist-only banner.
6. **Pending-signal revalidation** (live since 2026-06-09 20:38 EEST on PID 16684):
   - Stale-by-mode-horizon → `stale_before_entry`.
   - Favorable run > 2R without fill → `entry_moved_away`.
   - Hard invariant: never mutates entry/stop/TP/expires_at.

## Single-sentence summary

The system today **trades** crypto intraday (catalyst-confirmed) and crypto swing (RS leaders + narrative baskets) actionably; **trades** stocks intraday RTH with strong B-tier edge; **annotates but still alerts** crypto scalp as low-confidence pending strategy work; and **watchlists-only** stocks swing and invest until enough post-pause C-tier data accumulates to revisit them.

## Verdict
```
STRATEGY_PLAYBOOK_AUDIT_COMPLETE
```
