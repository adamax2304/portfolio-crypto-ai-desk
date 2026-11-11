# System Audit — 2026-06-03 14:00 EEST

Comprehensive 7-area audit of the crypto-ai-desk system. Read-only
inspection. No code changes to `src/`, `tests/`, `scripts/`, or `config/`.
Where bugs are confirmed but require code changes, they are surfaced as
TODOs in §9 for a separate manual session per the PART 16 contract.

---

## 1. Infrastructure / Process Health — ✅ GREEN

| Component | Status | Evidence |
|---|---|---|
| `CryptoAIDesk_Scheduler` (Windows Task) | **Running** | PID 10420, alive 18.3 h. Last cycle 7 (12:25–12:35 EEST) ok=16 failed=0. |
| `CryptoAIDesk_TelegramCollector` (Windows Task) | **Running** | PID 4912, alive 20 h. 18 channels resolved. |
| Crypto watchlist monitor (in-cycle) | **Running** | PID 8156 spawned 12:35, still alive (~90 min lifetime) — **PART 13 fix confirmed working** |
| Stocks watchlist monitor (in-cycle) | **Running** | PID 25928 spawned 12:35, lifetime ~90 min. `--market-hours-only` will gate ticks. |
| Opus auto-review routine | **Enabled** | 4 reviews today (00:52, 02:12, 11:14, 13:55). Next cron at 16:38 EEST. |
| Default scheduler cycle | **Running normally** | Last 7 cycles all `ok ≥ 15 / failed ≤ 1`. No timeouts since PART 14c (1800s bump on 06-02 18:48). |

No process crashes. No autorestart-loop triggers. No DLL init failures.
No FloodWait. No SQLite lock contention.

---

## 2. Error Surface — ✅ CLEAN (since PART 14)

Scheduler log error grep (last 24 h):

- **Pre-PART 14c (before 06-02 18:48):** 5 crypto-scalp timeouts at the
  old 900 s ceiling + 3 `exit=1` on `track-signals` and the failed
  intraday at 06-02 10:33. **All before the 1800 s bump.**
- **Post-PART 14c:** zero timeouts, zero `exit=1`, zero Tracebacks.

Cycle 7 (12:25 EEST today): every step exit=0. Total cycle wallclock
~35 min. Comfortably inside the 2 h interval.

---

## 3. Signal Pipeline — ✅ GREEN, with one regression

### 3.1 Today's registered signals (deduped by setup)

| asset | mode | tier | dir | n |
|---|---|---|---|---|
| stocks | intraday | A | long | **1** ← SMCI (regression — see §3.2) |
| stocks | intraday | B | long | 8 |
| stocks | intraday | C | long | 3 |
| stocks | swing | B | long | 7 |
| stocks | swing | C | long | 6 |
| stocks | invest | B | long | 6 |
| stocks | invest | C | long | 5 |
| crypto | (any) | A/B/C | any | **0** |

Crypto **zero signals today** — correct behaviour. BTC ATR percentile 100,
trend downtrend, regime = `high-volatility danger`. The system is right
to produce no-trade, and Opus reviews confirm this verdict.

### 3.2 SMCI A-tier regression — ❌ HIGH-PRIORITY DEFECT

The 13:55 Opus auto-review correctly flagged this. Independent
verification from this audit:

- **11 SMCI-tagged news rows in `news_items`** including:
  - 2026-03-19 SMCI 8-K + 2026-03-20 Form 8-K (SDNY indictment, Liaw resignation)
  - 2026-03-26 StocksToTrade indictment coverage
  - 2026-04-07 Supermicro IR investigation update
  - 2026-05-12 Hagens Berman class action filing
  - 2026-05-26 Faruqi & Faruqi class-action final deadline
  - 2026-05-06 / 2026-05-05 Q3 FY2026 results + 8-K
- **0 SMCI catalyst events generated today.** The catalyst-scan
  lookback window only sees fresh news (~12–24 h); the legal-flag
  context is "old" by that metric and stops reaching the scoring path.
- Today's score evolution:
  - 01:06 intraday B 71.26 → 01:25 swing B 72.5 → 01:29 invest B 67.82
  - **09:35 intraday A 82.26 (high confidence)** ← canonical PART 3
    legal-gate regression. Tier moved the wrong way (B→A).
- All-time SMCI A-tier outcomes (n=2): **AvgR −0.17, TotalR −0.33.**
  The system has no edge here yet it keeps promoting the name.

This is the textbook case PART 3 was added to catch and is the most
important finding of this audit. **Fix is a code change → §9 TODO.**

### 3.3 Tracked outcomes (last 24 h)

