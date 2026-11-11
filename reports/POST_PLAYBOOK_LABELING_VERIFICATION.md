# Post Playbook Labeling Verification

**Date:** 2026-06-09 · **Scope:** Verify the labeling layer is live across reports, dashboard, and LLM packets. No code-path changes since the report deploy.

## 1. Tests
| Suite | Result |
|---|---|
| `tests/test_playbook_labels.py` (new) | **16 passed** |
| `tests/test_stocks_swing_pause.py` | 9 passed |
| `tests/test_stocks_invest_pause.py` | 10 passed |
| `tests/test_crypto_scalp_low_confidence.py` | 6 passed |
| `tests/test_paper_execution_annotations.py` | 7 passed |
| `tests/test_pending_revalidation.py` | 6 passed |
| **Focused subset total** | **54 passed** |

No existing test broke.

## 2. CLI report runs
| Command | Exit | Playbook block visible? |
|---|---|---|
| `scalp-report --no-update` | 0 | ✅ every A/B + every C/watchlist idea has `#### Playbook` block |
| `intraday-report --no-update` | 0 | ✅ |
| `stocks-intraday-report` | 0 | ✅ A/B ideas carry block; C-tier rows carry `playbook=… status=…` suffix |
| `stocks-swing-report` | 0 | ✅ |
| `stocks-invest-report` | 0 | ✅ `A/B ideas=0 · C watchlist=5 · signals registered=0` — gate honored; C rows still carry playbook suffix |

LLM packets after each crypto run:
- `data/processed/llm_analysis_packet.md` carries the new `## Strategy Playbook Context` section at the top.
- `data/processed/llm_stocks_packet.md` carries the same block (shared `_build_playbook_context_block`).

## 3. Sample renders (verbatim)

### Crypto scalp report — idea card
```
### Trade Idea #1 - LONG ZEC/USDT

Score: 66.00/100
Confidence: medium
Trade Type: 5m / 15m
Risk: medium

#### Playbook
- Playbook: `crypto_scalp_momentum_continuation`
- Status: **low_confidence**
- Overlays: low_confidence_scalp
- Why this playbook: entry edge real (100% of expired scalps had positive MFE, avg +0.54R); TP1/2h horizon mismatch caps capture
- Known failure mode: TP1 distance ~1.86R vs typical captured MFE 0.54R — mean reverts before TP
- Manual review hint: Treat with lower confidence; consider taking partial off the table early.
```

### Stocks intraday report — idea card
```
### Idea #1 — B XOM long
#### Playbook
- Playbook: `stocks_intraday_rth_momentum`
- Status: **actionable**
- Overlays: rs_leader
- Why this playbook: stocks intraday B-tier 14d: WR 55%, PF 2.03, +80R; shorts subset PF 9.00
- Known failure mode: A-tier overpromotion on losing names — NVDA/SMCI/SMH longs structurally lose in this regime
- Manual review hint: Spot-check chart structure against thesis; avoid NVDA/SMCI longs without strong catalyst.
```

### Stocks invest report — watchlist row
```
- LLY (long): score 71.5, penalty 1.2 · playbook `stocks_invest_watchlist_30d_thesis` · status **watchlist_only**
```

### Obsidian dashboard — open trade row
```
- META · SHORT · intraday · tier B · score 68 · [TradingView](…)
  - Created: 2026-06-09 14:29 UTC | Expires: 2026-06-10 14:33 UTC
  - Paper entry: not triggered yet.
  - Entry zone: 594.47 – 598.40 | SL: 606.26 | TP1 582.68 / TP2 574.82 / TP3 563.03
  - Status: stale_before_entry | Current R: open | MFE: — | MAE: —
  - Playbook: `stocks_intraday_rth_momentum` · status **actionable** · overlays: short_playbook
  - Failure mode: A-tier overpromotion on losing names — NVDA/SMCI/SMH longs structurally lose in this regime
  - Manual review hint: Spot-check chart structure against thesis; avoid NVDA/SMCI longs without strong catalyst.
  - Source report: —
  - Comment: stale — pending past freshness horizon, manual review
```

