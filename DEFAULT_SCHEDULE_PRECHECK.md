# Default Schedule — Pre-flight Check

**Date:** 2026-06-01 00:08 EEST (Monday — weekday).
**Target:** start `scripts/run_default_market_schedule.py` as the desk's permanent operating loop.

---

## 1. Date / time / timezone

- Local: **2026-06-01 00:08 EEST** (UTC+3, Asia/Nicosia).
- UTC: 2026-05-31 21:08 UTC.
- Day-of-week: **Monday** → weekday rules apply.
- Effective cycle plan if started now: every 2h → 12 cycles per 24h. First cycle would run stocks (weekday).
- Long-horizon (swing/invest): runs on the **first cycle of each UTC day** then skips for the rest of the day via the `daily_<date>.done` marker.

## 2. Weekend / weekday mode

- **Weekend rule:** Saturday + Sunday → `crypto-only`, `stocks_enabled=False` (verified by `tests/test_default_market_schedule.py::test_saturday_is_weekend` + `test_stocks_off_on_weekend`).
- **Weekday rule:** Mon-Fri → `crypto + stocks intraday` (+ swing/invest once per day).
- `--crypto-only` / `--no-stocks` flag overrides weekday-on-stocks if needed.

## 3. Stocks enabled / disabled

- Today is Monday → **stocks ENABLED** by default.
- The scheduler does NOT check US session hours — stocks-intraday-report runs every 2h on weekdays regardless. Data-freshness stamp in the report tells downstream readers whether prices are stale (e.g. pre-market vs RTH).
- Stocks **scalp** does not exist in this CLI → step is a `note` ("stocks scalp unavailable") that records the gap in the cycle summary without failing.

## 4. Crypto alert registration fix (PART 1)

- `_maybe_register_signals` runs before `_maybe_send_trade_alerts` in `src/agents/supervisor.py`.
- `WatchlistMonitor.register_actionable_ticks` gates `monitor-watchlist` Telegram on registration success.
- `detect_untracked_legacy_alerts --since 2026-05-31` → **None. Every legacy crypto alert has a backing proposed_signal.** ✓
- Track-signals snapshot: `checked=134 updated=0 tp_hits=93 stopped=0 expired=0 not_triggered=0 ambiguous=0 no_ohlcv=0`. Health green.

## 5. Telegram cooldown (PART 2)

- `MaterialImprovementChecker.cooldown_minutes = 45.0` active.
- `entry_change` / `invalidation_change` / `score_improvement` suppressed within 45 min.
- `new_signal` / `tier_upgrade` bypass cooldown.
- Default scheduler **adds a one-shot retry on Telegram `ReadTimeout`** at the cycle-summary level (does not retry an in-pipeline alert; the cooldown handles dedup if the user resends).

## 6. Legal / headline gate (PART 3)

- `src/stocks/legal_risk.py` active.
- `StockTradeIdeaAgent` writes `ACTIVE_LEGAL_HEADLINE_RISK: ...` marker into `idea.avoid_conditions` for indictment / SEC / DOJ / auditor / class action / going concern.
- `MaterialImprovementChecker._classify` returns `legal_block` for any A/B with the marker → Telegram suppressed for those.
- Cycle summary tracks `skipped_legal_block` count per tick.

## 7. Obsidian command status

- `python -m src.cli review-day --no-print --write-obsidian` validated OK in the dry-run CLI surface check.
- Writes `obsidian_vault/11_Trade_Journal/Daily_Reviews/YYYY-MM-DD.md`.
- Failure here is **non-fatal** (the scheduler wraps it in `try/except` via `run_command`).

## 8. Untracked-crypto detector

- `python -m scripts.detect_untracked_legacy_alerts --since 2026-05-31` → 0 untracked.
- Runs on every cycle; if it returns non-zero the cycle summary will surface that count and Telegram alert text will include it.

## 9. Old scheduler / monitor process check

- `Get-CimInstance Win32_Process -Filter "Name='python.exe'"` filtered for `run_24h|run_default` → **no matches**.
- The previous 24h crypto-only scheduler died during cycle 10 (Windows DLL init failure) and was not restarted. Cycles 11 + 12 are not running.
- No background monitor processes left over.

## 10. Test suite status

- `tests/test_default_market_schedule.py` → **17/17 pass**.
- Full suite → **177 passed in 3:43**.
- Pre-existing tests (PART 1–5 regressions) all still green.

## 11. CLI surface validation

Dry-run validated 11 CLI commands:

| Command | Status |
|---------|--------|
| `track-signals` | OK |
| `scalp-report` | OK |
| `intraday-report` | OK |
| `swing-report` | OK (used for daily-once crypto long-horizon) |
| `active-signals` | OK |
| `signal-stats` | OK |
| `monitor-watchlist` | OK |
| `review-day` | OK |
| `stocks-intraday-report` | OK |
| `stocks-swing-report` | OK |
| `stocks-invest-report` | OK |
| `stocks-scalp-report` | **not present** — step is a `note`, scheduler continues |
| (crypto invest) | **not present** — `swing-report` covers long-horizon for crypto |

## 12. LLM-auto-invoke check (Opus discipline)

- Dry-run validated that `build_cycle_steps` output contains **zero** of: `opus`, `anthropic`, `claude api`, `enriched-review` tokens. ✓
- `tests/test_default_market_schedule.py::test_no_llm_tokens_in_any_cycle_plan` pins this contract across weekend/weekday/long-horizon variants.
- Enriched review remains manually triggered via the `enriched-review` skill (Sprint cycle-3/8/9 outputs prove the manual path works).

## 13. Go / no-go

| Item | Status |
|------|--------|
| Date / time / timezone known | ✅ Mon 00:08 EEST |
| Weekend / weekday rules in code | ✅ tests pin both |
| Stocks weekend-skip | ✅ verified |
| `--crypto-only` flag | ✅ validated end-to-end |
| `--run-once` flag | ✅ validated |
| `--date` override flag | ✅ available |
| Daily-once long-horizon | ✅ marker-file gate |
| Crypto legacy alert tracking fix (PART 1) | ✅ active, 0 untracked |
| Telegram 45-min cooldown (PART 2) | ✅ active |
| Stocks legal-risk gate (PART 3) | ✅ active |
| Source-discipline skill (PART 4) | ✅ manual-only |
| Daily Obsidian export (PART 5) | ✅ validated |
| Windows DLL init retry (cycle-10 fix) | ✅ implemented + tested constant |
| Telegram ReadTimeout retry | ✅ implemented |
| Duplicate monitor protection | ✅ PID-lockfile pattern |
| No auto-trade | ✅ confirmed (no execution layer in `src/`) |
| No auto-Opus / LLM | ✅ test + dry-run gate |
| Full test suite | ✅ 177 passed |

**Verdict: READY_TO_RUN_DEFAULT_SCHEDULE.** Awaiting user explicit approval to start.
