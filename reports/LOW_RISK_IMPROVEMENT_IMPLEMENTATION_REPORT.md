# Low-Risk Improvement — Implementation Report

**Date:** 2026-06-14 · **Scope:** Additive-only diagnostics layer. No production trading behavior is changed.

---

## 1. What was added

### New scripts (all under `scripts/`, read-only)
| File | Purpose |
|---|---|
| `scripts/audit_skipped_opportunities.py` | PART 1 — joins `rejected_ideas` + C-tier signals with their later same-symbol A/B outcomes; classifies as `promoted_winner` / `promoted_loser` / `mixed` / `none`. |
| `scripts/audit_expired_positive_mfe.py` | PART 2 — triggered A/B trades that expired flat after positive MFE; estimates partial-TP uplift vs winner-cut cost. |
| `scripts/audit_crypto_intraday_short_caution.py` | PART 3 — splits crypto intraday A/B shorts by catalyst / failed-reclaim / derivatives / BTC alignment; recommends a Telegram caution label only. |
| `scripts/audit_stocks_cluster_ranking.py` | PART 4 — per-day cluster rankings (mega_tech / semis / index_etfs / ai_infra); does NOT suppress alerts. |
| `scripts/audit_historical_archive_readiness.py` | PART 5 — inspects OHLCV / funding / OI storage; documents append-only conversion proposal. |

### Existing files touched (additive)
| File | Change |
|---|---|
| `scripts/write_obsidian_current_state_dashboard.py` | New `section_low_risk_diagnostics(db)` — section 12 with 4 panels: skipped, expired-MFE, short caution, cluster rank. Pure SQL aggregates. No existing numbers altered. |
| `tests/test_low_risk_diagnostics.py` | New 8-test file pinning the no-mutation invariants. |

### New report outputs (all under `reports/`)
| File | What it contains |
|---|---|
| `SKIPPED_SIGNAL_OPPORTUNITY_AUDIT.md` | Headline counts, top skip reasons, recommendation. |
| `SKIPPED_SIGNAL_FOLLOWUP.csv` | 2,053 rows: each rejected/C-tier candidate with its later A/B follow-up. |
| `EXPIRED_POSITIVE_MFE_OPPORTUNITY_AUDIT.md` | MFE buckets, partial-TP uplift estimate, winner-cut cost. |
| `CRYPTO_INTRADAY_SHORT_CAUTION_STUDY.md` | Subgroup table + caution-label recommendation. |
| `STOCKS_INTRADAY_CLUSTER_RANKING_AUDIT.md` | Per-day cluster rankings; additive only. |
| `HISTORICAL_ARCHIVE_READINESS_AUDIT.md` | Current archive state + smallest safe change proposal. |
| `LOW_RISK_IMPROVEMENT_IMPLEMENTATION_REPORT.md` | This file. |
| `POST_LOW_RISK_IMPROVEMENT_VERIFICATION.md` | Verification checklist. |

---

## 2. Headline findings

### Skipped opportunities (last 14d)

Two methodologies were run; both are in the report:

**Methodology A — strict (SQL-only, A/B confirmation required)**
- Records analyzed: **2,053** (1,500 rejected + 553 C-tier).
- Skips that saved a likely loss (same symbol later A/B and lost): **625**.
- Skips that missed a likely winner (same symbol later A/B and won): **223**.
- Net: **−402** → filters look net-protective by this strict measure.

**Methodology B — rich (candle-based +1R proxy)**
- Records analyzed: **1,353** (800 rejected sampled + 553 C-tier).
- Skips that saved a likely loss: **219**.
- Skips that missed a likely winner (same symbol later A/B and won OR price moved ≥ +1R proxy): **577**.
- Net: **+358** → broader move-proxy says filters cost opportunity.

**Why the disagreement**: Methodology B counts as "missed winner" any short-term ≥+1R price move regardless of whether the symbol ever became A/B again. Many of those moves probably reversed quickly or appeared in periods when entering would have been impractical. The strict measure is the lower bound; the rich measure is the upper bound.

- Top skip reason (rich): `Market regime is mixed; breakout failure risk is elevated.` (347).
- **Interpretation**: filters are doing real work but may be over-suppressing in mixed regimes. **No filter is relaxed.** A deeper study of the "mixed regime" rejection bucket is the highest-priority follow-up.

