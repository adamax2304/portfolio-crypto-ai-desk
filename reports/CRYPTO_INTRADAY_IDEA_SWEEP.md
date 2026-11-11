# Crypto Intraday Idea Sweep (read-model only)

- version: `crypto_intraday_preentry_v4`
- run_id: `crypto_intraday_preentry_v4:20261111T202530935100+0000:51b6f5052a4b27f0`
- config_hash: `51b6f5052a4b27f0`
- generated_at: `2026-11-11T20:25:30.935100+00:00`
- signals_sampled: **400**
- minimum resolved forward trades: **30**
- Source: crypto / intraday / new_logic_shadow / forward_since_activation / preentry_v2 / data_quality=ok.
- Asia/off rows are excluded by the existing production guard. No config, routing, live, final_r, or actionability writes.

## PULLBACK_LIMIT / current

Status: **INSUFFICIENT_FORWARD_SAMPLE**; resolved=14; skipped=65; unresolved=0; net=$-11.76; net R=0.2000; winrate=0.3571; PF=0.9139; size=FULL_SIZE_CONTROL
Execution diagnostics: entries=14; geometry changed=0; mean bars to entry=1.0; expired-entry skips=65; filter-excluded=0; feature-unavailable=0
Note: current zone

## PULLBACK_LIMIT / shallow

Status: **INSUFFICIENT_FORWARD_SAMPLE**; resolved=14; skipped=65; unresolved=0; net=$-11.76; net R=0.2000; winrate=0.3571; PF=0.9139; size=FULL_SIZE_CONTROL
Execution diagnostics: entries=14; geometry changed=79; mean bars to entry=1.0; expired-entry skips=65; filter-excluded=0; feature-unavailable=0
Note: shallow zone

## PULLBACK_LIMIT / deeper

Status: **INSUFFICIENT_FORWARD_SAMPLE**; resolved=14; skipped=65; unresolved=0; net=$-11.76; net R=0.2000; winrate=0.3571; PF=0.9139; size=FULL_SIZE_CONTROL
Execution diagnostics: entries=14; geometry changed=79; mean bars to entry=1.0; expired-entry skips=65; filter-excluded=0; feature-unavailable=0
Note: deeper zone

## PULLBACK_LIMIT / level_hold_1bar

Status: **INSUFFICIENT_FORWARD_SAMPLE**; resolved=9; skipped=70; unresolved=0; net=$-113.07; net R=-4.0000; winrate=0.2222; PF=0.1607; size=FULL_SIZE_CONTROL
Execution diagnostics: entries=9; geometry changed=0; mean bars to entry=3.33; expired-entry skips=0; filter-excluded=0; feature-unavailable=0
Note: one closed candle holds the pullback level, then a later retest fills

## PULLBACK_LIMIT / level_hold_v2

Status: **INSUFFICIENT_FORWARD_SAMPLE**; resolved=5; skipped=74; unresolved=0; net=$-82.33; net R=-3.0000; winrate=0.0; PF=0.0; size=FULL_SIZE_CONTROL
Execution diagnostics: entries=5; geometry changed=0; mean bars to entry=0.0; expired-entry skips=1; filter-excluded=0; feature-unavailable=0
Note: mid-zone reclaim with a quality close, then a retest within three bars

## PULLBACK_LIMIT / vwap_hold_1bar

Status: **INSUFFICIENT_FORWARD_SAMPLE**; resolved=8; skipped=71; unresolved=0; net=$-86.60; net R=-3.0000; winrate=0.25; PF=0.2; size=FULL_SIZE_CONTROL
Execution diagnostics: entries=8; geometry changed=0; mean bars to entry=3.75; expired-entry skips=0; filter-excluded=0; feature-unavailable=0
Note: one closed candle holds session VWAP, then a later retest fills

## PULLBACK_LIMIT / vwap_confirm_close

