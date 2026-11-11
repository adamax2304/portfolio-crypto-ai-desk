---
name: enriched-review
description: Use this skill when the user asks for an "enriched review", "opus review", "/enriched-review", or any request to produce an OPUS_ENRICHED_REVIEW_*.md. The skill enforces the §14 source-discipline contract from prompts/llm_review/enriched_market_review_protocol.md by loading WebSearch + WebFetch, running structured external research per candidate, persisting found news to news_items SQLite, and rendering a fully-cited markdown review. Do not use for the basic system reports (scalp-report / intraday-report) — those are deterministic CLI commands.
---

# Enriched Market Review — skill

## PART 16 (2026-06) — Two execution modes

This skill runs in TWO modes with different permission contracts:

1. **Manual mode** — invoked by the user typing `/enriched-review` or
   asking "do an enriched review". The user is online; the operator may
   request additional permissions during the run if needed. Code edits
   are still NOT a goal of the skill, but the operator can confirm
   tool prompts interactively.
2. **Scheduled mode** — invoked by the Claude Desktop cron task
   `opus-enriched-review-4h` every 4 hours. The user is NOT online.
   The run is **read-mostly and advisory-only**. The routine MUST NOT
   show the user permission prompts for forbidden actions. If a forbidden
   action is needed, write a `Fix Requests / TODO` entry instead.

**Hard rule (PART 16):**

> Scheduled review is read-mostly. It may create review artifacts only.
> It must never implement fixes. If permissions are required for a
> forbidden action, do not request them — skip the action and write a
> TODO.

The full permission contract lives in the routine task at
`~/.claude/scheduled-tasks/opus-enriched-review-4h/SKILL.md` (§A allowed,
§B forbidden, §C absolute permission rule, §Q TODO format).

For manual invocations, the operator should still respect the spirit:
the skill produces a review document, not a refactor.

This skill is the canonical workflow for producing `OPUS_ENRICHED_REVIEW_*.md`
files in this project. The full advisory protocol lives in
`prompts/llm_review/enriched_market_review_protocol.md`; this file is the
**operational checklist** that tells Claude *how* to actually execute it
when the user invokes the skill.

## When to invoke

Match any of:
- user says "enriched review", "opus review", "deep review", "market review with sources"
- user types `/enriched-review` (slash trigger)
- user explicitly asks to produce `OPUS_ENRICHED_REVIEW_*.md` or to "do a
  full review using external research"

Do **NOT** invoke for:
- `/run scalp-report` or `/run intraday-report` — those are deterministic
  pipeline runs, not reviews.
- "summarize today" — use `python -m src.cli review-day` instead.
- Quick questions / spot-checks — overkill.

## Required tools

Before doing ANY external research, load these deferred tools via
`ToolSearch`:

```
select:WebSearch,WebFetch
```

These are mandatory. If either fails to load and the run requires
external sources, **state "External web research unavailable" up front**
(per §14) and rely on internal data only — do not fabricate.

Optional / per scope:
- `mcp__Claude_in_Chrome__*` — if user wants TradingView chart
  verification. Requires Chrome extension; check `.mcp.json`.
- `Bash` — to invoke the ingestion script below.

## Workflow (in order)

### Phase 1 — Internal data (always first)

Read **before** any external lookup, per §2 of the protocol:

1. `python -m src.cli active-signals --asset-class crypto`
2. `python -m src.cli active-signals --asset-class stocks` (skip if
   crypto-only weekend run).
3. `python -m src.cli signal-stats --asset-class crypto`
4. `python -m src.cli signal-stats --asset-class stocks` (same caveat).
5. `python -m src.cli track-signals --all` (refresh outcomes first).
6. `python -m scripts.detect_untracked_legacy_alerts --since <today>` —
   surface any PART 1 regressions.
7. Latest reports:
   `data/reports/scalp/<latest>.md`,
   `data/reports/intraday/<latest>.md`.
8. Latest packets:
   `data/processed/llm_analysis_packet.md`,
   `data/processed/context_for_llm.md`.
9. Most-recent run folder under `data/scheduled_runs/` if a scheduler
   is active.
10. **🆕 Auto-collected catalyst data** (read BEFORE any WebSearch):
    - `data/catalysts/<YYYY-MM-DD>/catalyst_events.jsonl` (per-event records)
    - `data/catalysts/<YYYY-MM-DD>/narrative_baskets.jsonl` (clusters)
    - `data/catalysts/<YYYY-MM-DD>/catalyst_cycle_*.md` (per-cycle summary)
    If the scan has not run today (no files), trigger it:
    `python -m src.cli catalyst-scan --no-print`. The scan reads
    news_items already populated by RSSNewsCollector — it does NOT
    fetch new HTTP, so it is cheap and safe.
