# Stocks-Intraday LLM Review packet — cycle: power_hour

**ADVISORY / SHADOW. You (the reviewer) MUST NOT create trades, change score/tier/TP/SL, or unlock live. Output one of: approve / wait / reject / needs_human_review per candidate.**

## Actionable A/B stock-intraday candidates (last 48h): 4
- `sig_c16f6bd7fdd00640` REGN long tier=A @ 2026-11-11T20:46:09.711863+00:00
- `sig_091c5212bd41198a` REGN long tier=A profile=stocks_intraday_breakout_1bar_paper_v1 @ 2026-11-11T18:39:06.150810+00:00
- `sig_5da5baae4de908ad` REGN long tier=A profile=stocks_intraday_pullback_vwap_paper_v2 @ 2026-11-11T18:39:06.150810+00:00
- `sig_7fc833ccbbb90010` NOW short tier=B @ 2026-11-10T20:23:28.154867+00:00

## Demoted-to-C watchlist (with gate demotion reasons): 40
- `sig_83b8b2705dbf8e07` REGN long — lunch_requires_strong_confirmation
- `sig_253250d7018f578f` SOFI long — demoted
- `sig_9dc36c54d55a0086` BX long — demoted
- `sig_09bad19d360ff096` VRT long — demoted
- `sig_3d345d945a18dbcd` ANET long — demoted
- `sig_f785c9ef5c298333` NET long — demoted
- `sig_5376804e579d7e06` QQQ long — demoted
- `sig_2b9d7700cd7c438d` SPY long — demoted
- `sig_d00113e2caed5a52` VRTX short — market_context_conflict, sector_confirmation_conflict, last_30m_requires_trend_continuation, liquidity_rvol_below_min, catalyst_none_and_not_exceptional_technical
- `sig_b89043adb7fa53e6` XLK long — demoted
- `sig_aedada02cfa94c43` ORCL long — demoted
- `sig_4d9bb837a943b3c7` HOOD long — demoted
- `sig_1bff3a9056d075e6` ETN long — demoted
- `sig_d758b9ef97435bfa` HUT long — demoted
- `sig_12eafd1b51d6ee56` AMGN short — demoted
- `sig_e741dc302c0d0e0b` CRWD long — demoted
- `sig_eb34561493eae9a8` SMH long — demoted
- `sig_274c5334ac31f856` AMD long — demoted
- `sig_1db07db76e74d54c` ASML long — demoted
- `sig_b721922bd791067d` SMCI long — demoted
- `sig_579bff163a8355b7` CLSK long — demoted
- `sig_a621af55d62577e7` GOOGL long — demoted
- `sig_85fb0f95a1e14dc3` NFLX long — demoted
- `sig_705bf84ead762870` PLTR long — demoted
- `sig_79f93c4b20c671ae` BIIB long — demoted

## Post-trade diagnostics + cohort context
### Stocks-intraday post-trade diagnostics (last 14d, paper R — not legacy final_r)

**Evidence quality (Model F):** forward_postfreeze n=122 (ΣR=-5.55) — only bucket usable as proof of edge; backfill_pretrained n=0 — in-sample data that chose Model F's own thresholds, hypothesis only; unclassified n=0.

**By failure reason** (losses+expired only, worst R first):
- `weak_or_stale_catalyst`: n=16, ΣR=-12.87
- `no_gate_context`: n=27, ΣR=-3.00
- `spread_slippage_cost`: n=1, ΣR=-1.00
- `no_volume_followthrough`: n=39, ΣR=-0.31

**PnL(R) by session_phase:**
- `morning`: n=62, ΣR=-5.55
- `afternoon`: n=14, ΣR=-1.00
- `unknown`: n=46, ΣR=+1.00

**PnL(R) by catalyst_quality:**
- `none`: n=76, ΣR=-6.55
- `unknown`: n=46, ΣR=+1.00

**PnL(R) by market_context_status:**
- `ok`: n=76, ΣR=-6.55
- `unknown`: n=46, ΣR=+1.00

**PnL(R) by sector_confirmation_status:**
- `confirmed`: n=63, ΣR=-8.51
- `weak`: n=1, ΣR=-1.00
- `unknown`: n=46, ΣR=+1.00
- `provisional`: n=12, ΣR=+2.96

**Top avoidable loss buckets:** `weak_or_stale_catalyst` (-12.87R over 16), `no_gate_context` (-3.00R over 27), `spread_slippage_cost` (-1.00R over 1)

## Required output (structured JSON per candidate)
`{signal_id, decision, confidence, reasons, risks, catalyst_assessment, market_assessment, sector_assessment, chase_risk, stale_data_risk}` — advisory only; nothing is executed.