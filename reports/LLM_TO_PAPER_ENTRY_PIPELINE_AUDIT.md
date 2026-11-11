# LLM Routine → Signal Candidate → Continuous Paper-Entry Pipeline — Audit

**Date:** 2026-06-19 ~09:54 UTC · **Type:** read-only architecture audit (code + DB + logs). **No trading logic / scoring / TP-SL / routing / filters / live changed.**

## TL;DR
The pipeline is **candidate-then-continuous-monitor**, fully deterministic. The LLM (Opus/Sonnet) is a **read-only advisory layer** and is **not in the signal-creation or entry-trigger path**. Entry is detected by a deterministic OHLCV walk that **re-evaluates full history each pass**, so it is **gap-tolerant** — a monitor gap delays the live alert but does not lose the classification. **No entry-touch bug found.**

---

## A. How does it really work now?
**Candidate → continuous monitor.** Not immediate-entry, not review-only, not Opus-gated.

1. A **deterministic scanner** produces trade ideas (scoring/technical agents) and registers them:
   - `src/agents/supervisor.py:1027` → `register_ideas()` → `src/signals/registry.py:361` `store.upsert_proposed_signal(...)`, initial **`status = waiting_for_entry`** (`registry.py:293`, `STATUS_WAITING` in `src/signals/models.py`).
   - Crypto candidates come from the **watchlist monitor** (`report_id` prefix `watchlis…`); stocks from the **stocks intraday pipeline** (`report_id` prefix `stocks_i…`). DB confirms: **no `report_id` is ever an LLM/Opus run.**
2. The signal then **waits**. A deterministic **tracker** walks OHLCV candles and flips the status when a candle's high/low overlaps the entry zone / trigger.
3. Entry is checked **continuously between 2h cycles** (fast pending pass) — not only at the next review.

So: **B (candidate-then-monitor).** Opus does **not** open trades.

## B. Who makes the final paper-entry decision?
Two deterministic components — **no LLM**:
- **Entry-touch detection:** `src/signals/tracker.py` `_evaluate_signal_walk` / `_classify`. Zone touch (`tracker.py:266-280`: `low <= hi and high >= lo`) or trigger touch (`:282-289`). Sets `triggered / triggered_at / entry_price`.
- **Actionability gate + alert:** `src/notifiers/paper_entry.py` `decide_paper_entry` (blocks C-tier and scalp) → `send_paper_entry_alert` fires the Telegram paper-entry alert only for actionable (non-scalp, B/A) signals.
- **LLM is explicitly read-only/advisory:** `prompts/llm_review/enriched_market_review_protocol.md` §PART 16 ("read-mostly, advisory-only; may write only `OPUS_ENRICHED_REVIEW_*.md`; forbidden to modify scoring/agents/auto-trade"), and the scheduler self-guards against any LLM token in the plan (`scripts/run_default_market_schedule.py:1178`, "no Opus/Claude tokens in plan").

## C. How often is entry actually checked?
- **Full `track-signals` pass:** once per scheduler cycle (**`--interval-hours 2`**), at cycle start.
- **Fast pending-only pass (tier A/B, non-terminal):** `tracker.py` `track_pending_entries()` — every **5 min (crypto)** / **10 min (stocks)** inside the **90-min monitor window** per cycle (`run_default_market_schedule.py` crypto monitor `--interval 300`; stocks `--interval-minutes 10 --market-hours-only`).
- **Price source:** **OHLCV candles, not live tick** — crypto `5m/15m/1h` and stocks `15m/1h/1d` by mode (`tracker.py` `TIMEFRAME_PREFERENCE`).
- **Gap-tolerance (key):** the tracker **re-walks the full candle history from `created_at` on every pass**, trimming at `expires_at`. So a missed window is recovered retroactively — the classification is correct even after a gap; only the *live alert* is late.
- **Live state (06-19 09:54 UTC):** scheduler alive, **uptime ~18h**, cycles every ~2h (`CYCLE 7 END ok=20 failed=0`), heartbeat `problems: []`. The persistent runner (`CryptoAIDeskMonitor`) + watchdog (`CryptoAIDeskHeartbeat`) from yesterday's fix are holding; no gaps since.

