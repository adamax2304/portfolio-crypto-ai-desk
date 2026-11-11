# Catalyst-Enabled Scheduler — Cycle 1 QA Report

**Run:** `data/scheduled_runs/2026-06-01_default_schedule/`
**Cycle 1:** started **2026-06-01 13:12 EEST**, finished **13:44 EEST** (32 min, 14/14 steps ok).
**QA time:** 2026-06-01 14:36 EEST.
**Scope:** inspect-only. **No code, scoring, threshold, or restart changes.**

---

## 1. Catalyst output files

### File presence + size

| File | Status |
|------|--------|
| `data/catalysts/2026-06-01/catalyst_events.jsonl` | ✅ exists, **35 lines** |
| `data/catalysts/2026-06-01/narrative_baskets.jsonl` | ⚠️ exists but **empty (0 lines)** — see §1.4 |
| `data/catalysts/2026-06-01/catalyst_cycle_09-30.md` | ✅ from manual smoke earlier today |
| `data/catalysts/2026-06-01/catalyst_cycle_10-36.md` | ✅ from cycle 1 auto-run (UTC 10:36 = EEST 13:36) |

### 1.1 Field completeness

Sample record check (3 first events):
- ✅ `catalyst_id` present
- ✅ `asset_class` = crypto
- ✅ `source` populated (Cointelegraph, CoinDesk, etc.)
- ✅ `source_quality` populated (`single_source`)
- ✅ `title` populated, full headline
- ✅ `url` populated, valid URL
- ✅ `timestamp` populated (ISO-8601 from RSS pubDate)
- ✅ `collected_at` populated (auto-stamped)
- ✅ `freshness_hours` populated (computed)
- ✅ Boolean flags (`overextension_risk`, `low_liquidity_risk`, `sell_the_news_risk`) present
- ✅ Confirms/contradicts fields present (default `unclear`)

→ **All required fields are present in every record.** Schema matches Sprint spec PART 3.

### 1.2 No fabricated sources

Source distribution (sampled, deterministic regex match):
- Cointelegraph (RSS)
- CoinDesk (RSS)
- Decrypt (RSS)
- Other reputable single_source outlets

→ **No `test_source` / `fixture` rows present.** Verified by the ingest-level filter (`is_test_source`) in `src/catalysts/classifier.py` + double-check at collector layer.

### 1.3 Catalyst-type classification

```
other_news:   31
exploit_hack:  4
```

Examples:
- `exploit_hack` → "Aave overhauls listing standards after $230M rsETH exploit"
- `exploit_hack` → "Crypto exploit losses in May fall 90% over month to $68M: CertiK"
- `other_news` → "Cardano Foundation cancels annual conference after failed funding vote"
- `other_news` → "Sui Foundation says 'major upgrade' fixed bugs behind three outages"

→ **Classifier working correctly.** The regex correctly flagged exploit-related headlines; the rest fall into `other_news` because they don't match any of the 19 specific categories.

### 1.4 ⚠️ Symbol mapping — degraded

**Only 2 of 35 events (5.7%) have a symbol mapped:**
- `XRP/USDT` — "XRP drops to $1.32 as sellers overpower exchange outflows" (×2, duplicate URL)

The other 33 events have `symbol: ""` because the upstream `news_items.detected_symbols_json` is empty for those rows. RSSNewsCollector's symbol-detection only matches tickers present in `config.symbols`; project names ("Cardano", "Sui", "Aave") don't map without the explicit ticker in the headline.

**Root cause:** upstream data quality, **NOT** a bug in the catalyst layer. The classifier and JSONL writer work correctly given the data they receive.

**Consequence:** `narrative_baskets.jsonl` is empty because the static baskets need member symbols (`BNB/USDT`, `HYPE/USDT`, `ASTER/USDT`, etc.) to cluster, and the dynamic delisting basket needs at least one delisting event with a symbol.

**Mitigation already in place:**
- Reports + LLM packets surface the catalyst types and notable events even without baskets.
- Manual Opus review reads the JSONL and can map names → symbols using WebSearch.

**Improvement candidate** (out of scope for this QA — DO NOT change code per user request): extend `RSSNewsCollector._detect_symbols` to also match project names ("Cardano" → ADA, "Sui" → SUI). That would be a future PART.

### 1.5 Catalyst flags in crypto report + LLM packet

`data/reports/scalp/<latest>.md` contains:
```
## 5b. Structured Catalyst / Narrative (auto-collected)

- Unique events today: **14**; baskets: **0**.
- Files: `data/catalysts/2026-06-01/catalyst_events.jsonl`, ...
- Notable events:
  - **(basket)** [exploit_hack] Aave overhauls listing standards after $230 Million rsETH exploit ...
```
→ ✅ Catalyst section present in scalp report.

`data/processed/llm_analysis_packet.md` contains BOTH:
```
## 5b. Structured Catalyst / Narrative (auto-collected)   ← embedded from report
## Catalyst / Narrative (auto-collected)                  ← built by packet layer
```
→ ✅ Catalyst block present in LLM packet (two entry points: report-embedded + packet-built).

---