11. **Obsidian system prompt**:
    `obsidian_vault/15_LLM_Context/Opus_Enriched_Market_Review_System_Prompt.md`
    — refresh your behavior contract before producing the review.

Establish the **internal verdict per candidate** *before* touching the web.
External research is for confirm/weaken/contradict only.

### Phase 2 — Candidate selection (§3)

PART 15 update — strict priority order, **max 5** deep-dive candidates.
Asset-class is NOT a tiebreaker until tier ties (crypto A-tier ≥ stocks A-tier).

1. **Any A-tier signal — crypto or stocks** (asset-agnostic; crypto A-tier is
   rare → never skip in favour of a stocks A-tier).
2. **Any A/B signal carrying contradiction risk:** legal/headline risk,
   catalyst contradicts the technical signal, external news contradicts the
   score, stale data, untracked / system-integrity warning.
3. **New B-tier triggered in this cycle** (`created_at` within last ~2.5h).
4. **Active B-tier `waiting_for_entry` where price is within 1 ATR** of the
   entry zone — "price approaching" is the trader's primary alert pattern.
5. **Catalyst-backed C-tier** with score ≥ 78 OR a strong fresh narrative
   (basket primary symbol with `freshness < 6h`).
6. **Any symbol with fresh Telegram-channel news in the last 4h**
   (`news_items.source LIKE 't.me/%'`).
7. **System-integrity anomalies worth surfacing:** non-zero untracked-alert
   count, stale source, high-importance catalyst with `symbol IS NULL`,
   watchlist Telegram alert without backing `proposed_signal`, legal-risk on
   a stocks A/B.

If more than 5 candidates qualify, state in §7 of the review which qualifying
candidates were NOT deep-dived and why.

If there are zero qualifying candidates, that's fine — say so explicitly and
output "No clean candidates — watchlist / no-trade." in the Best Candidates
section.

### Phase 3 — External research per candidate (§4 + §14)

PART 15 update — internal-first, external only when needed.

Per candidate, BEFORE WebSearch:
- Check `news_items` for fresh rows where `detected_symbols` includes the
  candidate's base ticker AND `datetime(published_at) > datetime('now','-24 hours')`.
- Check `catalyst_events.jsonl` for an entry matching this candidate.

If internal records are present, recent, and CONSISTENT with the system's
signal — **reuse them**, no new WebSearch needed.

If internal records are missing, stale (>24h), inconsistent with the signal,
or contradicted by other internal sources — run external research:

**≥ 1 WebSearch query**. Query templates:

| Goal | Query template |
|------|----------------|
| Symbol catalyst | `{SYMBOL} crypto news catalyst {YYYY-MM-DD}` |
| Symbol fundamentals (token) | `{TOKEN_NAME} token unlock partnership {month YYYY}` |
| Symbol exchange events | `{SYMBOL} Binance listing delisting {YYYY-MM-DD}` |
| BTC / ETH macro | `Bitcoin Ethereum market analysis {YYYY-MM-DD}` |
| Sector / narrative | `{NARRATIVE} crypto sector news this week` |
| Exploit / hack | `{PROTOCOL} exploit drained {YYYY-MM-DD}` |

For **stocks** (when applicable, e.g. SMCI-style legal-risk check):
| Goal | Query template |
|------|----------------|
| Legal / regulatory | `{TICKER} SEC indictment lawsuit {YYYY}` |
| Earnings | `{TICKER} Q{n} earnings report {YYYY-MM-DD}` |
| Analyst | `{TICKER} analyst price target upgrade downgrade {month}` |

For each result you cite:
1. **Verify the URL opens** via WebFetch (don't trust the search-snippet
   alone — read the article).
2. Extract: `title`, `source`, `published_at` (date — if not visible on
   the page, write "date unavailable"), `url`.
3. Classify `verification_status`:
   - `primary_source` — official announcement (SEC filing, Binance
     announcement, company IR, exchange listing page).
   - `single_source` — reputable outlet (CNBC, Bloomberg, CoinDesk,
     Cointelegraph, Decrypt, Reuters).
   - `social_only` — Twitter / Telegram / Reddit — flag explicitly,
     treat as weak.
   - `unverifiable` — link 404s, paywall blocks WebFetch, date missing.
     **Do not use it as fact.**

### Phase 4 — Ingest sources into `news_items` SQLite

After collecting URLs, batch-ingest into the SQLite `news_items` table
so future cycles can see what you found:

```
python -m scripts.ingest_enriched_review_sources \
    --json data/raw/enriched_review_sources/<YYYY-MM-DD_HHMM>.json
```

The script (see `scripts/ingest_enriched_review_sources.py`) uses
`SQLiteStore.save_news_items` with `ON CONFLICT(url)` so it is idempotent.
Required JSON shape:

