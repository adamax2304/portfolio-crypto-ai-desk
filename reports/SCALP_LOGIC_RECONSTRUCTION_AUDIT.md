# Crypto Scalp — Logic Reconstruction (PART 1)

**Date:** 2026-06-15 · Read-only. Source-of-truth for the backtest engine.

## 1. Generation path

| Stage | Module | Role |
|---|---|---|
| Candidate discovery | momentum / crowd-attention scan → `MomentumCandidate` | picks symbols + `direction_bias` from technical momentum (no news required) |
| Technical setup | `src/agents/technical_setup_agent.py` | builds entry/stop/TP from EMA20 + ATR14 + recent range |
| Scoring / tier | `src/agents/scoring_agent.py` | assigns score + tier (scalp capped low-confidence) |
| Playbook label | `src/signals/playbooks.py` | `crypto_scalp_momentum_continuation` |
| Sizing weight | `config/sizing_weights.yaml` | **0.5×** (low-confidence) |

- **LLM / Opus involvement:** the trade-idea agent uses the LLM to phrase ideas, but scalp candidate selection + entry/stop/TP geometry are **deterministic technical** computations. Scalp is **technical by design**.
- **News/catalyst dependency:** none required (scalp does not gate on catalyst).
- **Derivatives/funding/OI dependency:** funding/OI is attached for context + crowding penalty, but the core scalp setup is price/ATR-driven.

## 2. Exact geometry (from `technical_setup_agent.py:52-97`)

For ATR = ATR14, close = last close, EMA20, recent 20-bar support/resistance:

**Long:**
- Entry zone: `[close − 0.65·ATR, close − 0.20·ATR]`
- Stop (invalidation): `support − 0.15·ATR` if that is tighter than `close − 1.8·ATR`, else `close − 1.2·ATR` (ATR stop)
- TP1 / TP2 / TP3: `close + 1.0·ATR / +2.0·ATR / +3.0·ATR`

**Short:** mirror image (entry `[close+0.20ATR, close+0.65ATR]`, stop `close+1.2ATR` or resistance, TP `close−1/2/3·ATR`).

- Entry mid ≈ `close ∓ 0.425·ATR`. Risk ≈ `0.775·ATR`. TP1 distance ≈ `1.425·ATR` → **TP1 ≈ +1.84R** in tracker R units (risk = |entry−stop|). This is the key geometric fact: TP1 is far (~1.8R), which is why scalps with avg MFE +0.56R rarely reach it before the 2h expiry.

## 3. Filters / caps

- **Chase filter:** `distance_atr = |close − EMA20| / ATR`; setups more than ~2 ATR from EMA20 are rejected ("do not chase").
- **Regime:** long in bearish/high-vol tape only allowed if relative-strength leader; else conflict penalty.
- **Tier:** scalp is held low-confidence (rarely above B); C-tier sized 0×.
- **No-trade** when ATR unavailable.

## 4. Expiry & revalidation

- **Validity window:** `config/signal_tracking.yaml` → scalp = **2 hours**.
- **Poll cadence (informational):** scalp check intervals `[15m, 30m, 1h, 2h]`.
- **Revalidation:** `stale_before_entry` if 2h elapses unfilled; `entry_moved_away` if price crosses invalidation before fill.

## 5. What the backtest must mirror

1. Scan on a fixed cadence (production ≈ scheduled reports; backtest will scan every 30 min).
2. Per symbol: compute EMA20 + ATR14 on the lookback window available at that timestamp (no lookahead).
3. Generate a long if trend up + within chase distance; short if mirror.
4. Apply the exact entry zone / ATR stop / 1-2-3 ATR TP geometry.
5. Fill only after `created_at`; 2h expiry; stale/moved-away rules.
6. R = (exit − entry) / |entry − stop|. Sized R = raw × 0.5.
7. Fees + slippage per the execution-cost model.

This reconstruction is the contract for `scripts/backtest_crypto_scalp_historical.py`.
