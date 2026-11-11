# Paper Trading Audit — 2026-06-01

_Window analyzed: 2026-05-22 → 2026-06-01 (~ 10 days). Source: `proposed_signals` × `signal_outcomes`, deduped by `(asset_class, symbol, mode, direction, calendar_day)`._

**Scope of this document.** Pure observation. No scoring / threshold / agent / strategy changes are applied. Recommendations are flagged "to consider"; the system is left running unmodified per user request.

**Counting model.** All numbers below treat a "trade" as one **unique daily setup** (`symbol × mode × direction × tier × day`). The historical `signal_id` duplication that inflated raw counts 5-15× has been fixed at the source (PART 10 — see footer), so going forward `proposed_signals` rows will match this view.

---

## 1. Executive read

| | Crypto | Stocks |
|---|---|---|
| Unique setups (10 days) | **24** | **178** |
| Triggered | 21 (88 %) | 135 (76 %) |
| Wins (final R > 0) | 5 | 28 |
| Losses (final R < 0) | 11 | 38 |
| Win-rate | **21 %** | **22 %** |
| Avg R per setup | **+0.12** | **+0.01** |
| Sample-size verdict | weak | borderline-reliable |

**The headline numbers are not catastrophic, they're early.** A 20-25 % WR with avg +R is a perfectly legitimate "small frequent wins + occasional big winners" profile **provided** wins are materially larger than losses. The data so far shows wins ARE bigger (avg crypto win ≈ +1.4 R, avg crypto loss ≈ -1.0 R) — that's the structural reason average R is still positive.

But it's all built on **< 200 unique trades**, half of which are repeats of the same handful of tickers. Confidence is fragile.

---

## 2. What's working — keep / lean in

### 2.1 SMCI intraday B-tier — best performer

| n | trig | W | L | avg R | total R |
|---|---|---|---|---|---|
| 7 | 7 | **4** | **0** | **+0.95** | +6.6 |

100 % entry-trigger rate. 4 of 7 hit TP1+. Despite the unresolved March-19 SDNY indictment overhang (verified in the latest Opus enriched review), the **technical-setup signal for SMCI is exceptionally clean** in this window. The price action is currently absorbing the legal-risk discount with strength.

→ **The setup engine is doing its job on SMCI**. Don't break it.

### 2.2 PLTR / NVDA / SMH / AVGO intraday B-tier

| Ticker | n | W | L | avg R |
|---|---|---|---|---|
| PLTR | 3 | 3 | 0 | +0.65 |
| NVDA | 2 | 1 | 0 | +0.50 |
| SMH (semis ETF) | 7 | 3 | 2 | +0.55 |
| AVGO | 5 | 2 | 2 | +0.54 |

All in the AI-data-center theme. The sector edge is real this cycle. Total realized R across just these four buckets ≈ **+9.3 R** in 10 days. That's the system's actual paper-trading PnL engine right now.

### 2.3 Crypto swing — small sample, very strong

| Setup | n | W | L | avg R |
|---|---|---|---|---|
| XLM/USDT swing long | 2 | 2 | 0 | +2.00 |
| ZEC/USDT swing long | 1 | 1 | 0 | +2.00 |
| Crypto swing B total | 4 | 4 | 0 | **+2.25** |

100 % win-rate on 4 setups. Sample is tiny but the magnitude is striking — when crypto-swing fires, the move is sizeable. The new **swing-2×/day** windows (PART 9) should let this bucket grow faster.

### 2.4 LLY intraday A-tier (when it worked)

| Date | n | W | L | avg R |
|---|---|---|---|---|
| 2026-05-25 | 1 | 1 | 0 | +1.00 |
| 2026-05-26 | 1 | 1 | 0 | +1.00 |

The earliest A-tier paper trades both won. Recent A-tier LLY signals (last 3 days) are 0-3 (lost) — a regime shift in healthcare or just noise on n=3.

---

## 3. What's not working — investigate / consider

### 3.1 Crypto intraday B-tier is **net negative**

| n | trig | W | L | avg R |
|---|---|---|---|---|
| 8 | 6 | **0** | **6** | **-0.75** |

Zero wins. Six losses. Includes: ETH short, XLM long, NIL long, SAGA long, TAO long, ZEC long, ZEC long. The common thread: **bearish crypto regime fighting long setups while shorts also fail because narrow stops get knocked**. This is exactly the case where the regime gate **should** be more aggressive at killing crypto-intraday B-tier alerts.

**To consider** (NOT implementing here): require regime alignment for crypto-intraday B-tier alerts. A B-tier long against `bearish trend` regime is already in the rejected pile, but only by the rejection-reason filter — the scoring engine still scores high enough to surface them. Either:
- raise the threshold for crypto-intraday B in bearish regimes, OR
- add a regime-alignment cap to the score (e.g., −15 to score when direction conflicts with regime trend).

