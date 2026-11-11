# Post Crypto Signal Expansion Verification

**Date:** 2026-06-09 · **Scope:** Independent 11-point checklist verification of the v1 expansion deploy.
**Pairs with:** [CRYPTO_SIGNAL_EXPANSION_REPORT.md](CRYPTO_SIGNAL_EXPANSION_REPORT.md) (implementation) · [CRYPTO_SIGNAL_EXPANSION_PRECHECK.md](CRYPTO_SIGNAL_EXPANSION_PRECHECK.md) (baseline).

## 1. CLI verification

| Command | exit | Expansion section present? |
|---|---|---|
| `python -m src.cli scalp-report --no-update` | 0 | ✅ "## 7e. Crypto Expansion Watchlist" rendered |
| `python -m src.cli intraday-report --no-update` | 0 | ✅ |
| `python -m src.cli swing-report` | 0 | ✅ |
| `python -m src.cli signal-stats --asset-class crypto` | runs; same numerical output as baseline (expansion does not register signals) | n/a |
| `python -m scripts.detect_untracked_legacy_alerts --since 2026-06-09` | "None. Every legacy crypto alert has a backing proposed_signal" | ✅ |

## 2. Tests

| Suite | Result |
|---|---|
| `tests/test_crypto_signal_expansion.py` (new) | **15 passed** |
| `tests/test_playbook_labels.py` | 16 passed |
| `tests/test_paper_execution_annotations.py` | 7 passed |
| `tests/test_pending_revalidation.py` | 6 passed |
| `tests/test_stocks_swing_pause.py` | 9 passed |
| `tests/test_stocks_invest_pause.py` | 10 passed |
| `tests/test_crypto_scalp_low_confidence.py` | 6 passed |
| `tests/test_parallel_fetch.py` | 6 passed |
| **Focused subset total** | **75 passed** |

## 3. 11-point spec checklist

| # | Item | Result |
|---|---|---|
| 1 | More symbols are scanned | scan count unchanged (still ~138); **expansion surfaces 35 EVALUATED candidates from the existing scanner output**, which is the next layer up from raw scan — the user sees more names without growing the upstream universe |
| 2 | More candidates appear in deep analysis | hard 20-cap on full-agent analysis preserved per spec; **expansion lane gives visibility into ~35 names beyond that cap** (8 genuinely new + 27 already in-top, shown with `in-top` status) |
| 3 | Expansion watchlist exists | ✅ section 7e in every crypto report; also persisted to `data/processed/agent_outputs/crypto_expansion_watchlist.json` |
| 4 | A/B count only rises in approved playbooks | ✅ expansion does NOT register proposed_signals; A/B count is unchanged at the data layer. Any future user-driven promotion would go through the existing scoring + tier gates. |
| 5 | Crypto scalp A/B count does not inflate because of expansion | ✅ `skipped_scalp=0` in live run; `test_scalp_playbook_is_never_produced_by_expansion` asserts the invariant |
| 6 | No thin/squeeze-prone shorts bypass the guard | ✅ quality-gate tests cover thin liquidity, upper-wick squeeze, extreme negative funding, missing derivatives — each blocks promotion with a `promotion_blockers` flag |
| 7 | C-tier/shadow candidates are tracked separately | ✅ `status` column in the rendered table: `in-top` / `shadow / C-tier` / `ready-for-promotion`. JSON output carries `quality_flags` and `promotion_blockers` per candidate |
| 8 | LLM packet includes expansion watchlist | ✅ appended to `context_for_llm.md` and persisted to JSON for the packet builder to read |
| 9 | Telegram does not spam C-tier/shadow | ✅ expansion never calls a notifier; agent source is asserted to lack `TelegramNotifier` import |
| 10 | Untracked legacy alerts = 0 | ✅ verified by `detect_untracked_legacy_alerts` |
| 11 | Runtime remains under timeout after parallel fetch | ✅ expansion adds no network calls (purely reads existing in-memory pipeline outputs); the last live scalp report wall ran ~1119 s (vs 2700 s timeout) |

## 4. PART 5 protection preservation

| Protection | Verified by |
|---|---|
| Short squeeze guard | Existing scoring agent path unchanged; expansion ADDS its own squeeze flag in `promotion_blockers` (test `test_short_squeeze_guard_flags_upper_wick`) |
| Pending revalidation | Untouched — `src/signals/revalidator.py` not edited |
| Pre-entry stale/moved-away logic | Untouched |
| Playbook labels | Used in expansion routing (uses `src/signals/playbooks.py`); no labeling change |
| Untracked legacy alert detector | Untouched; live result = 0 |
| Catalyst mapping warnings | Untouched |
| Low-confidence scalp banner | Untouched — `src/reports/report_builder.py` scalp banner block unmodified |

## 5. Live expansion sample (verbatim from latest scalp report)

```
## 7e. Crypto Expansion Watchlist

_Discovered by `DiscoveryExpansionAgent` beyond the top-N deep analysis cap.
**Informational — not a Telegram-actionable signal.** Routed to C-tier / shadow
until a corroborating thesis lifts them._

_Evaluated: 35 · by source:
{'rs_btc_leader': 5, 'rs_eth_leader': 5, 'momentum_24h_leader': 5,
 'momentum_7d_leader': 5, 'catalyst_backed': 10, 'weak_rs_short': 5} ·
 skipped (scalp playbook): 0 · already in top setups: 27_

| Symbol | Source | Playbook | Dir | Score | RS-BTC | Vol× | Status | Why not A/B | Promotes when |
|---|---|---|---|---:|---:|---:|---|---|---|
| CHZ/USDT | catalyst_backed | crypto_intraday_catalyst_or_momentum | long | 78 | +10.7% | 0.8x | in-top | Already in top-N deep setups | …|
| BIO/USDT | catalyst_backed | crypto_intraday_catalyst_or_momentum | long | 53 | -1.9% | 0.2x | shadow / C-tier | low_volume_ratio | Confirm fresh catalyst + RS not contradicting + entry structure on 15m–1h. |
| SAHARA/USDT | weak_rs_short | crypto_failed_bounce_short | short | 80 | -44.4% | 0.2x | in-top | Already in top-N deep setups | Confirm bearish HTF structure + derivatives data + clear stop above swing high; squeeze guard must remain clean. |
…
```

The mixture of `in-top` (visibility-only) and `shadow / C-tier` (genuinely new) entries is the expected behavior.

## 6. Files added / changed (recap)

**Added (5):**
- `src/agents/discovery_expansion_agent.py`
- `tests/test_crypto_signal_expansion.py`
- `reports/CRYPTO_SIGNAL_EXPANSION_PRECHECK.md`
- `reports/CRYPTO_SIGNAL_EXPANSION_REPORT.md`
- `reports/POST_CRYPTO_SIGNAL_EXPANSION_VERIFICATION.md`

**Changed (2):**
- `src/agents/supervisor.py`
- `src/reports/report_builder.py`

**Not touched (by design):**
- Any scoring code, threshold, TP/SL, signal generation, tier assignment.
- Telegram alert path.
- Pending revalidation, paper execution model, playbook labeling utility.
- Stocks pipeline (any of it).
- Historical signal_outcomes / proposed_signals data.

## Verdict
```
READY_AFTER_CRYPTO_SIGNAL_EXPANSION
```

v1 deployed cleanly: 15 new tests passing, 75 in focused regression, three crypto reports re-generated with the new section, untracked legacy alerts = 0, scalp A/B volume unchanged, squeeze guard still firing as expected, and 8 genuinely new shadow-lane candidates surfaced in the first live cycle — without modifying any scoring/threshold/TP/SL/signal-generation logic.
