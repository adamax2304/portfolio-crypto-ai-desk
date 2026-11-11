# Post Mode-Routing-Update Verification

**Date:** 2026-06-09 · **Scope:** Verify the two mode-routing changes from the Mode Viability Audit:
- PART 1: crypto scalp — keep active, mark low-confidence (no demotion, no suppression).
- PART 2: stocks invest — watchlist-only soft pause (mirror of swing-pause gate).
- PART 3: stocks swing pause preserved unchanged.

No scoring/threshold/TP/SL changes. No crypto demotion. No auto-trade. Telegram collector left running untouched.

## 1. Tests
| Suite | Result |
|---|---|
| `tests/test_stocks_swing_pause.py` | 9 passed |
| `tests/test_stocks_invest_pause.py` (new) | 10 passed |
| `tests/test_crypto_scalp_low_confidence.py` (new) | 6 passed |
| `tests/test_stocks_market_closed_stale.py` (1 updated) | 13 passed |
| `tests/stocks/test_stocks_scoring_and_ideas.py` (1 updated) | 7 passed |
| `tests/test_parallel_fetch.py` (regression) | 6 passed |
| **Focused subset total** | **48 passed** |
| **Full regression** (`tests/`) | **completed (exit 0)** |

Updates to existing tests:
- `test_invest_not_swing_paused` → `test_invest_not_affected_by_swing_cap`: now only checks the swing CAP marker is absent (invest itself becomes C-tier via its own gate, tested in the new file).
- `test_invest_not_affected_by_market_closed` → `test_invest_not_affected_by_market_closed_or_swing_caps`: same rationale.
- `test_trade_idea_agent_produces_stocks_asset_class`: relaxed swing-mode tier assertion to allow C (swing-pause demotion) with positive assertion that the swing CAP is present in that case.

## 2. Report CLI verification

### 2.1 Crypto reports
| Command | exit | report path | LLM packet |
|---|---|---|---|
| `scalp-report --no-update` | 0 | `data/reports/scalp/2026-06-09_13-46_scalp_report.md` | refreshed |
| `intraday-report --no-update` | 0 | `data/reports/intraday/2026-06-09_13-49_intraday_report.md` | refreshed |

Scalp report header (verified verbatim):
```
Mode: scalp
Data freshness: 2026-06-09 13:30:00+00:00
Market regime: range/chop (neutral)

> **CRYPTO SCALP — low confidence.** Entry edge exists (100% of expired scalps had positive MFE,
> avg +0.54R) but TP1/2h horizon mismatch caps capture (1W/7L over 14d, PF 0.14). Scalp remains
> active for data collection; re-audit at 20 closed A/B scalp signals. Treat A/B scalp ideas with
> lower confidence than intraday/swing.
```
Intraday report has NO scalp banner — verified by `test_intraday_report_has_no_scalp_banner` and report file inspection.

### 2.2 Stocks reports
| Command | exit | result |
|---|---|---|
| `stocks-intraday-report` | 0 | A/B intraday continues normally (no new banner) |
| `stocks-swing-report` | 0 | banner: `**STOCKS SWING — watchlist / research only.**` — pre-existing pause preserved |
| `stocks-invest-report` | 0 | **A/B ideas=0**, C watchlist=10, signals registered=0 |

Invest report header (verified verbatim):
```
Mode: invest
Asset class: stocks
Market session: regular session
Data freshness: 2026-06-09 14:04 UTC
> **STOCKS INVEST — watchlist / research only after mode viability audit: 0W/7L over 14d,
> same failure mode as paused stocks swing.** Invest A/B candidates are capped to C
> (no Telegram A/B alerts) until reviewed; they remain listed below for research.
```

## 3. Signal stats
- `signal-stats --asset-class crypto`: rendered; B-tier diagnostic line: "tier=B: triggered winrate 29% is low. Consider reviewing entries." (advisory only, no auto-action).
- `signal-stats --asset-class stocks`: rendered; legacy diagnostics on A/C tiers preserved.

## 4. Untracked legacy alerts
```
python -m scripts.detect_untracked_legacy_alerts --since 2026-06-09
→ "None. Every legacy crypto alert has a backing proposed_signal (or there were no crypto alerts)."
```
✅ **untracked = 0.**