- 82 triggered/closed signals.
- 1 win, 5 losses, 37 expired, remainder open.
- High `expired` ratio reflects: tight intraday entry zones + soft
  US tape during after-hours window (US RTH still closed today at audit time).

---

## 4. Telegram Alerts — ✅ DELIVERED CORRECTLY

### 4.1 Crypto watchlist tier-upgrades (last 24 h): **0**

Correct. No crypto setups crossed B/A threshold during the danger
regime. The monitor IS running (verified PID 8156 lifetime).

### 4.2 Stocks signal_alerts (last 24 h): **15**

Status distribution:
- **9 `tg=sent`** (real Telegram delivery) during yesterday's US RTH
  (17:41–18:59 EEST): AMD, NVDA, SMH, SMCI, AVGO entry_change /
  score_improvement / invalidation_change.
- **5 `tg=dry_run`** at 23:34–23:35 06-02 — left over from the
  manual smoke run I executed at the end of yesterday's session
  (not a routine bug; one-time test residue).
- **1 prior** during the 17:41 cluster also `tg=sent`.

Watchlist monitor PART 13 fix confirmed working (lifetime 90 min
sustained) — alerts genuinely fire on tier upgrades / score
improvements within the active monitor window.

### 4.3 Telegram channel ingestion (last 24 h): **106 messages**

- `t.me/WalterBloomberg` (stocks): 54 — macro/Trump/Iran headlines.
- `t.me/lookonchain` (crypto): 52 — on-chain whale moves.

Other 16 channels were quieter (weekend behaviour or off-cadence).

---

## 5. Obsidian Dashboards — ✅ GREEN (synced every cycle)

All 11 pinned dashboards refresh at the end of every cycle. Latest
mtime = **2026-06-03 12:35 EEST** (cycle 7 tail step `refresh obsidian
dashboard` exit=0 in 1.4 s).

| File | mtime | content |
|---|---|---|
| `00 📌 Dashboard.md` | 12:35 | MOC index links |
| `01 📌 Active Signals.md` | 12:35 | Current B/A waiting/triggered |
| `02 📌 Trade History.md` | 12:35 | Closed signals + outcomes |
| `03 📌 Todays Catalysts.md` | 12:35 | 4 baskets + top 30 events |
| `04 📌 Latest Reports.md` | 12:35 | Report links |
| `05 📌 Opus Auto Reviews.md` | 12:35 | OPUS_ENRICHED_REVIEW_* index |
| `06 📌 Telegram Feed.md` | 12:35 | 50-most-recent TG msgs |
| `07 📌 Schedule Status.md` | 12:35 | Live process health |
| `08 📌 Rejected Ideas.md` | 12:35 | 48 h reject reasons |
| `09 📌 Macro Risk Heatmap.md` | 12:35 | risk-on/off score |
| `10 📌 Performance by Mode.md` | 12:35 | mode × tier edge table |

---

## 6. Opus Auto-Review Quality — ✅ MATURING, with one consistent gap

### 6.1 Cadence — running, with some catch-up lag

Expected cron fires today: 00:30, 04:30, 08:30, 12:30 (+jitter ~9 min).
Observed today: 00:52, 02:12, 11:14, 13:55.

- 00:52 — close to scheduled 00:30+jitter ✓
- 02:12 — anomalous extra fire (likely manual `Run now` or a catch-up
  for a missed 00:30 slot). Not harmful.
- 11:14 — 08:30 slot missed, ran ~2h45m late (probable Claude Desktop
  was closed at 08:30, fired at next launch).
- 13:55 — 12:30 slot ran ~85 min late.

Conclusion: the routine is firing reliably **when Desktop is open**. The
catch-up behaviour is the documented Claude scheduled-task pattern.

### 6.2 Quality of latest review (13:55) — strong

- Correctly identified SMCI A-tier regression and demoted it to
  AVOID / MANUAL REVIEW REQUIRED (this is exactly the PART 16 escape
  valve in action).
- Cited 11 SMCI news rows and verified externally (SEC EDGAR, indictment
  date, class action, EY resignation).
- Catalyst-coverage diagnostic correctly emitted "weak this run
  (80.4% unmapped) — context only" — PART 15 §H working as designed.
- Diff vs prior 11:14 review properly compared score drift.
- Sources section fully cited with markdown + dates.

The 13:55 review is **PART 15-spec-compliant** and demonstrates the
new contract works.

### 6.3 Persistent gap: catalyst mapping at 80% unmapped

- 1,204 events today, only 64 categorised; 1,140 in `other_news`.
- 11 earnings_event ✓, 9 regulatory_sector_headline ✓, 1 exploit_hack
  (a generic DeFi headline, no symbol). **Zero `legal_risk` events** —
  this is *related to* the SMCI gap but not identical. The classifier
  pattern set covers indictment / SEC / class action; the events
  generated today simply don't carry symbols the entity-matcher
  recognises. Improvement is a code change → §9 TODO.