Status: **INSUFFICIENT_FORWARD_SAMPLE**; resolved=5; skipped=72; unresolved=2; net=$-64.54; net R=-2.2665; winrate=0.4; PF=0.1918; size=FULL_SIZE_CONTROL
Execution diagnostics: entries=7; geometry changed=0; mean bars to entry=0.0; expired-entry skips=0; filter-excluded=0; feature-unavailable=0
Note: enter at the close of the candle confirming session VWAP hold

## PULLBACK_LIMIT / level_hold_mid_zone_retest_2bar

Status: **INSUFFICIENT_FORWARD_SAMPLE**; resolved=5; skipped=74; unresolved=0; net=$-82.33; net R=-3.0000; winrate=0.0; PF=0.0; size=FULL_SIZE_CONTROL
Execution diagnostics: entries=5; geometry changed=0; mean bars to entry=0.0; expired-entry skips=1; filter-excluded=0; feature-unavailable=0
Note: close through the mid-zone with a strong body; retest within two bars

## PULLBACK_LIMIT / level_hold_far_edge_retest_2bar

Status: **INSUFFICIENT_FORWARD_SAMPLE**; resolved=3; skipped=76; unresolved=0; net=$-29.18; net R=-1.0000; winrate=0.0; PF=0.0; size=FULL_SIZE_CONTROL
Execution diagnostics: entries=3; geometry changed=0; mean bars to entry=0.0; expired-entry skips=1; filter-excluded=0; feature-unavailable=0
Note: close through the far zone edge with a strong body; retest within two bars

## PULLBACK_LIMIT / vwap_zone_slope_hold_retest_2bar

Status: **INSUFFICIENT_FORWARD_SAMPLE**; resolved=1; skipped=78; unresolved=0; net=$-25.91; net R=-1.0000; winrate=0.0; PF=0.0; size=FULL_SIZE_CONTROL
Execution diagnostics: entries=1; geometry changed=0; mean bars to entry=0.0; expired-entry skips=1; filter-excluded=0; feature-unavailable=0
Note: hold VWAP and the far zone edge with aligned VWAP slope; retest within two bars

## PULLBACK_LIMIT / level_hold_mid_zone_quality_retest_2bar

Status: **INSUFFICIENT_FORWARD_SAMPLE**; resolved=0; skipped=79; unresolved=0; net=$0.00; net R=0.0000; winrate=n/a; PF=n/a; size=FULL_SIZE_CONTROL
Execution diagnostics: entries=0; geometry changed=0; mean bars to entry=n/a; expired-entry skips=0; filter-excluded=0; feature-unavailable=0
Note: mid-zone hold plus frozen light market/derivatives quality; retest within two bars

## PULLBACK_LIMIT / vwap_zone_slope_quality_retest_2bar

Status: **INSUFFICIENT_FORWARD_SAMPLE**; resolved=0; skipped=79; unresolved=0; net=$0.00; net R=0.0000; winrate=n/a; PF=n/a; size=FULL_SIZE_CONTROL
Execution diagnostics: entries=0; geometry changed=0; mean bars to entry=n/a; expired-entry skips=0; filter-excluded=0; feature-unavailable=0
Note: VWAP/zone/slope hold plus frozen light market/derivatives quality; retest within two bars

## PULLBACK_LIMIT / risk_off_veto_shadow

Status: **AWAITING_POINT_IN_TIME_FEATURE_COVERAGE**; resolved=7; skipped=47; unresolved=0; net=$84.28; net R=3.7000; winrate=0.5714; PF=3.907; size=SHADOW_ONLY_COUNTERFACTUAL
Execution diagnostics: entries=7; geometry changed=0; mean bars to entry=0.29; expired-entry skips=47; filter-excluded=6; feature-unavailable=19
Note: Shadow counterfactual: omit only a frozen explicit BTC risk_off state.

## PULLBACK_LIMIT / oi_unknown_veto_shadow