## 5. 11-point verification checklist
| # | Item | Result |
|---|---|---|
| 1 | crypto scalp still generates actionable A/B if qualified | ✅ scalp report shows actionable A/B candidates (banner is annotation only) |
| 2 | crypto scalp low-confidence note appears in reports / Telegram | ✅ report banner + supervisor + watchlist_monitor alert lines verified |
| 3 | crypto swing remains actionable | ✅ crypto swing untouched (no scope change) |
| 4 | crypto intraday remains actionable | ✅ intraday-report ran with no new banner; A/B path unchanged |
| 5 | stocks intraday remains actionable | ✅ stocks-intraday-report ran; no invest/swing banners |
| 6 | stocks swing remains C/watchlist | ✅ swing-report ran, banner present; gate unchanged |
| 7 | stocks invest is now C/watchlist | ✅ invest-report shows A/B=0, C=10, all signals C-capped |
| 8 | no stocks invest A/B Telegram alerts | ✅ `signals registered=0` in invest run |
| 9 | untracked legacy alerts = 0 | ✅ detector returned `None` |
| 10 | LLM packets refresh | ✅ `data/processed/llm_analysis_packet.md` (crypto) + `llm_stocks_packet.md` (stocks) updated |
| 11 | no auto-trade | ✅ no auto-trade path touched; gate-only changes; manual paper-trading still required |

## 6. Scheduler deployment
| Before | After |
|---|---|
| Scheduler python PID **14692** (born 2026-06-08 23:06 EEST), running old code | Scheduler python PID **12380** (born 2026-06-09 17:07 EEST), running updated code |
| Wrapper: `cmd.exe ... autostart_scheduler.bat` (PID 5792, kept alive) | same wrapper, relaunched python child |
| Telegram collector PID **9240** | unchanged — **NOT restarted** per spec |

Procedure:
1. Old scheduler PID 14692 terminated (`Stop-Process -Force`); it was between report cycles, no in-flight crypto/stocks report run.
2. `autostart_scheduler.bat` relaunched python within ~10s as PID 12380.
3. Telegram collector (PID 9240) left running.
4. Next scheduler cycle will execute against updated `src/agents/supervisor.py`, `src/stocks/agents/trade_idea_agent.py`, `src/stocks/reports/stocks_report_builder.py`, `src/reports/report_builder.py`, `src/agents/watchlist_monitor.py`.

## 7. Files changed
| File | Change |
|---|---|
| `src/stocks/agents/trade_idea_agent.py` | + invest watchlist gate (mirror of swing gate) |
| `src/stocks/reports/stocks_report_builder.py` | + invest watchlist-only banner |
| `src/reports/report_builder.py` | + scalp low-confidence banner |
| `src/agents/supervisor.py` | + scalp low-confidence line in `_format_idea_alert` |
| `src/agents/watchlist_monitor.py` | + scalp low-confidence line in `format_alert` |
| `tests/test_stocks_invest_pause.py` (new) | 10 invest pause tests |
| `tests/test_crypto_scalp_low_confidence.py` (new) | 6 scalp annotation tests |
| `tests/test_stocks_swing_pause.py` | 1 test renamed/updated (invest cap rationale) |
| `tests/test_stocks_market_closed_stale.py` | 1 test renamed/updated (invest cap rationale) |
| `tests/stocks/test_stocks_scoring_and_ideas.py` | swing-mode tier assertion relaxed (allows pause-induced C) |

## 8. Reports created
- `reports/STOCKS_INVEST_WATCHLIST_PAUSE_FIX_REPORT.md`
- `reports/CRYPTO_SCALP_LOW_CONFIDENCE_REPORTING.md`
- `reports/POST_MODE_ROUTING_UPDATE_VERIFICATION.md` (this file)

## Final
```
READY_AFTER_MODE_ROUTING_UPDATE
```

- Code + tests + reports + scheduler deployment all verified.
- Crypto scalp stays actionable; low-confidence annotation surfaces in reports and Telegram.
- Stocks invest A/B is now soft-paused to C (mirror of swing); next live signal will validate gate at production runtime.
- Stocks swing pause preserved unchanged; 0 A/B leaks.
- No auto-trade, no scoring/threshold/TP/SL changes, Telegram collector untouched.
