# Auto Enriched-Review Routine Fix Report (PART 15)

**Date:** 2026-06-03
**Scope:** Update the routine prompt + supporting docs for the
`opus-enriched-review-4h` Claude scheduled task. Advisory only — **no
trading, no scoring, no agent, no scheduler, no strategy changes.**

---

## 1. Files Changed

| # | Path | Change |
|---|------|--------|
| 1 | `C:\Users\adama\.claude\scheduled-tasks\opus-enriched-review-4h\SKILL.md` | **Full rewrite via `mcp__scheduled-tasks__update_scheduled_task`.** New 13-section structure, strict priority order, legal/headline/price-reaction/prev-review/catalyst-coverage logic, graceful web-unavailable fallback, correct output contract. |
| 2 | `.claude/skills/enriched-review/SKILL.md` (project-scoped skill used by manual `/enriched-review`) | Phase 2 candidate selection rewritten to PART 15 priority order; Phase 3 internal-first external-research rule; new Phase 5 (chart + price-reaction), Phase 5a (catalyst coverage), Phase 5b (legal/headline), Phase 5c (prev-review diff); Phase 6 structure replaced with the new 13-section layout. |
| 3 | `prompts/llm_review/enriched_market_review_protocol.md` | §3 candidate selection rewritten with the new priority order (asset-agnostic A-tier ranking). |
| 4 | `obsidian_vault/15_LLM_Context/Opus_Enriched_Market_Review_System_Prompt.md` | Header banner added: PART 15 changes summarized. |
| 5 | `AUTO_ENRICHED_REVIEW_ROUTINE_FIX_REPORT.md` (this file) | New. |

No edits under `src/` — confirmed via diff. No scheduler restart, no agent
changes, no scoring changes.

---

## 2. What Was Fixed

### 2.1 Output contract contradiction (PART 2)

**Before:** Prompt said "ONE markdown file + ONE Telegram message" but
the routine also wrote a timestamped history copy and a sources JSON
and (optionally) called ingestion.

**After:** Allowed outputs explicitly enumerated:

1. `OPUS_ENRICHED_REVIEW_LATEST.md`
2. `OPUS_ENRICHED_REVIEW_AUTO_<YYYY-MM-DD_HHMM>.md`
3. `data/raw/enriched_review_sources/<ISO>.json`
4. Optional idempotent ingestion via `scripts.ingest_enriched_review_sources`
5. ONE compact Telegram summary

Forbidden actions enumerated in the same place (no `src/` edits, no
scheduler restart, no auto-trade, no paid APIs, READ-ONLY of
`news_trader`).

### 2.2 Web-research access + fallback (PART 0 / PART 5)

`WebSearch` + `WebFetch` are loaded via `ToolSearch:` at the top. If
either fails to load, the routine sets "External web research
unavailable" up front and falls back to internal `news_items` /
`catalyst_events` / `narrative_baskets` ONLY — no fabrication. A
specific candidate whose verdict depends critically on external
verification is demoted to "manual review required" rather than
blocking the whole review.

### 2.3 Smarter stale-scheduler check (PART 3)

**Before:** Single condition — `scheduler.log` mtime > 3h → defer.

**After:** Two-signal AND condition — defer only when BOTH
`scheduler.log` mtime > 3h AND the latest `cycle_*_summary.md` mtime > 3h.
Cuts false-positive defers (e.g. scheduler still ticking while a heavy
report writes slowly).

When deferring: write `OPUS_ENRICHED_REVIEW_DEFERRED_<ISO>.md`, send the
one-line Telegram, exit. Do not continue.

### 2.4 Candidate selection (PART 4)

**Before:** Stocks A-tier listed first, crypto A-tier listed after.

**After:** Asset-class is **not** a tiebreaker until tier ties. Priority:

1. Any A-tier (crypto OR stocks).
2. A/B with contradiction risk (legal, catalyst-vs-technical, stale,
   integrity).
3. New B-tier triggered this cycle (~2.5h).
4. Active B-tier waiting_for_entry within 1 ATR.
5. Catalyst-backed C-tier score ≥ 78 or fresh basket primary.
6. Symbol with fresh Telegram-channel news in last 4h.
7. System-integrity anomalies (untracked alerts, NULL-symbol catalyst,
   etc.).

Max 5 deep dives. Excess qualifying candidates listed in §7 with reason.

### 2.5 External research is internal-first (PART 5)

**Before:** Required ≥1 WebSearch + ≥1 WebFetch per candidate, every run
— burned tokens and time for candidates the system already had fresh
internal data on.

**After:** Per candidate, check `news_items` (last 24h) + `catalyst_events`
first. Reuse them if fresh and consistent. Run WebSearch + WebFetch
**only** when internal records are missing, stale, or contradict the
system's signal. Every external claim still requires source + title + date +
URL + verification_status + (confirms / weakens / contradicts) label.

### 2.6 Catalyst coverage diagnostics (PART 6)

New Phase 5a / Step 5. Compute per run:
- total `catalyst_events`,
- mapped count (non-null symbol),
- unmapped count,
- `narrative_baskets` count,
- if unmapped > 50 % → emit "catalyst mapping weak this run — use catalyst
  layer as context, not final decision." in §5 AND in the Telegram
  summary. List top 3 unmapped headlines by importance.

### 2.7 Legal / headline check on every stocks A/B (PART 7)