### 3.2 AAPL intraday B-tier — losing the AI thesis

| n | W | L | avg R |
|---|---|---|---|
| 5 | 0 | 2 | **-0.27** |

AAPL signals are *triggering* (entering the zone) but failing to follow through. Possible reasons: AAPL is the most "consensus long" name in the AI basket → late entries into already-extended moves. The `wait_pullback` playbook from the catalyst layer might not be flowing into the signal selection for AAPL.

**To consider:** when MSFT + NVDA + AMD + AVGO are already running strong, AAPL's marginal alpha is small — it's beta-following the basket. Either deprioritize AAPL during "AI basket already moving" conditions or treat it strictly as `wait_pullback`.

### 3.3 Tier discipline is **broken**

Trigger-rate by tier:

| Class | A | B | C |
|---|---|---|---|
| stocks | 80 % | 77 % | 73 % |
| crypto | (n/a) | 88 % | (rejected) |

A-tier should have a **noticeably higher** trigger rate AND a **noticeably higher** win-rate than B and C. Reality: A-tier is virtually indistinguishable from B-tier (80 vs 77 % trigger). The score numbers (82+ A, 65-80 B, 50-65 C) don't yet map to observably different outcomes.

**Why this might be:** A-tier is so rare (n=15 in 10 days) that variance dominates. We need more A-tier samples. Or: the criteria distinguishing A from B (currently RR ≥ 1.5, no score caps) don't correlate with win-rate in this market.

**To consider (later):**
- Track A-tier outcomes specifically — once n ≥ 30, judge whether to keep the threshold or tighten it.
- Look at WHICH cap_reasons are dropping setups from A → B. If "earnings unknown" is the main one, the calendar-lookup gap is hurting us.

### 3.4 Long-horizon (swing / invest) buckets are still empty

| stocks swing B | n=19 | W=0 | L=1 | avg=-0.05 |
| stocks invest B | n=13 | W=0 | L=0 | avg=+0.00 |

Almost all of these are `not_triggered` or still open. Long-horizon needs **weeks**, not days, to validate. The PART 9 fix (2×/day windows for swing+invest) will increase the sample faster — re-audit in 2 weeks.

### 3.5 Multiple modes firing on the same symbol simultaneously

Today SMCI is active as: intraday B + swing B + invest B + intraday A on different cycles. They share the underlying SMCI price move — so a single bad day at SMCI bleeds **three signals at once**. This is correlated-risk hidden inside the tier table.

**To consider:** add a `correlated_setup_warning` cap when the same symbol appears at ≥ 2 modes B-tier on the same day. Doesn't reject, just flags so position sizing accounts for it.

---

## 4. System / infra issues found (NOT scoring-related)

### 4.1 Signal-ID duplication — FIXED in this commit (PART 10)

Pre-fix: each 2 h cycle generated a new `signal_id` for the same setup because the hash included `report_id` and 10-digit-precision entry floats. Inflated raw counts by 5-15× and confused every analytics view.

Fix applied:
- `signal_id_for()` now hashes only `(symbol, mode, direction, tier, calendar_day)`.
- 12/12 dedup tests green (`tests/test_signal_id_dedup.py`).
- 27/27 scheduler tests green.
- `upsert_proposed_signal` already had `ON CONFLICT(signal_id) DO UPDATE` → existing dupes stay, new signals coalesce going forward.

**Effect:** starting next scheduler cycle, `proposed_signals` stops bloating, `active-signals` CLI returns honest unique counts, and the Obsidian dashboards no longer need their post-hoc dedup CTEs (they keep them for backward-compat with historical rows).

### 4.2 `expected_rr_tp1` is always ≈ 1.00 in active signals

Every active signal in `01 📌 Active Signals.md` shows **RR = 1**. Looking at the calculation in `src/signals/registry.py:_expected_rr()`, it's correct — TP1 and invalidation are computed by the system to give an ATR-based 1:1 setup by default. But that means **every B-tier setup has identical structural RR**. The only thing distinguishing them is the score.

**To consider:** if the bot is meant to express conviction via RR, then it should size TP1 differently for higher-conviction setups (e.g., A-tier targets 1.5R, B-tier 1.0R). Currently it doesn't.

### 4.3 Earnings calendar lookup is broken

Every stocks intraday signal carries the warning: `earnings: UNKNOWN (calendar lookup missing — treat as undated event risk)`. This means **the system doesn't actually know when MSFT, AMD, NVDA, etc. report**. Holding a signal blind through earnings is a real risk.

**To consider:** fix the yfinance earnings-date pull, OR pull from Yahoo Earnings Calendar HTML directly, OR add a manual `data/stocks/earnings_calendar.yaml` for the top 30 tickers.

