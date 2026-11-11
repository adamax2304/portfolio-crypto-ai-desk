# Playbook Labeling — Implementation Report

**Date:** 2026-06-09 · **Scope:** Annotation-only labeling layer that names every signal's trading playbook + current status + known failure mode. No scoring, threshold, TP/SL, or signal-generation changes. No auto-trade. No data deleted.
**References:** [STRATEGY_PLAYBOOK_AUDIT.md](STRATEGY_PLAYBOOK_AUDIT.md) (the contract) · [CURRENT_TRADING_PLAYBOOKS.md](CURRENT_TRADING_PLAYBOOKS.md) (the summary).

## 1. Single source of truth

File: [src/signals/playbooks.py](../src/signals/playbooks.py) (~210 lines, pure stdlib).

Exposes:
- 9 playbook constants (6 crypto + 3 stocks) and 5 overlay constants.
- 3 status constants: `actionable`, `low_confidence`, `watchlist_only`.
- Dataclass `PlaybookLabel` with `to_dict()` and `to_markdown_block(heading_level=…)` helpers.
- `label_for(signal_dict)` — primary entry point; safe against missing fields.
- `label_from_trade_idea(idea)` — convenience for `TradeIdea` objects.

### Routing rules (one line each)
| asset × mode × direction × news | Playbook | Status |
|---|---|---|
| crypto / scalp / any | `crypto_scalp_momentum_continuation` | low_confidence |
| crypto / intraday / long / catalyst | `crypto_intraday_catalyst_or_momentum` | actionable (preferred) |
| crypto / intraday / long / no-catalyst | `crypto_intraday_catalyst_or_momentum` | actionable (weaker) |
| crypto / intraday / short | `crypto_failed_bounce_short` | actionable |
| crypto / swing / long | `crypto_swing_narrative_rs_momentum` | actionable (primary) |
| crypto / swing / short | `crypto_failed_bounce_short` | actionable |
| crypto / invest / any | `crypto_swing_narrative_rs_momentum` | actionable (rare path) |
| stocks / intraday / any | `stocks_intraday_rth_momentum` | actionable (primary) |
| stocks / swing / any | `stocks_swing_watchlist_rs_rotation` | watchlist_only |
| stocks / invest / any | `stocks_invest_watchlist_30d_thesis` | watchlist_only |

### Overlays (additive)
- `catalyst_backed` — `news_supported=1`.
- `rs_leader` — score ≥ 80 on crypto intraday/swing long (top-decile proxy).
- `short_playbook` — direction = short.
- `low_confidence_scalp` — every crypto scalp.
- `watchlist_only_mode` — every stocks swing/invest.

## 2. Surfaces wired

| Surface | File | What is rendered |
|---|---|---|
| Crypto reports (scalp/intraday/swing) | `src/reports/markdown_templates.py` → `trade_idea_markdown` | A "#### Playbook" block under every idea card with playbook, status, overlays, why, failure mode, manual hint. Applies to A/B and C-tier sections. |
| Stocks reports (intraday/swing/invest) — A/B section | `src/stocks/reports/stocks_report_builder.py` → `_ideas_section` | Same "#### Playbook" block under every A/B idea. |
| Stocks reports — C/Watchlist section | `src/stocks/reports/stocks_report_builder.py` → `_watchlist_section` | Compact `playbook=<label> status=<status>` suffix on each watchlist line. |
| Crypto LLM packet | `src/analysis/packet.py` → new `_build_playbook_context_block()` + slot in `sections` | Dedicated "Strategy Playbook Context" section at the top with the 14d performance table + overlay primer + decision shortcuts. |
| Stocks LLM packet | `src/stocks/llm_packet.py` → reuses crypto's `_build_playbook_context_block` | Same context block included at the head of the stocks packet. |
| Obsidian dashboard — open trades | `scripts/write_obsidian_current_state_dashboard.py` → `render_open_trade` | Adds 3 lines per open trade: `Playbook · status · overlays`, failure mode, manual review hint. |
| Obsidian dashboard — last 5 crypto / stocks trades | `render_recent_trade` | Adds `playbook=<label>` in the headline of each row. |
| Obsidian dashboard — new section "8b. Playbook Performance Snapshot" | `section_playbook_performance` | 9-row table: n / closed / W / WR / PF / netR per playbook from live `signal_outcomes`. |