```json
[
  {
    "title": "...",
    "source": "CoinDesk",
    "url": "https://...",
    "published_at": "2026-05-30T14:00:00Z",
    "detected_symbols": ["BTC/USDT"],
    "detected_narratives": ["macro"],
    "importance": 0.7,
    "verification_status": "single_source"
  }
]
```

If you have only 1–2 sources, you may inline-call
`SQLiteStore.save_news_items` from a tiny Python one-liner via Bash
instead of dumping JSON.

### Phase 5 — Chart verification + price-reaction / chase check (§5 + PART 15)

If `mcp__Claude_in_Chrome__*` is loaded and configured:
- Navigate to TradingView for each actionable candidate; take a
  screenshot via `mcp__Claude_in_Chrome__gif_creator` or page-text via
  `mcp__Claude_in_Chrome__get_page_text` to verify trend / structure /
  retest / volume.

Otherwise:
- **Write "TradingView / manual chart check unavailable"** in the review.
- Use local OHLCV / ATR / EMA fields from the report only.
- **Never fabricate a chart observation.**

PART 15 — for EVERY candidate, also answer explicitly in its deep dive:

- Has price already reacted to the catalyst?
- Is the setup chasing the move?
- Is there a retest / pullback structure forming?
- Is the move overextended (e.g., > 2 ATR from EMA20)?
- Would entry NOW be late?
- What price level would make this actionable?

### Phase 5a — Catalyst coverage check (PART 15 / §6)

Compute and report:

- Total `catalyst_events.jsonl` rows for today.
- Events with a non-empty `symbol`.
- Events with empty / null `symbol` (unmapped).
- `narrative_baskets.jsonl` row count.
- If `unmapped > 50 %` of total: emit the line
  **"catalyst mapping weak this run — use catalyst layer as context, not final decision."**
  in §5 of the review and in the Telegram summary.
- Also list top 3 unmapped catalyst headlines by importance.

### Phase 5b — Legal / headline risk check (PART 15 / §7)

For EVERY stocks A or B candidate (and crypto symbols with prior legal
flags like SMCI), search/check for:

- indictment, SEC investigation, DOJ investigation, class action,
  securities fraud
- auditor resignation, accounting irregularities, restatement, going concern
- regulatory risk (FDA halt, export-control ban, sanctions)
- delisting risk, guidance withdrawal, suspicious rally after bad earnings

If verified per §G source discipline:
- Add a `LEGAL/HEADLINE RISK` line to the candidate's deep dive.
- Final verdict becomes `AVOID` or `MANUAL REVIEW REQUIRED` — never a clean
  actionable.
- Cite source + date.

Canonical regression case: SMCI's March-2026 SDNY indictment was not
caught initially while the system still produced A-tier scores.

### Phase 5c — Compare with previous review (PART 15 / §9)

Find the most recent `OPUS_ENRICHED_REVIEW_AUTO_*.md` other than the
one you're about to write. In §4 of the review summarise:

- **New** candidates since prior review.
- **Removed** candidates (and why).
- **Upgraded / downgraded** (tier change, score change ≥ 5).
- **New catalysts** since prior review.
- **Thesis changed or unchanged** per surviving candidate.
- **What was confirmed** by this run's data.
- **What was invalidated** (price moved past invalidation, catalyst
  proven wrong, etc.).

If no prior auto-review exists, write **"previous review unavailable."** in
§4 and continue.

### Phase 6 — Render `OPUS_ENRICHED_REVIEW_*.md`

**Agent Council Review Mode (2026-06):** produce the review as a SINGLE LLM run
that reasons like a trading-desk council — nine virtual agents
(`data_quality, market_regime, catalyst_narrative, derivatives_squeeze,
technical_entry, execution_lifecycle, risk_manager, playbook_performance,
head_trader`), each emitting verdict / confidence / reason_codes / data_missing
/ suggested_effect=`advisory_only` / facts_used, then a Head Trader synthesis.
**No extra agents/processes/LLM calls** — internal reasoning only, advisory,
no scoring/TP-SL/entry/routing/execution change. Embed the mandatory machine-
readable Agent Council JSON block and an Agent Council table. The full spec
(agent responsibilities, reason-code sets, JSON shape, status-language rules)
is in `~/.claude/scheduled-tasks/opus-enriched-review-4h/SKILL.md` →
"AGENT COUNCIL REVIEW MODE" and protocol §17.

**Status/lifecycle language (mandatory):** never bare `expired` / bare `+0R` /
"no active trades"; use OPEN-actionable / WAITING / REVIEW-SHADOW /
ENTERED-UNRESOLVED / NO-ENTRY·STALE·MOVED-AWAY / CLOSED WIN·LOSS·FLAT /
NEEDS-REVIEW. Split expired into entered-unresolved (not a miss) vs no-entry.

