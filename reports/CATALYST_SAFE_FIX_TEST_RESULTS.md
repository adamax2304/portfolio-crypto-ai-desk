# Catalyst Safe-Fix Test Results (PART 10)

**Date:** 2026-06-15

## New test file: `tests/test_catalyst_safe_fixes.py` — 14 passing

| Test | Covers |
|---|---|
| test_1 / test_2 | stocks `news_supported` flag set with news / not without (PART 1) |
| test_3 | funding snapshot insert + dedup (PART 2) |
| test_4 | OI snapshot insert (PART 2) |
| test_5 | archive helper best-effort: skips failed records, no raise, None store ok |
| test_6 | scoring agents do NOT import archive / reference snapshot tables |
| test_7 | crypto catalyst labels (freshness/source/deriv/mapping) |
| test_8 | technical signal → none; "no squeeze" not flagged as risk |
| test_9 | telegram block catalyst-backed |
| test_10 | telegram block stocks "not available for stocks" |
| test_11 | setup alert includes catalyst block + header + "No paper entry yet." |
| test_12 | paper-entry includes catalyst block + disclaimer |
| test_13 | technical setup shows "Catalyst: none" |
| test_14 | compute_labels is pure (no signal mutation) |

## Broader focused regression

```
$ pytest test_catalyst_safe_fixes + test_telegram_standardization + test_paper_entry_alerts
         + test_sizing + test_playbook_labels + test_low_risk_diagnostics + test_pending_revalidation
101 passed
```

No previously passing test regressed. Telegram standardization (38), paper-entry
(16+), sizing (19), low-risk diagnostics (8) all still green with the new
catalyst block inserted.

## Scope verification (grep)

```
grep -c "derivatives_archive|funding_snapshots|oi_snapshots" \
     src/agents/scoring_agent.py src/stocks/agents/scoring_agent.py
→ 0  (both files)
```
Confirms the archive is write-only and not on any scoring read-path.
