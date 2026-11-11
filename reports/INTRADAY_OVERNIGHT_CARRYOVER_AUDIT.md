# Intraday Overnight-Carryover Audit (PART 3)

**Date:** 2026-06-17 · read-only.

## Why intraday trades hung "since yesterday"
Current rules (verified in code):
- `config/signal_tracking.yaml` / `src/signals/config.py`: **intraday validity = 24h** (scalp 2h, swing 168h, invest 720h). `expires_at = created_at + 24h`.
- `src/signals/registry.py` sets `expires_at`; `src/signals/tracker.py` marks `STATUS_EXPIRED` only when the clock passes `expires_at` *without* a terminal TP/stop.
- **A *triggered* (filled) intraday trade has NO max-holding, NO end-of-day close, and NO next-session revalidation.** It runs until TP/stop or until the 24h window lapses → it can sit open across a UTC-day (and, for stocks, across the RTH close into the next session).
- `src/signals/revalidator.py` exists but only re-checks **unfilled `waiting_for_entry`** signals (marks `STATUS_STALE_BEFORE_ENTRY` after a freshness horizon: intraday 4h), and only when run with `--revalidate-pending`. It does **not** touch filled trades.

So intraday signals legitimately live up to 24h, which routinely crosses a day boundary — exactly the "held since yesterday" behavior.

## Measured carryover
- **91 intraday trades carried overnight** (entry date ≠ exit/now date): **84 stocks, 7 crypto.**
- Outcome of the 91: **48 expired@0R, 21 win, 22 loss; net sumR +17.0.**
- **155 triggered trades expired at 0R overall** (stocks/intraday 48, stocks/swing 36, stocks/invest 36, crypto/scalp 34, crypto/intraday 1).

**Reads:**
- Overnight carry is **overwhelmingly a stocks-intraday phenomenon** (84/91) and is **net +17R**, so it is *not* a P&L emergency — but it is a **risk-hygiene + capacity problem**: stocks "intraday" routinely become silent multi-day holds, and ~half (48) just expire at 0R, tying up tracking/attention.
- crypto intraday almost never expires (1) — it resolves to TP/stop fast; its carry (7) is minor.
- The pending side IS handled (141 `stale_before_entry`), but only when the revalidator runs.

## Proposed rules (cautious — not implemented)
**Crypto intraday:**
- max **pending** age already ≈ handled by revalidator (4h) — ensure `--revalidate-pending` actually runs on the monitor.
- add a **max *trade* age** (e.g. close/expire a filled intraday trade after N h, e.g. 12–16h, or at the next regime refresh) instead of letting it ride to 24h.
- **next-session revalidation**: if regime flipped or catalyst expired since entry → relabel/close/reduce.
- if price never reached TP within N h → review/flatten.

**Stocks intraday:**
- **RTH-aware expiry**: expire/close unresolved intraday trades at US cash close instead of +24h.
- **no overnight carry unless explicitly converted to swing** (relabel `intraday → carryover/swing`, **reduce risk**, require next-day revalidation). The +17R says don't hard-flatten everything at EOD — but it must be a *deliberate, relabeled, smaller-risk* hold, not a silent one.
- next-day reset around earnings/macro.

**Guardrails:** don't "close everything at night" (carry is net-positive); the fix is **labeling + revalidation + expiring dead trades sooner**, not blanket EOD liquidation.

## Verdict
`RECENT_LOSSES_REQUIRE_INTRADAY_EXPIRY_FIX` applies as a **risk-hygiene** fix (mostly stocks), not a P&L rescue: add max-trade-age + RTH-aware expiry + explicit relabel-to-carryover with reduced risk + next-session revalidation. Medium priority; validate forward.