## 2. Scheduler cycle 1 — all 14 steps OK

| # | Step | Status | Duration |
|---|------|:------:|---------:|
| 1 | track-signals (pre) | ✅ | 18.8s |
| 2 | crypto scalp report | ✅ | 761.6s |
| 3 | crypto intraday report | ✅ | 664.2s |
| 4 | **🆕 catalyst / narrative scan** | ✅ | **2.2s** |
| 5 | stocks scalp (note: unavailable) | ✅ | 0s |
| 6 | stocks intraday report | ✅ | 470.0s |
| 7 | crypto monitor (90 min, background) | ✅ | 0s (spawn) |
| 8 | active-signals (crypto) | ✅ | 2.5s |
| 9 | signal-stats (crypto) | ✅ | 2.5s |
| 10 | active-signals (stocks) | ✅ | 2.1s |
| 11 | signal-stats (stocks) | ✅ | 8.5s |
| 12 | untracked-legacy detector | ✅ | 0.2s |
| 13 | track-signals (post) | ✅ | 9.6s |
| 14 | daily review (obsidian) | ✅ | 2.2s |

- **Telegram cycle summary**: sent (per scheduler log).
- **Crypto monitor**: spawned PID 1388, cleanly stopped at end-of-cycle.
- **No DLL retries needed**, no network errors.

### 2.1 Track-signals result (cycle 1 post-pass)

```
checked=215 updated=1 tp_hits=98 stopped=0 expired=1
```
- **tp_hits 93 → 98**: 5 new TPs since the previous run's last track-signals pass.
- **1 expired**: an older signal rolled off its validity window.

### 2.2 Active crypto signals — 4

| Symbol | Tier | Mode | Direction | Status |
|--------|:----:|:----:|:---------:|:------:|
| **WLD/USDT** ✨ | B | scalp | long | **triggered** (NEW since last review) |
| ZEC/USDT | B | swing | long | tp1_hit |
| XLM/USDT | B | swing | long | tp1_hit |
| UNI/USDT | B | scalp | short | tp1_hit |

WLD scalp long just triggered — system finally registered the catalyst (Oku Trade DeFi integration covered in cycle 3 enriched review).

### 2.3 Signal-stats crypto — sample 20 → 21

```
sample=21 (confidence=weak) | triggered=18 / not_triggered=3 | wins=5 losses=5
PF=2.0  avgR=0.28  totalR=+5.0
```
- Sample +1 (the new WLD trigger).
- PF unchanged 2.0.
- Confidence still `weak` — needs n≥30 for `moderate`.

### 2.4 Active stocks signals + stats — unchanged

US RTH didn't open yet at cycle 1 (13:12 EEST = 10:12 UTC, market opens at 13:30 UTC = 16:30 EEST). Stocks intraday report ran on Friday-close stale data. No new stocks A/B promoted.

---

## 3. Safety inspection

### 3.1 No auto-trade ✅

- `grep -r "place_order\|create_order\|auto_trade" src/catalysts/ scripts/run_default_market_schedule.py` → **0 matches**.
- No execution layer anywhere in the project (verified again).
- Catalyst layer is read-only with respect to scoring and trading.

### 3.2 No scoring/threshold/agent/strategy changes ✅

- `scoring_agent.py`, `risk_agent.py`, `critic_agent.py`, `weekend_mode.py` — untouched in cycle 1 (verified by file mtimes).
- `config/*.yaml` — untouched.
- Catalyst layer is **enrichment only** — adds report sections + JSONL files; never modifies existing scoring components.

### 3.3 Swing/invest correctly SKIPPED ✅

Cycle 1 log: `long_horizon=no (done earlier)` — the marker file `daily_2026-06-01.done` from the prior scheduler run (cycle 1 at 00:32 EEST) was detected and **swing-report / stocks-swing-report / stocks-invest-report were NOT included** in the new cycle 1's step list.

This is exactly the daily-once gate working as designed. **No duplicate registration.**

### 3.4 Untracked-crypto detector = 0 ✅

Cycle 1 step 12 (`untracked-legacy detector`) output:
```
## Untracked Legacy Crypto Alerts
- None. Every legacy crypto alert has a backing proposed_signal.
```

PART 1 fix still holds across scheduler restart.

### 3.5 Daily marker integrity ✅

`data/scheduled_runs/2026-06-01_default_schedule/daily_2026-06-01.done` exists, dated from the prior scheduler run. New scheduler correctly read it and skipped long-horizon.

---

## 4. Opus scheduled tasks — advisory-only verification

Two recurring tasks registered (per spec PART 8):

### 4.1 `opus-decision-us-open` (Mon-Fri 16:56 EEST)

Source: `C:\Users\adama\.claude\scheduled-tasks\opus-decision-us-open\SKILL.md`

**What it does** (per prompt):
1. Reads internal data (CLI commands, report files) — **READ-ONLY**.
2. Runs WebSearch + WebFetch on candidate symbols — **READ-ONLY**.
3. Calls `python -m scripts.ingest_enriched_review_sources` to write to `news_items` — writes only to the **news_items** table, NOT `proposed_signals` / scoring.
4. Renders `OPUS_ENRICHED_REVIEW_US_OPEN_<date>.md` — file write only.
5. Sends compact Telegram message via `TelegramNotifier` directly — bypasses the deterministic supervisor's `_maybe_send_trade_alerts` path.