---

## 7. Paper-Trading Profitability — ✅ Marginally positive, edges concentrated

Unique-setup aggregate stats (all-time, deduped by
`(asset_class, symbol, mode, direction, day)`):

| asset | n | wins | losses | WR | AvgR | TotalR |
|---|--:|--:|--:|--:|--:|--:|
| crypto | 25 | 5 | 9 | 20 % | +0.10 | +2.50 |
| stocks | 225 | 41 | 46 | 18 % | +0.045 | +10.06 |

Both buckets are net-positive. WR ~20 % with positive AvgR =
healthy *small-frequent-wins-plus-occasional-big-winner* profile.

### 7.1 Stocks edge by mode × tier (the workhorses)

| mode × tier | n | trig | wins | losses | WR | AvgR | TotalR |
|---|--:|--:|--:|--:|--:|--:|--:|
| intraday **A** | 17 | 14 | 2 | 7 | 12 % | −0.07 | **−1.20** |
| intraday **B** | 76 | 56 | 22 | 16 | 29 % | +0.20 | **+14.90** ★ |
| intraday **C** | 54 | 41 | 13 | 16 | 24 % | −0.03 | −1.65 |
| swing **A** | 2 | 2 | 0 | 0 | 0 % | 0 | 0 |
| swing **B** | 28 | 24 | 4 | 4 | 14 % | +0.04 | +1.00 |
| swing **C** | 16 | 13 | 0 | 3 | 0 % | −0.19 | −3.00 |
| invest **B** | 17 | 14 | 0 | 0 | 0 % | 0 | 0 |
| invest **C** | 15 | 8 | 0 | 0 | 0 % | 0 | 0 |

**The system's actual edge lives in stocks intraday B-tier (+14.90R on
76 unique setups, WR 29 %).** This was the same finding in the prior
audit two days ago — it has held.

A-tier intraday is still **net negative** (−1.20R on 17 setups). This
matches what the 13:55 Opus review called out about stocks A-tier
underperformance.

### 7.2 Stocks A-tier per-symbol (where A-tier did and didn't work)

| symbol | n | AvgR | TotalR |
|---|--:|--:|--:|
| **LLY** | 2 | +1.00 | +2.00 ← only A-tier winner |
| NVDA | 2 | 0 | 0 |
| TSLA | 1 | 0 | 0 |
| MSFT | 2 | −0.07 | −0.14 |
| AMD | 3 | −0.17 | −0.50 |
| **SMCI** | 2 | −0.17 | −0.33 ← legal overhang biting |
| AAPL | 6 | −0.20 | −1.22 ← most A-tier losses |
| XLK | 1 | −1.00 | −1.00 |

This data **supports demoting SMCI in the scoring path** (§9 TODO):
two prior A-tier SMCI signals already lost money before this fresh
one regressed.

---

## 8. Cross-cutting Findings

### 8.1 What worked since the prior audit
- PART 13 (monitor lifetime) — confirmed via PID 8156 alive 90 min.
- PART 14c (scalp 1800 s) — zero timeouts since the bump.
- PART 14a (BTC-trend-aware market_alignment) — visible in the scalp
  /intraday rejection logs (shorts now alignment-boosted, just below
  the B-tier ceiling because of weak volume + post-move-extended).
- PART 14b (MEXC derivatives fallback) — zero `Derivatives data
  unavailable` rejections in any cycle today.
- PART 15 (auto-review content contract) — the 13:55 review is fully
  spec-compliant.
- PART 16 (permission-light routine) — the routine completed
  autonomously, no permission prompts.

### 8.2 What is broken or weak
- SMCI A-tier despite legal overhang (§3.2). High-priority, code-only
  fix.
- Catalyst symbol-mapping at 80 % unmapped (§6.3). Medium-priority,
  code-only fix in the entity-matcher / classifier interplay.
- Opus routine occasionally catches up late when Desktop is closed
  (§6.1). Operational, not a code issue.
- `signal_alerts.dry_run` residue rows from yesterday's manual smoke
  run still in the DB — purely cosmetic; they're filtered out of
  the §4 "real alerts" view.

### 8.3 What's correctly NOT happening
- Crypto trades during danger regime — system refuses, Opus confirms,
  no false longs.
- No auto-trade. No executions. No fund moves.
- No `news_trader/` writes (read-only respected).

---

## 9. Fix Requests / TODO (for separate manual session)

