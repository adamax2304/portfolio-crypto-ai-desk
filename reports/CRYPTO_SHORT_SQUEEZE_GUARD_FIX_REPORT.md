# Crypto Short Squeeze-Risk Guard — Fix Report (PART 22)

**Date:** 2026-06-04
**Type:** conservative crypto short-side safety layer (cap-to-C). No auto-trade,
no global-threshold change, no stop/TP geometry change, no long-logic change, no
hard-reject of shorts, no data deleted.

## What it does
Caps **high-squeeze-risk crypto SHORTS** to **C / watchlist** (so they are
recorded but **not** Telegram-actionable A/B), based on the read-only audit
(`CRYPTO_SHORT_SQUEEZE_AND_SCAM_WICK_AUDIT.md`): failed shorts were late / thin /
squeezed, **not** mis-stopped. Stops are left untouched (audit: stops were
2.4–4.5× the p90 upper wick — fine).

## Architecture (mirrors the existing PART 20/21 cap pattern)
- **`src/analysis/short_squeeze_gate.py`** (NEW, pure/testable):
  `assess_short_squeeze(candidate, setup, derivative, params)` → `SqueezeVerdict`
  (risk_score, flags, cap, cap_value, cap_reason, note).
- **`src/agents/momentum_scanner_agent.py`**: now computes per-candidate
  squeeze diagnostics from OHLCV — `return_1h`, `quote_volume_24h_usd`,
  `upper_wick_atr_max`, `upper_wick_atr_avg` (read-only).
- **`src/models.py`**: `MomentumCandidate` carries those 4 new optional fields.
- **`src/agents/scoring_agent.py`**: for `direction == "short"` only, calls the
  gate and applies its cap via the existing `caps` mechanism; flags → warnings,
  note → reasons. **Longs never invoke the gate.**
- **`config/scoring.yaml → short_squeeze_guard`**: configurable thresholds
  (`cap_to 60`, `bounce_1h_pct 1.5`, `bounce_dist_atr 0.5`,
  `min_quote_volume_usd 15M`, `max_upper_wick_atr 1.5`, `thin_volume_ratio 0.6`,
  `exhaustion_dist_atr -1.8`, `exhaustion_24h_pct -10`). Global A/B thresholds
  unchanged.

## Cap rules (cap → C; `cap_to=60` < `b_tier=65`)
| flag | condition | catches |
|---|---|---|
| `short_bounce_guard` | 1h return > +1.5% **or** >0.5 ATR above EMA20 | BCH, DEXE, GPS |
| `thin_liquidity_short_squeeze_risk` | 24h quote vol < $15M | SAHARA, OPG, DEXE, GPS |
| `high_upper_wick_short_squeeze_risk` | max upper wick > 1.5× ATR | OPG, DEXE |
| `no_derivatives_thin_short` | derivs missing **and** thin tape | thin alts |
| `late_short_after_exhaustion` | >1.8 ATR below EMA20 **or** 24h < −10% | **warning only** unless combined with a cap flag |

→ ETH-style liquid shorts falling cleanly get only the exhaustion *warning* and
are **not capped** (req #4). Stop/TP geometry untouched (req: no wick-widening).

## Reports / Telegram / packets (PART 5)
Cap reasons + the warning surface in the crypto scalp/intraday reports
(Rejected/Watchlist + idea cap_reasons), the LLM packet, and `signal-stats`/
Telegram context. Capped shorts are C-tier → **no A/B Telegram alert** (monitor
alerts A/B only).

## Tests (PART 6) — `tests/test_short_squeeze_guard.py` (10, all green)
gate: bounce caps; thin caps; high-wick caps (multi-flag); liquid clean short
NOT capped; exhaustion-alone = warning. scoring end-to-end: DEXE-like thin/
bounce short → **C** with squeeze cap_reason; liquid ETH-like short → not
squeeze-capped; **long with thin/high-wick/bounce values → unaffected**; global
thresholds unchanged. Regression: RS-leader/scoring/tiering/regime + full suite.

## Safety
- ✅ Shorts not disabled globally (cap-to-C, not reject). ✅ Longs untouched.
- ✅ Stop/TP geometry unchanged. ✅ Global A/B thresholds unchanged.
- ✅ Existing risk filters intact (additive cap). ✅ No data deleted. ✅ No auto-trade.

## Files
- `src/analysis/short_squeeze_gate.py` — NEW
- `src/agents/momentum_scanner_agent.py` — squeeze diagnostics
- `src/models.py` — 4 new MomentumCandidate fields
- `src/agents/scoring_agent.py` — short squeeze cap wiring
- `config/scoring.yaml` — `short_squeeze_guard` block
- `tests/test_short_squeeze_guard.py` — NEW (10)
