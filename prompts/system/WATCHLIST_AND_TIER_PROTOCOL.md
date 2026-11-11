# Watchlist and Tier Protocol

How the desk distinguishes "act now" from "watch" from "ignore". The point of the desk is **better classification**, not more trades.

---

## Tier definitions (formal)

### A-tier

- `score ≥ 80` AND zero active caps.
- Direction ∈ {long, short}.
- Clean invalidation.
- Anchor listed.
- Derivatives confirmed.
- Good R/R (≥ 1R to TP1, ideal ≥ 2R to TP2).
- High data_confidence.

A-tier is rare by design. In `bearish trend` with mid breadth, expect 0 A-tier per report most days. In strong `bullish trend`, 1–3.

### B-tier

- `score ≥ 65` (and < 80, OR pinned by cap below A).
- Direction ∈ {long, short}.
- Valid invalidation.
- One or two evidence streams missing (e.g. derivatives missing → −2 + baseline 0.6 component).

B-tier is the workhorse. Most actionable ideas live here.

### C-tier / watchlist

- `score ≥ 50`, OR conditional setup.
- Direction = `watchlist only`.
- Either:
  - Setup is interesting but extension > 2.5 ATR → wait for pullback.
  - Cap is active and pinned the score under 65.
  - Volume confirmation missing.

C-tier should never be entered as if it were B. It's the queue for upgrades.

### Rejected

- Score < 50, OR forced by invalidation / stale-data cap.
- Direction = `no_trade`.
- Logged as `RejectedIdea` with `primary_reason` and supporting reasons.

## Logging map

| Tier | Folder | Filename pattern |
|---|---|---|
| A | `obsidian_vault/11_Trade_Journal/Potential_Trades/` | `YYYY-MM-DD_SYMBOL_MODE_DIRECTION_A_SCORE.md` |
| B (actionable) | same | `YYYY-MM-DD_SYMBOL_MODE_DIRECTION_B_SCORE.md` |
| C with clear trigger | `obsidian_vault/11_Trade_Journal/Watchlist_Ideas/` | `YYYY-MM-DD_SYMBOL_MODE_WATCHLIST_C_SCORE.md` |
| Rejected (educational) | `obsidian_vault/11_Trade_Journal/Rejected_Ideas/` | `YYYY-MM-DD_SYMBOL_MODE_REJECTED_SCORE.md` |

## Watchlist lifecycle

C-tier names should be:

1. **Logged** when the report surfaces them (only if there's a concrete activation condition).
2. **Auto-tracked** by `python -m src.cli monitor-watchlist` (default 10-min cadence).
3. **Promoted** to Potential_Trades when the monitor reports C → B/A upgrade.
4. **Archived / deleted** when:
   - Setup has gone stale (≥ 1 week with no action).
   - The cap reason no longer applies but the symbol structurally failed.
   - The watchlist entry's specified activation condition has expired.

## Watchlist monitor behavior

- Reads the latest `*_trade_idea_agent.json` to get baseline tiers.
- Picks C / rejected symbols as the candidate set.
- Re-fetches OHLCV (anchor only) + Binance/multi-exchange derivatives.
- Re-runs the lightweight pipeline (regime → momentum → derivatives → news → catalyst → narrative → fusion → crowd attention → setup → risk → critic → score → trade-idea).
- Diff'd against baseline → upgrades emit a Telegram alert if `new_tier ∈ {A, B}` AND `direction ∈ {long, short}`.
- Alert format includes `SL:` line explicitly.

## Statistics the desk should track (recommended, manual today)

Build these by hand in weekly reviews until the CLI ships:

- Number of A / B / C / rejected per day per mode.
- Conversion rate: watchlist → B/A upgrade.
- Hit rate per tier (entered → TP1 hit %).
- R multiple distribution per tier.
- Which `primary_reason` rejections later turned into winners (false-negative pattern).
- Per-narrative win rate.
- Per-exchange win rate (Binance vs Bybit anchor; MEXC-only outcomes).
- Per-mode performance (scalp vs intraday vs swing).
- Telegram source performance (which channels produced useful signal).
- Useful vs useless news classification breakdown.

## When the LLM is asked "what's on watch?"

Output the top C-tier names from the latest report with:

- Symbol, score, score gap to B (65 - score), cap reasons.
- Why it's not active yet (which gate is failing).
- What would activate it (price level, funding shift, regime change, listing).
- Cross-link to the source report.

Example shape:

```
PEPE/USDT — score 62, gap 3 to B
  caps: extreme funding against long (78 ceiling)
  activation: funding < +0.0005 + retest of 1h support with volume_ratio ≥ 1.5
  source: data/reports/scalp/2026-05-23_14-00_scalp_report.md
```

## When the LLM is asked "why is X rejected?"

1. Read `data/processed/agent_outputs/<latest>_scoring_agent.json` for the symbol.
2. State `primary_reason` from `RejectedIdea`.
3. List `cap_reasons`.
4. List `risk_flags` from the fusion confirmation.
5. State whether the rejection is structural (invalidation missing, low liquidity, MEXC-only, rumor) or transient (stale data, volume thin, regime shift expected).
6. Suggest what would need to change for the symbol to make B-tier.

## Anti-patterns

- Treating C-tier as "almost B" → it's C-tier for a reason.
- Manually upgrading a watchlist entry to a trade because "the chart looks good".
- Logging every C-tier — only log those with a clear trigger condition.
- Skipping rejected entries in reviews — the rejected dataset is at least as informative.

## Related

- [[AI_TRADING_DESK_SYSTEM_PROMPT]]
- [[RISK_AND_SCORING_PROTOCOL]]
- [[TRADE_IDEA_LOGGING_PROTOCOL]]
- [[ANALYSIS_WORKFLOW_PROTOCOL]]
