# PRE — Fast Safe Acceleration Baseline (PART 0)

**Date:** 2026-06-17 · **Stage:** apply the obvious leak fix (C-tier stocks-intraday) + accelerate evidence (OHLCV backfill, shadow exits) + stability. **No live, no trade-math change.**

## Confirmed state (safety gates)
| Gate | State |
|---|---|
| live | **off** (Control Plane `enable_live_commands=False`) |
| auto-live | **off / locked** (`auto_live_locked=True`) |
| crypto scalp actionable | **off** (shadow-only) |
| stocks scalp production | **off** |
| `partial_exit_model.enabled` | **false** (config verified) |
| TP/SL / scoring / thresholds | **unchanged** |
| sector cap value | **unchanged** (1.0/0.5/0×) |
| last full suite | 742 passed, 0 failed |

## Current scheduler steps (19, dry-run verified)
track-signals (pre) → crypto scalp/intraday reports → catalyst scan → **catalyst integrity scan** → **ohlcv archive (5m/15m)** → stocks intraday report → crypto/stocks monitors → active-signals/signal-stats → **open intraday lifecycle review** → untracked detector → track-signals (post) → daily review → dashboard refresh. (3 bolded = added in the prior operational deploy; all non-fatal.)

## OHLCV archive status (pre-backfill)
Started in the prior stage; archive ≈ rolling window depth on day 1 (5m≈18h, 15m≈2.3d). Path-aware profit replay coverage ~17.8% → this sprint backfills 5m/15m to lift it.

## Current C-tier behavior (verified)
- `decide_paper_entry` already returns `should_send=False` with `reason_skipped="tier=C not actionable"` for **all** C-tier (crypto + stocks). The stocks monitor `_load_active_ab` already filters alerts to A/B. The Control Plane `actionability.classify` already lists "C-tier → not actionable".
- ⇒ **C-tier stocks-intraday is already non-actionable.** The 30d −34R C-tier figure is a **tracking/measurement artifact** (C-tier signals are registered+tracked for outcomes), not live actionable exposure. This sprint makes the restriction an **explicit, configurable, labeled policy**.

## paper_entry payload fields / Control Plane / Telegram (current)
- Payload carries the risk-guard bundle (circuit breaker, risk-off, lifecycle, sector-cap would-bind, profit hint, catalyst integrity, position advisor).
- Control Plane reads them read-only (`desk_adapter.py` `.get()`); TS optional fields.
- Telegram B/A alerts: SL always present, freshness line, compact diagnostic lines appended; plain-text.

## What this sprint connects (all safe)
1. Explicit stocks-intraday C-tier policy flag + labels (routing/actionability only).
2. Historical 5m/15m OHLCV backfill into `data/archive/ohlcv` (append-only).
3. Shadow exit manager + ledger (alternative-exit measurement; real exits unchanged).
4. Stability/sanity checks + post-backfill replay.

## What will NOT change
Live/auto-live/exchange-exec, scalp enablement, TP/SL, scoring, thresholds, sector-cap value, BE/partial/trailing in trade logic, hard breaker/throttle/cap, force-close, history, Control Plane safety/commands/locks.

## Rollback
Set `tier_policy.stocks_intraday_c_tier: actionable` (reverts the C-tier label/route); delete `src/signals/tier_policy.py`, `src/exits/`, the new scripts; delete `data/archive/ohlcv` (rolling cache untouched). Each is independent and zero-impact on live trades.