## D. Can the 2h Opus review cause a missed entry?
**No.** Opus/Sonnet is not in the entry path at all. Entry detection is deterministic, OHLCV-driven, and runs independently of any LLM review (every 5/10 min within the window + every cycle, with retroactive re-walk). The 2h review cadence affects only the **advisory markdown/Telegram**, never entry timing.

## E. Are there cases where price touched the entry zone but paper did not enter?
**Verified against the DB (entry_triggered flag by terminal status):**

| status | entry_triggered=1 | entry_triggered=0 | meaning |
|---|---|---|---|
| `expired` | **483** | 0 | entry **was** touched → trade opened, just no TP/stop before validity end (entered, not a miss) |
| `stopped` / `triggered` / `tp1_hit` | all | 0 | entered |
| `missed_no_entry` | 32 | **340** | mostly never touched |
| `stale_before_entry` | 35 | **169** | mostly never touched |
| `entry_moved_away` | 17 | 26 | price drifted off the zone |

Recent samples (06-19): ETH/ZEC/BTC scalp `expired` → `trig=1, alerts=2` (entered + alerted); SUI/AVAX/stocks `stale`/`moved_away` → `trig=0, alerts=0` (genuinely no touch → correctly no entry).

**So the only "touched but not paper-entered" cases are by design:**
- **review-only / C-tier / scalp** signals: tracker may mark them triggered, but `decide_paper_entry` suppresses the actionable alert (DB: C-tier stale had `alerts=0`). Not a bug — that's the shadow/non-actionable policy.
- A small **historical** set (`stale`/`missed` with `entry_triggered=1`: 35+32) is a labeling nuance (touch detected on a later re-walk / near the expiry boundary), **not** a live paper miss. Worth a Friday note, not a fix.

## F. If touched-but-not-entered — what is the cause?
- **review-only tier (C-tier / scalp)** → by design (actionability gate). ✅ primary explanation.
- **monitor gap** → causes a **late live alert**, but the tracker's full re-walk recovers the classification (entered/expired marked retroactively). For short-validity **scalp** (2h window) a long gap can make the alert useless even though the label is correct. The 06-18 12:29→15:39 UTC gap is now closed by the persistence fix.
- **OHLCV granularity** (15m intraday candles): intra-candle touches are still captured via candle high/low; a true miss only happens if the OHLCV archive lacks candles for that window (data gap), not a logic error.
- **bug:** none found in entry-touch logic.

## G. What needs fixing now (if any bug)?
**No correctness bug to fix.** Trade logic is sound and gap-tolerant. One **optional, non-urgent enhancement** (Friday review, NOT a trade-logic change): the live paper-entry **alert** has a small blind spot — the fast pending pass runs only inside the 90-min monitor window, leaving ~30 min/cycle uncovered for *real-time* alerts (classification is still recovered next pass). If lower alert latency is desired, consider running the pending-only A/B pass continuously across the full 2h interval. This affects alert timeliness only, not entry classification or any trade math. **Recommend: leave as-is until the forward test on the now-stable monitor produces evidence.**

## H. What must NOT change
scoring · TP/SL · routing/actionability tiers · entry-touch logic · scalp-off · C-tier-shadow · filters · live/auto-live · BE/partial/trailing · strategy math. This was a read-only audit; nothing above was touched.

---

## Verdicts
- **PIPELINE_OK_CANDIDATE_THEN_CONTINUOUS_MONITOR** ✅ — deterministic candidate → continuous OHLCV monitor.
- **LLM_NOT_IN_EXECUTION_PATH** ✅ — explicitly clears `PIPELINE_RISK_LLM_TOO_CLOSE_TO_EXECUTION` (Opus is read-only/advisory).
- **ENTRY_TOUCH_MISSED_NEEDS_FIX** ❌ — not observed; non-entries had `entry_triggered=0` (no touch) or were review-only/C-tier by design.
- **MONITOR_GAP_EXPLAINS_LATE_ALERTS** (partial) — gaps delay *live alerts*, not classification (tracker re-walks history); the 06-18 gap is now closed.
- **NO_TRADE_LOGIC_CHANGE** ✅