New Phase 5b / Step 7. For every stocks A or B candidate (and crypto
symbols carrying prior legal flags like SMCI), search/check for
indictment, SEC, DOJ, class action, fraud, auditor resignation,
accounting restatement, regulatory risk, delisting risk, guidance
withdrawal. If found and verified: add a `LEGAL/HEADLINE RISK` line,
demote verdict to AVOID or MANUAL REVIEW REQUIRED, cite source + date.

The canonical regression is the SMCI March-2026 SDNY indictment that
slipped past A-tier scoring. PART 7 catches that class of case.

### 2.8 Price-reaction / chase check (PART 8)

New Phase 5 question set, mandatory per candidate:

- Has price already reacted to the catalyst?
- Is the setup chasing?
- Is there a retest / pullback structure?
- Is the move overextended (> 2 ATR from EMA20)?
- Would entry NOW be late?
- What level makes it actionable?

If chart MCP not loaded: state "TradingView / manual chart check
unavailable" and rely on local OHLCV / ATR / EMA fields from the report
only. No fabricated chart observations.

### 2.9 Diff vs previous auto-review (PART 9)

New Phase 5c / Step 8. Find the most recent `OPUS_ENRICHED_REVIEW_AUTO_*.md`
other than the one being written. §4 of the review summarises: new /
removed / upgraded-downgraded candidates, new catalysts, thesis
changed-or-not, confirmed, invalidated. If no prior review exists: write
"previous review unavailable." and continue.

### 2.10 Output structure (PART 10)

The review markdown is now organised as 13 sections in the exact order
specified in the user's PART 10. Includes a dedicated "Scheduler / Data
Freshness Check" (§3), "What Changed vs Previous Review" (§4), "Catalyst
Coverage" (§5), per-mode final verdict (§12).

### 2.11 Telegram summary (PART 11)

Strict format under 3500 chars. Includes verdict per mode, top decisions,
avoid list, top risk, catalyst-coverage line (with weak-mapping warning if
applicable), file name, "Advisory only. No auto-trade." footer. If no
clean candidates → "No clean candidates — watchlist / no-trade."

### 2.12 Ingest sources (PART 12)

Persist to `data/raw/enriched_review_sources/<ISO>.json`, then run
`scripts.ingest_enriched_review_sources` once per asset class cited
(crypto / stocks). On ingest failure: log in §10 risks, continue review,
do not crash.

---

## 3. Dry Validation (PART 14)

Run on the **live** project state at 2026-06-03 01:18 EEST. All routine
prerequisites resolve without errors:

| Step | Result |
|------|--------|
| Latest scheduler folder | `2026-06-02_default_schedule` (scheduler.log 0.4h old, latest cycle 12.7h old → routine would NOT defer because `scheduler.log` is fresh) |
| Crypto scalp report | `2026-06-02_22-22_scalp_report.md` (0.7h) — fresh |
| Crypto intraday report | `2026-06-02_22-32_intraday_report.md` (0.5h) — fresh |
| Crypto swing report | `2026-06-02_14-55_swing_report.md` (8.1h) — carry-forward |
| Stocks intraday report | `2026-06-02_22-36_stocks_intraday_report.md` (0.4h) — fresh |
| Stocks swing report | `2026-06-02_15-03_stocks_swing_report.md` (8.0h) — carry-forward |
| Stocks invest report | `2026-06-02_15-08_stocks_invest_report.md` (7.9h) — carry-forward |
| Catalyst directory | `data/catalysts/2026-06-02/` present. 3,315 events. **mapped 688 / unmapped 2,627 (79 %) → routine WILL emit "catalyst mapping weak this run" warning**. 4 baskets. |
| Previous auto-reviews | 3 found. Latest: `OPUS_ENRICHED_REVIEW_AUTO_2026-06-03_0052.md` → diff section will work. |
| Ingest script | `scripts/ingest_enriched_review_sources.py` present and callable. |

Telegram notifier — already configured for the project; no new
credentials required.

---

## 4. Task Confirmation

```
taskId:        opus-enriched-review-4h
enabled:       true
cron:          30 0,4,8,12,16,20 * * *      (6×/day; 4-hour cadence)
description:   "Auto enriched-review every 4h … PART 15 upgrade — …"
nextRunAt:     2026-06-03 01:38 UTC = 04:38 EEST
lastRunAt:     2026-06-02 21:38 UTC = 00:38 EEST  (older prompt — last run before this fix)
jitterSeconds: 530   (system-controlled, ~9 min jitter)
```

The next auto-review (04:38 EEST) will run with the PART 15 prompt.

---

## 5. Limitations Remaining

1. **Catalyst mapping is 79 % unmapped today.** The routine will surface
   this in every review until the catalyst-collector's symbol-resolver
   improves. This is a content limitation, not a routine bug.
2. **Chart access** (TradingView / Chrome MCP) is not in the routine's
   default tool set. Every review will declare "TradingView / manual
   chart check unavailable" and rely on local OHLCV. Acceptable per
   the user's earlier explicit choice.
3. **`opus-decision-us-open`** and `opus-decision-evening` remain
   disabled (superseded by the 6×/day routine since 2026-06-01).
4. **Claude Desktop must be open** for the cron-based scheduled task to
   fire. If the Desktop app is closed during the cron moment, the task
   runs on next launch (one-shot catch-up, no back-fill of skipped slots).

---

## 6. Verdict

`READY_FOR_NEXT_AUTO_REVIEW`
