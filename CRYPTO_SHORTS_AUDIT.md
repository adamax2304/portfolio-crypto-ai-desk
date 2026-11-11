# Crypto Shorts Audit

**Date:** 2026-05-29. Read-only. No code/scoring/threshold changes. No auto-trade.

---

## Executive Summary

**Crypto shorts are NOT disabled and ARE being generated.** The perceived "no shorts" is a combination of two real effects:

1. **(A) Correct no-trade** — today's downtrend is a *shallow, low-volume grind* (alts −1% to −2.5%, volume below average). The few names that moved enough are *overextended* (>2 ATR, "do not chase"), and several lack derivatives data. So most short candidates correctly fail universal quality gates. Shorting a crowded, low-volume grind is a squeeze trap.
2. **(D) Untracked legacy short alerts** — the shorts that DID qualify (UNI/USDT B 65.5, BCH/USDT B 72.1) were **sent to Telegram via the legacy `watchlist_alerts` path but never registered into `proposed_signals`.** So they vanish from `active-signals` and `signal-stats`, making it *look* like the system produces no shorts when it actually produced 2 B-tier shorts today.

**Verdict: E (mixed) — dominated by A + D.** Not B (shorts are not disabled by design); not primarily C (filters are not anti-short — they apply the same gates to longs).

---

## PART 1 — Crypto direction logic

| File | Setting / logic | Effect on shorts |
|------|-----------------|------------------|
| `config/` | **No** `allow_shorts` / `long_only` / `direction_filter` / `spot_only` flag anywhere | Shorts are **not disabled** by config |
| `src/agents/momentum_scanner_agent.py` (L95–116) | Computes `short_score` from negative RS-vs-BTC (±8 ×1.4), volume-ratio bonus, `close<ema20<ema50` (+12), "breakdown" tag (+8), and **−6 penalty if overextended & distance_atr < −2**. bias="short" only if `short_score > long_score AND short_score ≥ 50` | Shorts require *real* downside momentum + structure; **already-crashed names are penalized** (anti-chasing) |
| `src/agents/technical_setup_agent.py` (L68–129) | Builds full short setup: entry/invalidation/TP for `direction=="short"` | Shorts get complete setups (symmetric with longs) |
| `src/agents/scoring_agent.py` (L31, L196–225) | Regime alignment: short in **bearish trend = 0.88** (full bonus), transition/range = 0.58, bullish = 0.25. Funding cap: short capped at 78 if `funding < −0.001` ("crowded short") | Shorts **rewarded** in bearish regime, but **capped when funding is very negative** (squeeze risk) |
| `src/agents/risk_agent.py` (L48–66) | `short in bearish trend` → **no penalty**. `long in bearish trend` → +25. Universal gates: volume<0.5 → +8; >2 ATR → +12; RR<1 → +14; no invalidation → +25 | Risk engine treats shorts **fairly** in downtrend; rejections come from universal quality gates, not anti-short bias |
| `src/agents/market_regime_agent.py` | Produces label `bearish trend (risk-off)` today; style "short bias or no trade" | Regime correctly flags short-friendly environment |
| `src/signals/registry.py` (`_qualifies_for_tracking`) | A/B long/short qualify; registration is a separate step | Shorts *qualify* — but only if the report path actually calls `register_ideas` (see Part 3) |
| `src/agents/supervisor.py` (L678) | Alert filter: `tier in {A,B} and direction in {long,short}` — sends BEFORE register (L481 vs L482) | Short alerts can be SENT before/ without registration |
| `src/agents/watchlist_monitor.py` | Sends `watchlist_alerts` directly; **no `register_ideas` call** | Monitor short alerts are **untracked by design** |
| `src/reports/report_builder.py` | A/B/C buckets include both long & short; **no dedicated short section / short watchlist** | Shorts shown inline, no special surface |

**Conclusion:** every layer supports shorts. There is no `long_only` switch. Shorts are a first-class direction.

---

## PART 2 — Recent rejected crypto candidates (latest scalp, bearish regime)

Regime: **bearish trend (risk-off)**. Rejected breakdown:

| Symbol | dir | score | Primary rejection reason |
|--------|-----|------:|--------------------------|
| ALLO, IO, ID, INJ, AIGENSYN, XLM, FET, NEAR, XPL | **long** | 25–46 | "Long setup conflicts with current market regime" (+ weak volume / missing derivatives) — **correct: longs killed in downtrend** |
| **FIL/USDT** | **short** | 46.2 | Derivatives unavailable; volume below average; breakout confirmation weak → **below 50, missing OI/funding** |
| **TON/USDT** | **short** | 30.1 | "Price >2 ATR from EMA20; do not chase; move extended" → **overextension penalty** |

**Top short-rejection reasons:**
1. **Shallow move / low momentum** — weakest alts are only −1% to −2.5% (MEGA, FIL, SUI, TRX, UNI); negative RS too small to push short_score past 50.
2. **Volume below average** — no breakdown confirmation (the −8/+8 volume gate fails).
3. **Overextension** — the names that DID drop hard (TON) are >2 ATR below EMA20 → "do not chase."
4. **Missing derivatives data** — FIL/TON have no OI/funding → short conviction can't be confirmed.
5. **Crowded-short funding cap** — negative funding ("shorts may be crowded") caps several at 78.