Structure (Agent Council JSON + Table inserted after freshness; existing
sections kept):

```
# Opus Enriched Review — <SLOT TYPE / context>

## 1. Executive Summary               (≤10 lines; state slot type + "advisory only / no auto-trade")
## 2. Data Used
## 3. Scheduler / Data Freshness       (+ monitor / paper status if available)
## 3A. Agent Council JSON              (the mandatory ```json block)
## 3B. Agent Council Table             (Agent | Verdict | Confidence | Reason codes | Suggested effect)
## 4. What Changed vs Previous Review  (per Phase 5c; OR "previous review unavailable.")
## 5. Catalyst Coverage                (mapped/unmapped counts, baskets, top 3 unmapped if weak)
## 6. Market Landscape                 (Market Mood / Risk Routing — DRIVEN BY the council)
   - Crypto (BTC/ETH regime, breadth, vol, long/short bias)
   - Stocks (weekday + fresh only — SPY/QQQ/IWM/DIA, VIX, sector context)
## 7. Candidate Deep Dives             (≤ 5; long/short/wait, actionable-now vs wait-for-trigger,
                                       catalyst support/contradiction, chase risk, entry freshness,
                                       lifecycle status, legal/headline risk for stock A/B, verdict)
## 8. Best Candidates Ranked           (always name best long-watch / short-watch / catalyst-watch +
                                       avoid with exact triggers; never a bare "No clean candidates.")
## 9. Avoid / No Trade                 (this decision window only — never "stop system")
## 10. Main Risks
## 11. Action Plan — next 4 hours
## 12. Final Verdict per Mode
## 13. Sources                         (markdown hyperlinks + publication dates)
## 14. Fix Requests / TODO             (TODO-only; no fixes from scheduled runs)
```

Filename convention:
- Auto-routine: `OPUS_ENRICHED_REVIEW_LATEST.md` (overwrite) +
  `OPUS_ENRICHED_REVIEW_AUTO_<YYYY-MM-DD_HHMM>.md` (history).
- Manual / contextual: `OPUS_ENRICHED_REVIEW_<context>.md` (e.g.
  `OPUS_ENRICHED_REVIEW_24H_CRYPTO_ONLY.md`).

### Phase 7 — §14 final checklist (block on any failure)

Before saying "done", verify:

- [ ] Every external claim has a named source, title, date, URL.
- [ ] No uncited stats (revenue / EPS / price target / %-move).
- [ ] No uncited legal claims (SEC / DOJ / indictment / auditor / class action).
- [ ] No fabricated TradingView observations — if charts unavailable, said so.
- [ ] Missing source → wrote "source unavailable" instead of guessing.
- [ ] `test_source` / fixture news was filtered out (the news_items
      pipeline already does this; double-check no test-tagged URL slipped in).
- [ ] **Sources** section at the bottom with markdown hyperlinks.
- [ ] If web entirely unavailable: declared "External web research
      unavailable" up front and did not upgrade confidence on imagined
      context.

If any item fails, **fix before delivering**. The audit value of the
review depends on every external claim being verifiable against a
dated, named source.

## Safety constraints (inherit from project)

- Do NOT auto-trade (no execution layer exists).
- Do NOT change scoring / thresholds / agent / strategy code.
- Do NOT refactor.
- Do NOT add paid APIs.
- The news_trader bridge is READ-ONLY — never write to
  `C:\Users\adama\Documents\zeph ai projects\news_trader\`.

### PART 16 — Fix Requests / TODO escape valve (mandatory §14 of every review)

When a review (manual or scheduled) observes a bug, regression, scoring
anomaly, missing feature, broken pipeline step, integrity issue, or
improvement opportunity, the review document MUST include a §14
"Fix Requests / TODO" section. Each entry uses this format:

```
### TODO-<short-tag>
- **issue:**            <one-line description>
- **evidence:**         <file path / log line / SQL query result>
- **suggested manual fix:** <what a human-driven session should do>
- **priority:**         high | medium | low
- **first observed:**   <YYYY-MM-DD HH:MM EEST>
```

Scheduled runs MUST NOT attempt to act on these TODOs; manual runs MAY
flag them for the operator but still produce the review document, not
the fix. A separate manual Claude / Codex session with explicit
permissions will work the TODOs later.

If there are no issues to surface, the section reads `_None._`. The
section must always exist so the diff-vs-prior-review can track it.

## Output

Single markdown file at project root: `OPUS_ENRICHED_REVIEW_<context>.md`
with the sections above. Telegram is NOT sent from this skill — it
produces a doc; user sends manually if they want.
