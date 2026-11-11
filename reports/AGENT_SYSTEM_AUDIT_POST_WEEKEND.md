# Agent-by-Agent System Audit — Post-Weekend

**As of:** 2026-06-07 (Sun) · READ-ONLY · evidence from 72h trade universe +
scheduler/Opus logs.

## Crypto agents
| Agent / system | Status | Latest | Evidence | Pass |
|---|---|---|---|---|
| Momentum scanner | ✅ | every cycle | 46 A/B crypto setups (72h); funnel producing scalp/intraday/swing | PASS |
| Scoring agent | ✅ | every cycle | A/B/C tiering working; squeeze/RS/funding caps applied (`scoring_agent.py:266`) | PASS |
| Regime detector | ✅ | every cycle | "bearish trend (risk-off)" read corroborated by Opus + external prints | PASS |
| RS-leader logic | ✅ | live | `relative_strength_gate` present; longs trading (n=12) | PASS |
| Short squeeze guard | ✅ (idle) | live | wired; 0 caps this window (no thin shorts qualified); clean shorts +16R | PASS |
| Short-side logic | ✅ | live | shorts **+16R PF 3.67 WR 57%** — the weekend engine | PASS |
| Catalyst/news support | ✅ | live | news-backed +9R PF 5.5 vs no-news +7R PF 1.88 | PASS |
| Tracking / outcomes | ✅ | continuous | signal_outcomes updating (last check minutes ago); MFE/MAE/R populated | PASS |
| Reports | ⚠ | intermittent | scalp/intraday reports **time out on some daytime cycles** (P1 infra TODO) | PARTIAL |
| Telegram alerts | ✅ | live | 46 sent / 0 post-fix failures; cooldown/dedup intact; untracked=0 | PASS |

## Stocks agents
| Agent / system | Status | Evidence | Pass |
|---|---|---|---|
| Stock intraday agent | ✅ | intraday A/B **+10R PF 3.5 WR 71%** (n=30) — best stock mode | PASS |
| Stock swing/invest logic | ✅ (paused/thin) | swing capped to watchlist; invest n=9 (6 waiting, 0R) | PASS |
| Swing pause gate | ✅ | 0 new swing A/B; post-fix swing → C | PASS |
| Market-closed gate | ✅ | 48× fired (72h) | PASS |
| Stale post-earnings gate | ✅ | code intact; fires on news+UNKNOWN calendar | PASS |
| Legal/headline gate | ✅ | 9× `legal_headline_risk` (SMCI etc.) | PASS |
| ETF earnings gate | ✅ | ETF severity not_applicable; no false stale | PASS |
| Stock monitor alerts | ✅ | weekend-idle (correct); plain-text + dedup intact | PASS |
| Reports | ✅ | swing report renders watchlist-only banner; intraday/invest generate | PASS |

## Opus enriched-review
| Aspect | Status | Evidence |
|---|---|---|
| Routine running | ✅ | all slots fired every day (06-06 ×6, 06-07 ×2 so far) |
| Market-aware slots | ✅ | titles correct ("Europe / pre-US context — 11:43") |
| Title/header | ✅ | slot + cycle + scheduled-task name in header |
| WebSearch/WebFetch | ✅ | CoinDesk HTTP 200 cited; Invezz 403 handled via WebSearch |
| Source citations | ✅ | external prints cited with dates/values |
| Catalyst coverage | ✅ | reports 27% mapped / 73% unmapped (flagged weak) |
| Prior-review comparison | ✅ | §4 diffs vs prior slot |
| Advisory-only | ✅ | "No auto-trade. Read-mostly per PART 16" present; no edits/trades |
| Telegram summary | ✅ | slot-tagged header; sent |
| Caught issues | ✅ | weekend-closed awareness; flagged stale reports; suggested CLI mapping check (advisory) |
| Wrong claims | none found | external numbers cited & labeled; no fabricated charts (chart tools "not loaded" noted) |

## Summary
All agents **PASS** except crypto **report generation** which is PARTIAL due to
the intermittent daytime scalp/intraday timeout (infra, non-fatal). No agent is
down or producing corrupt data. No agent disabled.