### TODO-SMCI-legal-gate-regression
- **issue:** SMCI scored A-tier 82.26 today despite a fully-documented
  active legal overhang (SDNY indictment 2026-03-19, EY resignation
  2024-10-30, two class-action filings). PART 3 legal-risk gate is not
  blocking this name.
- **evidence:**
  - `proposed_signals` row at `2026-06-03 09:35` `symbol=SMCI tier=A
    score=82.26`
  - 11 SMCI news rows in `news_items` (date range 2026-03-19 ↔ 2026-05-26)
  - 0 SMCI events in today's `catalyst_events.jsonl`
  - All-time SMCI A-tier outcomes: 2 setups, AvgR −0.17R
- **suggested manual fix:**
  - In the catalyst-scan path, add a **persistent legal-flag carry**:
    once a symbol acquires a `catalyst_type=legal_risk` event with
    severity (indictment / class-action / auditor-resignation /
    SEC-charge), that flag remains attached to the symbol for at least
    90 days (or until an explicit "cleared" event) regardless of news
    freshness.
  - In `scoring_agent.py`, add a hard cap when a stocks A/B candidate
    carries an active legal-flag (cap at 60 = C-tier, similar to PART 11
    regime cap). Cite the legal_flag in `cap_reasons` so the dashboards
    and the Opus review can surface it.
  - Add a regression test: insert an SMCI signal with the active legal
    catalyst → expect tier ≤ C.
- **priority:** high
- **first observed:** 2026-06-03 09:35 EEST (escalated A-tier);
  similar B-tier with overhang since at least 2026-05-29.

### TODO-catalyst-symbol-mapping
- **issue:** 80 % of catalyst events today are unmapped (no `symbol`).
  This breaks the system-internal "symbol-aware catalyst" path and the
  legal-flag detection that depends on it.
- **evidence:** 1,204 events, 236 mapped, 968 unmapped (80.4 %).
  Persistent: 81.2 % unmapped yesterday, 79.2 % the day before.
- **suggested manual fix:**
  - Extend the entity-alias matcher (`src/catalysts/entity_aliases.py`)
    with stocks-specific aliases (currently it's crypto-focused).
  - For stocks, run the news title through the universe ticker list
    (`config/stocks/universe.yaml`) as a fallback when the alias matcher
    finds nothing — same pattern the RSS collector already uses.
  - Promote `other_news` events with high-importance keywords (e.g.
    "SEC", "indictment", "guidance withdrawal") to richer categories so
    they reach the scoring path.
- **priority:** medium
- **first observed:** persistent, > 7 days.

### TODO-cleanup-dry-run-signal_alerts
- **issue:** 5 `tg=dry_run` rows from yesterday's manual smoke run
  still in `signal_alerts`. Cosmetic.
- **evidence:** `SELECT * FROM signal_alerts WHERE telegram_status =
  'dry_run' AND date(sent_at) = '2026-06-02';`
- **suggested manual fix:** one-off SQL delete plus a `--dry-run`
  audit flag for the monitor to tag them as `qa_dry_run` instead of
  the same status used by genuine "notifier disabled" runs.
- **priority:** low
- **first observed:** 2026-06-02 23:34 EEST.

### TODO-opus-routine-cadence-resilience
- **issue:** When Claude Desktop is closed during a cron fire (08:30,
  12:30 today), the routine only catches up once on next launch — it
  does not back-fill skipped slots.
- **evidence:** Today's runs at 00:52 / 02:12 / 11:14 / 13:55 vs
  scheduled 00:30 / 04:30 / 08:30 / 12:30.
- **suggested manual fix:** operational only — keep Claude Desktop
  open during paper-trading hours. No code fix required.
- **priority:** low / operational

---

## 10. Verdict

- **Infra & process health:** GREEN.
- **Error surface:** CLEAN since PART 14.
- **Signal pipeline:** GREEN, **except SMCI A-tier legal regression**.
- **Trade tracking:** GREEN. Honest outcome accounting.
- **Telegram delivery:** GREEN. Real alerts firing during US RTH.
- **Obsidian dashboards:** GREEN, synced every cycle.
- **Opus auto-reviews:** GREEN content quality. Catch-up lag when
  Desktop is closed.
- **Profitability:** marginal-positive aggregate (crypto +2.50R,
  stocks +10.06R). The edge is concentrated in **stocks intraday
  B-tier (+14.90R)**.

**Single high-priority defect:** PART 3 legal-risk gate is not
catching SMCI today despite full news coverage. Logged as
`TODO-SMCI-legal-gate-regression` for a separate manual session with
elevated permissions.

No code changes were made in this audit per the PART 16 read-mostly
contract. The Windows scheduled tasks continue running undisturbed.