## 3. Tests
File: [tests/test_playbook_labels.py](../tests/test_playbook_labels.py) — **16 tests, all pass**:

| Group | Coverage |
|---|---|
| Primary routing | scalp / intraday with catalyst / intraday no catalyst / swing long / intraday short / swing short |
| Stocks routing | stocks intraday actionable / stocks swing watchlist / stocks invest watchlist |
| Overlay rules | RS-leader only on high-score crypto intraday/swing long; catalyst on news=1; short on direction=short |
| Rendering | markdown block contains heading + playbook + status + overlays + why + failure mode |
| Robustness | unknown mode falls through safely; empty dict does not raise |

## 4. Verification — what the user will see now

### In a crypto report (scalp example)
```
### Trade Idea #2 - LONG ZEC/USDT

Score: 66/100
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

**Thesis**
…
```

### In a stocks report
```
### Idea #1 — B XOM long
#### Playbook
- Playbook: `stocks_intraday_rth_momentum`
- Status: **actionable**
- Overlays: rs_leader
- Why this playbook: stocks intraday B-tier 14d: WR 55%, PF 2.03, +80R; shorts subset PF 9.00
- Known failure mode: A-tier overpromotion on losing names — NVDA/SMCI/SMH longs structurally lose in this regime
- Manual review hint: Spot-check chart structure against thesis; avoid NVDA/SMCI longs without strong catalyst.
- Score: 81.00
…
```

### In LLM packets (Opus context)
Top of the packet now carries a "## Strategy Playbook Context" section with the full playbook → status → 14d performance table + decision shortcuts. Opus sees this before any specific idea, so its synthesis can reason by named playbook instead of only by tier/score.

### In Obsidian dashboard
- Every open trade now shows a `Playbook · status · overlays` line + failure-mode + manual-hint.
- Last 5 trades show `playbook=<label>` in the headline.
- A new "## 8b. Playbook Performance Snapshot" section renders a 9-row table with live 14d PF / WR / netR per playbook.

## 5. What was NOT changed
- No scoring weights.
- No thresholds.
- No TP/SL geometry.
- No signal generation (`technical_setup_agent`, `scoring_agent`, `trade_idea_agent` left untouched).
- No tier assignment.
- No Telegram alert text (so existing alert format/cooldowns are unchanged).
- No data deletion. No reclassification of historical outcomes.

## 6. Files added / changed
**Added (2):**
- `src/signals/playbooks.py`
- `tests/test_playbook_labels.py`

**Changed (5):**
- `src/reports/markdown_templates.py` — render playbook block on every crypto idea.
- `src/stocks/reports/stocks_report_builder.py` — render playbook block on every stocks idea + suffix on watchlist rows.
- `src/analysis/packet.py` — new `_build_playbook_context_block` + slot in section list (crypto packet).
- `src/stocks/llm_packet.py` — include the same block at the head of the stocks packet.
- `scripts/write_obsidian_current_state_dashboard.py` — playbook lines on open/recent trades + new "8b. Playbook Performance Snapshot".

## Verdict
```
PLAYBOOK_LABELING_DEPLOYED
```

Every A/B and C-tier idea in every report, every active and recent trade in the dashboard, and the Opus packet header now carries the named playbook + actionability status + known failure mode + manual-review hint. The mapping comes from a single utility (`label_for`) backed by 16 unit tests. The Opus packet additionally carries the canonical playbook-context block at the top so strategy-aware synthesis is the default reasoning frame.
