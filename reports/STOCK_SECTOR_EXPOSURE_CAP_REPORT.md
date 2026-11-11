# Sector / Risk-Bucket Exposure Cap — Rule B (PART 3)

**Date:** 2026-06-16 · `src/signals/portfolio_caps.py`

Per `risk_bucket` + `direction`, rank existing open exposure + surviving candidates
(best-first) and cap effective weight:

| rank | weight | status |
|------|--------|--------|
| 1 | 1.0× | actionable |
| 2 | 0.5× | half_size |
| 3+ | 0.0× | shadow_sector_cap |

**Counted toward the cap:** open/triggered/waiting A/B stocks-intraday positions in the
same bucket+direction, plus surviving batch candidates (after Rule A).
**Excluded:** C-tier, rejected, expired/stopped/closed, stocks swing/invest (paused),
crypto, crypto scalp shadow, already-shadowed proxy duplicates, opposite direction,
different bucket, unknown bucket (→ `unknown_bucket_actionable`, not capped).

**Conservative combine with playbook weight:** `effective = min(playbook_weight, cap_weight)`
— so an A-tier long that already carries the 0.5× overpromotion override never gets
*upsized* by the cap.

**Examples (tested):** AMD(90)/NVDA(80)/SMCI(70) semis-long same day → 1.0× / 0.5× / 0×.
Existing open SMH long → new AMD long = rank 2 → 0.5×. Opposite direction / different
bucket → rank 1 (uncapped).

Tests: `test_3_4_5...`, `test_6_existing_active_position_counts`,
`test_7_opposite_direction_not_capped`, `test_8_different_bucket_not_capped`, live
`test_live_second/third_exposure...`. Raw R, score, tier, TP/SL untouched
(`test_13_14...`). **PART 3 status: DONE.**