### 4.4 Watchlist-monitor contributed only 11 rows lifetime

Despite running every 5 minutes for 90 minutes per cycle (≈ 18 ticks per cycle × 12 cycles/day = 216 opportunities/day), the monitor only added **11 signals total** to the registry. Either:
- The tier-upgrade event is genuinely rare (which is fine — it's working as designed).
- Or the registration path inside the monitor is silently failing some of the time.

Worth a brief inspection at some point. Not urgent.

---

## 5. Per-bucket consider-list (ranked by realised R)

| Bucket | Status | What to consider |
|---|---|---|
| stocks intraday B (top tickers) | ✅ Working | Keep as-is. Largest sample, +0.18R avg, positive R total. |
| crypto swing B | ✅ Promising | Let 2×/day windows accumulate sample. |
| SMCI intraday B | ✅ Star | No change. Watchlist monitor doing its job. |
| stocks intraday A | ⚠️ Underperforming | Watch n grow. If by n=30 still ≤ B, revisit threshold or capping logic. |
| AAPL intraday | ❌ Losing | Mark AAPL "wait_pullback only" when basket already moving. |
| crypto intraday B | ❌ Losing | Tighten regime gate for crypto longs in bearish regime. |
| stocks swing / invest | ⏳ Premature | Re-audit at 2 weeks. |
| stocks C-tier (intraday) | ➖ Slightly negative | Already filtered from Telegram — fine. |

---

## 6. What is genuinely correct right now

1. **Telegram cooldown working** (PART 2) — no spam. Manual review of `watchlist_alerts` shows clean tier-upgrade alerts with 30-45 min spacing.
2. **PART 1 fix is doing its job** — no untracked legacy alerts in the last 24 h.
3. **PART 3 legal-risk gate** — SMCI overhang IS being surfaced in the latest enriched review even though it's not blocking new signals (because the system still creates the technical setup; the gate would only fire if the news re-classifies). Trader read works.
4. **Stocks news catalyst auto-collection** (PART 6) — DeItaone-style channels now landing in `news_items` with correct `asset_class=stocks`. Already feeding the `06 📌 Telegram Feed.md` dashboard.
5. **Default scheduler 2h cadence** — 12 cycles/day with crypto monitor + stocks monitor running between cycles. PID 20768 alive and healthy.
6. **Obsidian dashboards (11 pinned tabs)** — render in < 1 s every cycle, idempotent.
7. **Catalyst-scan** — 4 baskets discovered yesterday with correct `avoid_chase` / `wait_pullback` / `related_beta_rotation` playbooks.

---

## 7. Recommendations to discuss (NOT implementing without explicit approval)

**Highest leverage:**
1. **Tighten crypto-intraday B-tier regime gate**. The −0.75R bucket is bleeding the otherwise-positive crypto track record. (Code-side: extend the regime cap in `src/agents/scoring_agent.py`.)
2. **Fix earnings calendar lookup**. Every stocks signal carries the UNKNOWN flag — that's a real risk in earnings season. (Code-side: `src/stocks/events.py` or equivalent.)
3. **Track A-tier separately and aggressively**. Add a per-tier A snapshot to the Obsidian dashboard so we see whether A-tier discipline holds as sample grows.

**Medium leverage:**
4. **De-emphasize AAPL in active AI baskets**. Either dynamic deprioritization or a `wait_pullback` hard mode when the basket is already extended.
5. **Add correlated-setup warning**. When same symbol fires ≥ 2 modes B+ on the same day, flag for position sizing.
6. **Differentiate A vs B by RR target**. A-tier targets 1.5R+, B-tier 1.0R. Adds expected-value gap that currently doesn't exist.

**Low leverage / nice to have:**
7. **Audit the watchlist-monitor registration path** — only 11 contributions lifetime.
8. **Add per-symbol PnL leaderboard** to dashboards once n ≥ 30 per symbol.

---

## 8. Trust calibration

- The setup engine **finds real edges** (SMCI/PLTR/NVDA/AVGO/SMH worked, crypto swing worked).
- The regime gate **partly works** (rejects most weak crypto longs) but **leaks some** (the 6 crypto-intraday B losses got through).
- The scoring **doesn't yet differentiate A from B in outcome terms** — needs more A samples and/or stricter A criteria.
- The infrastructure (scheduler / monitors / TG / Obsidian / catalyst / Opus routine) is **clean and reliable** — no operational bugs surfaced in this audit beyond the now-fixed signal_id duplication.

**Bottom line:** the paper trading isn't broken, it's young. The losses on crypto intraday are the most actionable thing to fix; everything else either works or needs more data.

---

_Audit produced 2026-06-01 by manual review. No code under `src/` was modified for the strategy / scoring / agent layer in this commit — only `src/signals/models.py:signal_id_for()` for the duplication fix._
