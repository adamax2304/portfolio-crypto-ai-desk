# Post-Weekend Fix Verification (live)

**As of:** 2026-06-07 (Sun) · window 72 h. Verifies all prior fixes are still
active in production after the weekend run. READ-ONLY.

## Crypto
| Check | Status | Evidence (72h) |
|---|---|---|
| Short squeeze-risk guard wired | ✅ | `scoring_agent.py:266` calls `assess_short_squeeze`; import intact |
| Thin/bounce shorts capped to C | ✅ (no-op window) | **0** squeeze-caps fired — no thin/bounce short candidates qualified this window; guard live, just nothing to cap |
| Clean liquid shorts allowed | ✅ | A/B shorts **+16R PF 3.67 WR 57%** (n=34) — clean shorts flowing & winning |
| RS-leader longs allowed | ✅ | `relative_strength_gate` + scanner RS logic present; longs trading (n=12) |
| Untracked legacy alerts = 0 | ✅ | 0 crypto alerts without backing proposed_signal; 0 bad asset_class |

## Stocks
| Check | Status | Evidence |
|---|---|---|
| Swing pause active (A/B → C) | ✅ | post-fix swing signals = **2× tier C**, **0 new A/B**; all 14 swing A/B in window are **pre-fix** (created 06-04 14:55 / 06-05 14:50, before fix 06-05 19:00 UTC) |
| No swing A/B Telegram alerts | ✅ | new swing never enters A/B set; pre-fix swing all already-alerted (deduped) |
| Market-closed intraday gate | ✅ | **48×** `market_closed_intraday_planning_only` fired (72h) |
| Post-earnings stale gate | ✅ | gate code intact; fires on news-confirmed earnings + UNKNOWN calendar |
| SMCI legal/headline gate | ✅ | **9×** `legal_headline_risk`; SMCI export-control 8-K flagged in Opus |
| ETF earnings N/A | ✅ | ETF earnings severity not_applicable; no false stale flags |
| Telegram plain-text fix | ✅ | sends use `parse_mode=""` |
| No new failed:HTTPError 400 | ✅ | **0** `failed:HTTPError` after fix (06-05 19:00 UTC). 15 failures in window are all **pre-fix** |

## Reporting
| Check | Status | Evidence |
|---|---|---|
| A/B-only headline performance | ✅ | headline metrics computed on A/B only; C-tier reported separately (crypto C=0, stocks C −12R shown apart) |
| C-tier separated | ✅ | stocks C-tier (95 sigs, −12R PF 0.25) excluded from headline |
| LLM packets refreshed | ✅ | `data/processed/llm_stocks_packet.md` refreshed on report runs; Opus reads packets |
| Catalyst reached reports/packets | ✅ | `data/catalysts/2026-06-07/catalyst_events.jsonl` (601 rows) + baskets; Opus cites them |
| Obsidian dashboards fresh | ✅ | scheduler runs `refresh obsidian dashboard` each cycle (exit=0 in log) |

## Conclusion
**All prior fixes remain active and correct after the weekend.** The only
"unverified-by-organic-event" item is the squeeze-guard cap (no qualifying thin
short appeared this window) — the code path is intact and clean shorts passed &
won (+16R), so the guard is not over-capping. Stocks swing pause + Telegram-400
fix both confirmed with zero regressions.