### Obsidian dashboard — new "8b. Playbook Performance Snapshot" (excerpt)
```
| Playbook | n | closed | W | WR | PF | netR |
|---|---:|---:|---:|---:|---:|---:|
| `crypto_swing_narrative_rs_momentum` (long) | 13 | 13 | 10 | 77% | 5.00 | +21 |
| `crypto_intraday_catalyst_or_momentum` (catalyst=1) | 10 | 8 | 4 | 50% | 2.75 | +7 |
| `crypto_intraday_catalyst_or_momentum` (no catalyst) | 18 | 13 | 3 | 23% | 0.70 | −3 |
| `crypto_scalp_momentum_continuation` (low-confidence) | 56 | 8 | 1 | 12% | 0.14 | −6 |
| `crypto_failed_bounce_short` | 45 | 15 | 6 | 40% | 2.00 | +9 |
| `stocks_intraday_rth_momentum` (long) | 454 | 166 | 89 | 54% | 1.94 | +72 |
| `stocks_intraday_rth_momentum` (short) | 25 | 7 | 6 | 86% | 9.00 | +8 |
| `stocks_swing_watchlist_rs_rotation` (paused) | 54 | 44 | 5 | 11% | 0.15 | −33 |
| `stocks_invest_watchlist_30d_thesis` (paused) | 39 | 24 | 0 | 0% | 0.00 | −24 |
```

### LLM packet (Opus context) — `## Strategy Playbook Context`
The crypto packet (`llm_analysis_packet.md`) and stocks packet (`llm_stocks_packet.md`) now both carry the playbook→status→14d performance table + overlay primer + decision shortcuts at the top. Opus reads this before any specific idea, so its synthesis reasons by named playbook instead of only by tier/score.

## 4. Seven-point spec checklist
| # | Check | Result |
|---|---|---|
| 1 | Every A/B signal has a playbook label | ✅ rendered by `trade_idea_markdown` (crypto) and `_ideas_section` (stocks) |
| 2 | Every C/watchlist signal has a playbook label | ✅ crypto via `trade_idea_markdown` re-use; stocks via watchlist suffix |
| 3 | Crypto scalp shows `low_confidence` | ✅ both in the idea block and in the dashboard performance table |
| 4 | Stocks swing/invest show `watchlist_only` | ✅ both in the idea block and in the dashboard performance table |
| 5 | Opus packet includes playbook labels | ✅ `Strategy Playbook Context` section at top of both packets |
| 6 | No scoring/TP/SL/signal logic changed | ✅ no edits to `scoring_agent.py`, `technical_setup_agent.py`, `trade_idea_agent.py` (except prior gate adds, which were pre-existing in this work) |
| 7 | Tests / snapshot checks pass | ✅ 16/16 new + 54 in focused regression subset |

## 5. Files touched (recap)
- `src/signals/playbooks.py` (new)
- `tests/test_playbook_labels.py` (new)
- `src/reports/markdown_templates.py`
- `src/stocks/reports/stocks_report_builder.py`
- `src/analysis/packet.py`
- `src/stocks/llm_packet.py`
- `scripts/write_obsidian_current_state_dashboard.py`

## 6. Untouched (by design)
- `src/agents/scoring_agent.py`, `src/agents/technical_setup_agent.py`, `src/agents/trade_idea_agent.py`
- `src/stocks/agents/scoring_agent.py`, `src/stocks/agents/technical_setup_agent.py`, `src/stocks/agents/trade_idea_agent.py`
- All `config/*.yaml` weight/threshold tables.
- Telegram alert path.
- Historical `signal_outcomes` rows.

## Verdict
```
PLAYBOOK_LABELING_READY
```

Every surface the user reads (reports, dashboard, Opus packet) now carries the named playbook, current actionability status, and known failure mode for every signal. Labels are derived deterministically from existing signal fields by a single utility with 16 unit tests; no scoring, threshold, TP/SL, or strategy logic has changed.
