# System Signal Tracking Verification — 2026-05-28

**Run at:** 2026-05-28 ~23:55 EEST
**Context:** autonomous frequent scheduler ran 01:22 → ~14:12 EEST (PC likely slept after ~14:12; last report `2026-05-28_11-12` UTC = 14:12 EEST). No scheduler/monitor process running now — clean verification window.

---

## 1. Executive Summary

**Status: WORKING.** Signal recording, tracking, statistics, report integration, and the stocks Telegram ledger all function correctly. No critical bug found → **no code changes made.**

Main findings:
- ✅ Signal registration, tracking, active-signals, signal-stats all work; `no_ohlcv=0`, `errors=0`.
- ✅ Recent Signal Performance section in reports **matches** signal-stats exactly (sample, PF, tier counts).
- ✅ LLM packets fresh + asset-class isolated.
- ⚠️ Stocks raw stats inflated ~8× by repeated registrations (deduped view provided).
- ⚠️ Crypto uses **legacy `watchlist_alerts`** path → 0 rows in modern `signal_alerts` ledger (known asymmetry, not a bug).
- ⚠️ Obsidian logging dormant (no new signal logs / reviews written; `update-obsidian-context` still TODO).

**Safe to proceed to fresh analysis: YES.**

---

## 2. Signal Recording

| Check | Result |
|-------|--------|
| A-tier ideas registered | ✅ (stocks A raw=68) |
| B-tier ideas registered | ✅ (stocks B raw=294, crypto B raw=13) |
| C-tier registered only with entry/trigger | ✅ (C raw=203, all carry entry zone + invalidation) |
| Rejected NOT treated as active | ✅ (rejected never enter `proposed_signals` as active) |
| proposed_signal vs executed_trade vs signal_alert separated | ✅ — three distinct tables: `proposed_signals`, (no executed-trade table — user does not log real trades here), `signal_alerts` / `watchlist_alerts` |

Required fields verified on recent crypto + stocks signals — all present: `signal_id, asset_class, symbol, mode, direction, tier, score, confidence, entry_low/high, invalidation, tp1/tp2/tp3, created_at, status, source_report_path, thesis`.

---

## 3. Signal Tracking

```
python -m src.cli track-signals --all
checked=311 updated=149 tp_hits=63 stopped=0 expired=142
not_triggered=7 ambiguous=0 no_ohlcv=0 errors=0
```

- ✅ Crypto signals tracked.
- ✅ Stocks signals tracked.
- ✅ `no_ohlcv=0` — cross-asset OHLCV path resolution works.
- ✅ `errors=0`.
- ✅ Outcomes written back to DB (149 updates this pass; 142 expired = end-of-day validity windows closing — healthy).

---

## 4. Signal Statistics

### Raw (`signal-stats`)
| Class | Sample | Confidence | Triggered | Wins | Losses | PF | avgR | totalR |
|-------|-------:|-----------|-----------|-----:|-------:|---:|-----:|-------:|
| Crypto | 13 | **weak** | 11 | 1 | 5 | 0.2 | −0.36R | **−4.0R** |
| Stocks | 565 | "reliable"* | 285 | 62 | 41 | 2.07 | +0.16R | **+45.0R** |

\* "reliable" label is misleading — inflated by duplicate registrations.

### Deduped (one canonical signal per unique setup)
| Bucket | Raw n | Dedup n | PF | totalR | winrate |
|--------|------:|--------:|---:|-------:|--------:|
| crypto_AB | 13 | 11 | 0.00 | −5.0R | 0% |
| crypto_scalp_AB | 8 | 6 | 0.00 | −1.0R | 0% |
| crypto_intraday_AB | 5 | 5 | 0.00 | −4.0R | 0% |
| stocks_AB | 362 | **45** | 3.50 | +5.0R | 75% |
| stocks_A_only | 68 | 11 | 1.00 | +0.0R | 50% |
| stocks_B_only | 294 | 34 | inf | +5.0R | 100% |
| stocks_C_only | 203 | 29 | 0.67 | −1.0R | 40% |

**Inflation factor:** stocks ~8× (raw 362 / dedup 45). Crypto ~1.2× (raw 13 / dedup 11 — minimal).

**Sample-size verdict:**
- Crypto: 11 unique A/B → **weak/anecdotal**, and **net negative** (0 wins on dedup, −5R). Do NOT tune scoring on this.
- Stocks: 45 unique A/B → **moderate**; positive (PF 3.50, +5R dedup) but B-only winrate=100% is a small-sample artefact, not a durable edge.

**Note on discrepancy:** `signal-stats` crypto shows 1 win; dedup shows 0. This is because the dedup helper counts wins via the `final_outcome` field, which lags behind the live `status` for the 1 TAO TP1 (booked but `final_outcome` not yet stamped "win"). Cosmetic limitation of the read-only dedup script, not a tracking bug.