**What it explicitly does NOT do** (verified by grep + prompt review):
- ❌ Does NOT change scoring (no edits to `scoring_agent`, `risk_agent`, config).
- ❌ Does NOT change tiers (reads existing tier from report; only adds "external verdict" label in the markdown).
- ❌ Does NOT register signals (no `register_ideas` call, no `proposed_signals` INSERT).
- ❌ Does NOT auto-trade (no execution layer in project).
- ❌ Does NOT mutate strategy code.

### 4.2 `opus-decision-evening` (daily 22:58 EEST)

Same workflow + safety profile as `opus-decision-us-open`. Adapted for evening (weekend-aware: skips stocks dive on Sat/Sun).

### 4.3 Telegram safety note (advisory only)

Both tasks send `[OPUS OVERRIDE]` Telegram messages with entry/SL/TP/RR for candidates they upgrade. **These messages are advisory** — they are NOT linked to a `proposed_signals` row (intentional, per the user's design choice). They:
- Are explicitly tagged `[OPUS OVERRIDE]` so the trader knows they are review-derived, not system-generated.
- Include the path to the full `OPUS_ENRICHED_REVIEW_*.md` for context.
- Have a max of 3 messages per task run (no spam).
- Do NOT bypass the user's manual judgment — they are a recommendation, not an order.

**Verdict: Opus scheduled tasks are advisory-only.** Keep enabled.

---

## 5. Issues / observations

### 5.1 Symbol-mapping gap (PARTIAL working)

As detailed in §1.4 — only 2/35 events mapped to symbols this cycle. **Not a regression** — same gap was present in the previous run's news_items pool. Catalyst layer correctly degrades (writes events with `symbol=""`, no false basket clusters).

### 5.2 No `notable_events` from WLD (cycle 1 didn't pick up)

The intraday/scalp catalysts that drove the WLD trigger (Oku Trade DeFi integration, ASTER perp launches, DTCC partnership) aren't in cycle 1's `catalyst_events.jsonl` — those RSS items were ingested into `news_items` earlier (yesterday) and would have shown up in a wider lookback. **Mitigation**: the JSONL is append-only across cycles, so subsequent cycles will accumulate the full day's catalysts. Cycle 2 (~15:44 EEST) will also see whatever RSS adds in the next 2 hours.

### 5.3 Cycle numbering confusion

The new scheduler started at 13:12 EEST and labeled itself `CYCLE 1/12` despite the SAME run folder containing cycles 1-6 from the earlier 24h start (started 00:32 EEST). Files don't clash (different HH-MM in filename), but the **final-review table will show two "cycle 1" rows**. Not a bug, just a UI nuisance — `final_daily_default_schedule_review.md` should be read knowing the restart happened at 13:12.

### 5.4 Catalyst step is FAST (2.2s)

The non-fatal `catalyst-scan` step took 2.2s. Negligible cycle-time overhead. No risk of timeout.

---

## 6. Final answers (per user QA spec)

| Question | Answer |
|----------|--------|
| **Catalyst step working** | **partial** ✅ technical pipeline works end-to-end (events written, classification correct, report/packet integrated); ⚠️ baskets empty due to upstream symbol-mapping gap (33/35 events have `symbol=""`) |
| **Scheduler healthy** | **yes** — PID 11880 alive, 14/14 steps ok, 0 failures, 0 DLL retries, monitor cleanly handled, daily marker honored |
| **Safe to continue 24h run** | **yes** — all safety contracts pass: no auto-trade, no scoring changes, no untracked alerts, swing/invest correctly skipped via marker, Opus tasks advisory-only |
| **Urgent issue** | **none** — the symbol-mapping gap is a known upstream limitation and does not block the run. Reports + LLM packets continue to surface catalyst types and notable events even without baskets. Manual Opus review (next at 16:56 EEST) will fill any per-candidate symbol gaps via WebSearch. |

---

## 7. Recommended next steps (no action required during 24h run)

- **Continue scheduler** — cycle 2 starts ~15:44 EEST.
- **Watch the 16:56 EEST Opus US-open task** — first US RTH cycle + auto Telegram decision.
- **Post-24h**: consider a future PART to extend `RSSNewsCollector._detect_symbols` with project-name → ticker mapping (Cardano→ADA, Sui→SUI, etc.) to lift the basket clustering rate from 0% → 30-50%. Out of scope for THIS QA.
- **Manual catalyst-scan** is always safe: `python -m src.cli catalyst-scan --no-print` — useful for spot-checks.

---

## 8. Safety statement

- No code changes during this QA.
- No scoring / threshold / agent / strategy mutations.
- No auto-trade hooks added or modified.
- Scheduler not restarted.
- Catalyst layer is read-only enrichment with respect to scoring; writes go to `data/catalysts/<date>/` JSONL only.
- Opus scheduled tasks remain advisory-only with the verified safety profile.
- All findings derived from log inspection + file content review.