Status: **AWAITING_POINT_IN_TIME_FEATURE_COVERAGE**; resolved=6; skipped=46; unresolved=0; net=$46.45; net R=2.2000; winrate=0.5; PF=1.8493; size=SHADOW_ONLY_COUNTERFACTUAL
Execution diagnostics: entries=6; geometry changed=0; mean bars to entry=1.67; expired-entry skips=46; filter-excluded=15; feature-unavailable=12
Note: Shadow counterfactual: omit only fresh derivatives snapshots with OI regime unknown.

## PULLBACK_LIMIT / high_atr_veto_shadow

Status: **AWAITING_POINT_IN_TIME_FEATURE_COVERAGE**; resolved=10; skipped=51; unresolved=0; net=$-9.18; net R=0.2000; winrate=0.3; PF=0.9165; size=SHADOW_ONLY_COUNTERFACTUAL
Execution diagnostics: entries=10; geometry changed=0; mean bars to entry=1.0; expired-entry skips=51; filter-excluded=13; feature-unavailable=5
Note: Shadow counterfactual: omit observed ATR(14) > 2.5%; waits for point-in-time feature coverage.

## PULLBACK_LIMIT / low_rvol_veto_shadow

Status: **AWAITING_POINT_IN_TIME_FEATURE_COVERAGE**; resolved=8; skipped=47; unresolved=0; net=$59.48; net R=2.7000; winrate=0.5; PF=2.0769; size=SHADOW_ONLY_COUNTERFACTUAL
Execution diagnostics: entries=8; geometry changed=0; mean bars to entry=1.25; expired-entry skips=47; filter-excluded=19; feature-unavailable=5
Note: Shadow counterfactual: omit observed RVOL(20) < 0.5; waits for point-in-time feature coverage.

## BREAKOUT_CONTINUATION / strong_confirmation_only

Status: **BLOCKED_STRONG_CONFIRMATION_EVIDENCE**; resolved=0; skipped=79; unresolved=0; net=$0.00; net R=0.0000; winrate=n/a; PF=n/a; size=HALF_SIZE
Execution diagnostics: entries=0; geometry changed=0; mean bars to entry=n/a; expired-entry skips=0; filter-excluded=0; feature-unavailable=0
Note: point-in-time strong confirmation

## BREAKOUT_CONTINUATION / breakout_15m_vwap_btc_quality_shadow

Status: **BLOCKED_STRONG_CONFIRMATION_EVIDENCE**; resolved=0; skipped=0; unresolved=0; net=$0.00; net R=0.0000; winrate=n/a; PF=n/a; size=PAPER_COUNTERFACTUAL_ONLY
Execution diagnostics: entries=0; geometry changed=0; mean bars to entry=n/a; expired-entry skips=0; filter-excluded=79; feature-unavailable=0
Note: Paper counterfactual: strong 15m breakout structure, VWAP-side hold and aligned BTC slope; waits for frozen feature coverage.

## MOMENTUM_TAKER_NOW / current_half_size

Status: **INSUFFICIENT_FORWARD_SAMPLE**; resolved=0; skipped=12; unresolved=0; net=$0.00; net R=0.0000; winrate=n/a; PF=n/a; size=HALF_SIZE
Execution diagnostics: entries=0; geometry changed=0; mean bars to entry=n/a; expired-entry skips=12; filter-excluded=0; feature-unavailable=0
Note: current entry, HALF_SIZE control

## LIMIT_THEN_TAKER_TIMEOUT / disabled

Status: **DISABLED_BY_TEST_PLAN**; resolved=0; skipped=0; unresolved=0; net=$0.00; net R=0.0000; winrate=n/a; PF=n/a; size=SHADOW_ONLY
Execution diagnostics: entries=0; geometry changed=0; mean bars to entry=n/a; expired-entry skips=0; filter-excluded=0; feature-unavailable=0
Note: excluded from all parameter tests; production policy unchanged

No variant is auto-promoted. A result becomes reviewable only after the resolved forward gate; operator sign-off remains required.