---

## 5. Reports and LLM Packets

### Recent Signal Performance section — VERIFIED CORRECT
Latest stocks report (`2026-05-28_11-12` UTC) section:
```
Sample size: 565 (confidence=reliable)
A-tier: 68 | B-tier: 294 | C-tier: 203
Triggered: 285 / 565 (50.4%)
Wins: 62 | Losses: 41 | Ambiguous: 1
TP1 hit rate: 22.1% | Stop hit rate: 23.2%
Triggered winrate: 21.8% | Avg R: 0.158 | Total R: 45.00 | PF: 2.07
Active right now: 314
```
- ✅ Sample 565 matches `signal-stats` (565)
- ✅ PF 2.07 matches `signal-stats` (2.0714)
- ✅ A/B/C 68/294/203 matches dedup raw counts
- ✅ No zero values, no schema errors (the earlier report_section bug is fixed and holding)

### LLM packet freshness
| Packet | Last modified (EEST) | Status |
|--------|----------------------|--------|
| context_for_llm.md | 2026-05-28 14:05 | ✅ fresh |
| llm_analysis_packet.md (crypto) | 2026-05-28 14:05 | ✅ fresh |
| llm_stocks_packet.md | 2026-05-28 14:12 | ✅ fresh |

- ✅ Each packet refreshed by its report run (timestamps align with last cycle ~14:12).
- ✅ Crypto packet contains only crypto candidates; stocks packet only stocks (asset-class isolation preserved).
- ✅ Signal performance summary present in both packets.

---

## 6. Obsidian / Notebook

| Item | Status |
|------|--------|
| Proposed signals → Obsidian | ❌ not written (only SQLite registry) |
| Outcomes → Obsidian | ❌ not written |
| Daily reviews → Obsidian | ❌ only 1 stale weekly review from 2026-05-24 |
| Crypto/stocks separated in Obsidian | folders exist, no live data |
| `update-obsidian-context` | ❌ still TODO stub |
| LLM can use Obsidian dynamic context | ❌ `Current_Context_For_LLM.md` is template only |

**Limitation (not fixed today, out of scope):** Obsidian is a static knowledge base; the live signal/outcome/review writers are not implemented. The SQLite registry + `signal-stats` + the in-report Recent Signal Performance section cover the same information, so the LLM is not starved — it just doesn't read from Obsidian.

No small safe command exists to populate it (`update-obsidian-context`, `log-idea-to-obsidian`, `review-day` are all stubs). Marked as limitation.

---

## 7. Telegram Alerts

| Check | Stocks | Crypto |
|-------|--------|--------|
| A/B can alert | ✅ (178 sent) | ✅ via legacy path |
| C-tier alerts | ✅ blocked | ✅ blocked |
| Rejected alerts | ✅ blocked | ✅ blocked |
| No alert without invalidation | ✅ | ✅ |
| Duplicate alerts skipped | ✅ (`signal_alerts` ledger) | ✅ (cooldown) |
| Materially improved re-alerts | ✅ (`MaterialImprovementChecker`) | ⚠️ only tier upgrades |
| dry_run does not block real alerts | ✅ (verified earlier when 8 dry_run rows cleared → real sends fired) | n/a |
| Alert ledger | `signal_alerts` (modern) | `watchlist_alerts` (legacy) |

`alert-status`:
- **Stocks:** 362 A/B, 178 alerts sent, 184 not-alerted (duplicates of same setups), 0 dup-skipped estimate.
- **Crypto:** 13 A/B, **0 in `signal_alerts`** — confirms crypto uses legacy `watchlist_alerts`. Not broken; just a different, lower-reactivity path. Documented in `CRYPTO_SIGNAL_ABSENCE_AUDIT.md`.

---

## 8. Issues Found

| Severity | Issue |
|----------|-------|
| **Critical** | None |
| **High** | None |
| **Medium** | (M1) Stocks signal registry inflated ~8× by repeated registrations — cosmetic, inflates "reliable" label. (M2) Crypto alert path is legacy `watchlist_alerts`, much less reactive than stocks. |
| **Low** | (L1) Obsidian live logging dormant. (L2) dedup helper win-count lags `final_outcome` vs live `status` (1 crypto win not reflected). (L3) Autonomous scheduler appears to have stopped after ~14:12 EEST (PC likely slept) — operational, not a code bug. |

None of these block analysis. None warrant a code change under the "fix only critical technical bugs" rule.

---

## 9. Fixes Applied

**None.** No critical technical bug was found. Per instructions, no code, scoring, threshold, agent, or architecture changes were made.

---

## 10. Final Verdict

**READY — proceed to fresh analysis** (with documented limitations: stocks stats inflation → use deduped view; crypto alert asymmetry; Obsidian dormant).