### Expired positive-MFE
- 1,890 A/B triggered trades total.
- ~85 expired with MFE > +0.5R (potential partial-TP candidates).
- Partial @ +0.5R theoretical uplift: ~+21R; winner-cut cost: similar magnitude → **roughly neutral**. No TP change.

### Crypto intraday shorts
- No-news shorts: ~70% of cohort and carry most of the realized loss.
- Recommended action: **Telegram caution label only** — `⚠️ NO-NEWS-NO-DERIV SHORT — historically thin edge in this regime`.

### Stocks cluster ranking
- Cluster rank shown as additive label per signal (`#N/M` and `cluster risk: low/med/high`).
- NO alerts suppressed.

### Historical archive
- Crypto OHLCV at ALL timeframes is **rolling ~220 candles per file**.
- Funding + OI stored only as latest-cache string blobs.
- Smallest safe change is documented but **not implemented**.

---

## 3. Dashboard panel (section 12)

The Obsidian dashboard now has a new **§12. Low-Risk Diagnostics (additive, read-only)** with 4 sub-panels:
- 12a. Skipped opportunity monitor (last 14d) — top reasons + promotion count.
- 12b. Expired positive-MFE monitor — count + theoretical partial-TP uplift.
- 12c. Crypto intraday short caution — no-news short count + realized R.
- 12d. Stocks intraday cluster ranking — last 24h signal count + pointer to audit.

All 4 panels read from existing tables. None overwrite any previously rendered numbers.

---

## 4. What is explicitly NOT changed

| Surface | Status |
|---|---|
| Scoring / thresholds / TP / SL | UNCHANGED |
| Mode routing / playbook gates | UNCHANGED |
| `config/sizing_weights.yaml` | UNCHANGED |
| `proposed_signals` / `signal_outcomes` / `signal_alerts` / `watchlist_alerts` | UNCHANGED (no INSERT/UPDATE/DELETE from any audit script) |
| Stocks swing / invest pause | KEEP at 0× |
| C-tier / shadow / expansion | NOT promoted |
| Telegram (existing setup + paper-entry alerts) | UNCHANGED |
| Scheduler script | UNCHANGED |
| File-store collectors | UNCHANGED (archive proposal documented only) |

---

## 5. Live numbers verified

| Metric | Before | After |
|---|---:|---:|
| `proposed_signals` count | 1,635 | 1,635 |
| `signal_outcomes` row count | 92,981 | 92,981 |
| `signal_alerts` count | 724 | 724 |
| `watchlist_alerts` count | 195 | 195 |
| `signal_outcomes` sum(`final_r`) | 68,505.0 | 68,505.0 |
| paper_entry alerts | 166 | 166 |

No production data was mutated by any audit script or by the dashboard update.

---

## 6. How to run

```bash
# Run all 5 audits
python scripts/audit_skipped_opportunities.py
python scripts/audit_expired_positive_mfe.py
python scripts/audit_crypto_intraday_short_caution.py
python scripts/audit_stocks_cluster_ranking.py
python scripts/audit_historical_archive_readiness.py

# Refresh dashboard with new §12 panels
python -m scripts.write_obsidian_current_state_dashboard
```

All scripts are idempotent (overwrite report files; no DB writes). Safe to schedule weekly.

---

## 7. Tests

`tests/test_low_risk_diagnostics.py` — **8 passing**:
1. No audit script INSERTs into `proposed_signals`.
2. No audit script imports / calls the Telegram notifier.
3. No audit script UPDATEs `proposed_signals` (C-tier stays C-tier).
4. Expired-MFE audit has no `INSERT/UPDATE/DELETE` on `signal_outcomes`.
5. Cluster ranking audit has no writes to `signal_alerts` / `watchlist_alerts`.
6. Crypto short caution script declares "label only" / "Do not implement".
7. No audit script writes to strategy config; CSV/text writes only go to `reports/`.
8. No audit script contains mutation SQL on `signal_outcomes`.

41/41 in focused regression subset pass.

---

## Verdict

```
LOW_RISK_IMPROVEMENT_DEPLOYED
```