This is a **grinding, low-volume, crowded-short downtrend** — exactly the environment where clean short *entries* are scarce. The rejections are legitimate quality gates, not anti-short bias.

---

## PART 3 — Untracked short alerts (the real gap)

Detector `scripts/detect_untracked_legacy_alerts.py --since 2026-05-29`:

| symbol | tier | mode | dir | score | sent_at (UTC) | trackable |
|--------|------|------|-----|------:|---------------|-----------|
| **UNI/USDT** | B | scalp | **short** | 65.5 | 08:36 | ❌ NO |
| **BCH/USDT** | B | scalp | **short** | 72.1 | 08:45 | ❌ NO |
| XLM/USDT | B | swing | long | 65.4 | 10:56 | ❌ NO |
| INJ/USDT | B | swing | long | 66.1 | 11:36 | ❌ NO |

**Key finding: the system DID produce 2 B-tier crypto shorts today (UNI, BCH).** They were:
- Generated (B-tier, score 65.5 / 72.1) ✅
- Sent to Telegram (legacy `watchlist_alerts`) ✅
- **NOT registered in `proposed_signals`** ❌ → invisible to `active-signals`, `signal-stats`, `track-signals`.

**Why not registered:** they came through the legacy alert path (monitor-watchlist and/or supervisor alert-before-register). `WatchlistMonitor` never calls `register_ideas`; the supervisor sends the alert at L481 before registering at L482, and registration can drop an idea whose `raw.setup` lacks full entry/invalidation. Either way → no trackable row. (Documented in `CRYPTO_ALERT_REGISTRATION_AUDIT.md`.)

**Consequence:** crypto short performance is **systematically under-recorded.** Every legacy short alert is a blind spot. The crypto PF (0.0, −5R, 0 wins) does NOT include UNI/BCH shorts — so crypto stats are incomplete in BOTH directions.

---

## PART 4 — Report-generated vs monitor-generated shorts

| Path | Generates shorts? | Registers to proposed_signals? | Trackable? |
|------|-------------------|--------------------------------|-----------|
| `scalp-report` | ✅ yes (FIL, TON appeared as short candidates) | ✅ if they clear A/B + have setup | ✅ when registered |
| `intraday-report` | ✅ yes | ✅ same | ✅ |
| `monitor-watchlist` | ✅ yes (UNI, BCH B shorts came via this path) | ❌ **never calls register_ideas** | ❌ untracked |

**Inconsistency confirmed:** reports register their A/B shorts; the **watchlist monitor alerts shorts but does not register them.** So a short that flips to B/A *between report runs* (caught by the monitor) gets a Telegram alert but no trackable signal. This is the asymmetry that hides crypto shorts from stats.

---

## PART 5 — Verdict

**E. Mixed issue — dominated by A (correct no-trade) + D (untracked legacy shorts).**

- ✅ **Not A-only:** the system isn't purely "no clean setups" — it found UNI/BCH B-tier shorts.
- ❌ **Not B:** shorts are fully supported; no design-level disabling.
- ⚠️ **Partly C, but not the main cause:** filters are strict (overextension, volume, derivatives, crowded-funding cap) but they apply equally to longs; they are not anti-short. In a shallow low-volume grind they correctly reject most shorts.
- ✅ **Strongly D:** the qualifying shorts (UNI, BCH) are lost because the monitor/legacy path doesn't register them → they never reach `signal-stats`, so the system *looks* short-blind when it isn't.

**Plain English:** the downtrend is real but *orderly and low-volume with crowded shorts*, so high-quality short entries are genuinely scarce (correct). The shorts that DO qualify are being alerted but silently dropped from tracking (a real gap).

---

## PART 6 — Recommendations (no code changes yet)

Ordered by value:

1. **Migrate legacy short alerts into `proposed_signals`** (highest priority) — the same fix already queued in `CRYPTO_ALERT_REGISTRATION_AUDIT.md`. Until this lands, crypto shorts (and longs) from the monitor path are untracked, and crypto PF/winrate is meaningless. **Do this first, after the scheduler finishes.**
2. **Add short-rejection diagnostics** — a small "Rejected Shorts" sub-section in the crypto report listing, per short candidate, which gate failed (volume / overextension / missing-derivatives / funding-cap). Makes "why no shorts" auditable without code spelunking. Read-only reporting change.
3. **Add a separate crypto-short watchlist** — surface near-miss shorts (short_score 45–55, or B-tier-but-overextended awaiting retest) so you can watch for a clean entry instead of losing them.
4. **Do NOT lower short thresholds yet** — there is no performance data to justify it (shorts are untracked, sample = 0 tracked shorts). Lowering gates now would just add low-quality shorts in a squeeze-prone, crowded-funding tape. Only revisit after #1 gives real short PF data.
5. **Leave momentum/risk/scoring short logic as-is** — it is correctly rewarding shorts in bearish regime (0.88 alignment, no risk penalty) and correctly avoiding overextended/crowded shorts. No change needed.

**Sequencing:** (1) after scheduler finishes → migrate/registration fix; then collect tracked short outcomes for ~2 weeks; THEN decide on #2–#4 with data.

---

## Safety

- No code, scoring, thresholds, agents, or strategy changed.
- Detector + reads only.
- No auto-trade. Scheduler not interrupted.
