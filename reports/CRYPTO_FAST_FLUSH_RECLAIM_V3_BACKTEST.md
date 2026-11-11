# Crypto Fast Flush Reclaim v3 - Historical Replay

- generated: `2026-10-06T00:09:30.244428+00:00`
- event period: `2026-09-21T20:10:00+00:00` to `2026-09-28T20:45:00+00:00`
- chronological split: `2026-09-27T22:10:00+00:00` (70% train / 30% untouched holdout)
- source events: `2680`
- missing: `{"base_bar": 1, "context": 2254, "geometry": 1456, "ohlcv": 0}`

Every result below is net of modeled fees and slippage. Simultaneous stop/target bars are stop-first. Correlated market cascades count once, using the strongest liquidation event.

## CONTROL_5M_RECLAIM

- selected on train only: `{"max_flush_atr": 3.25, "max_flush_pct": 2.5, "max_oi_drop_pct": 3.0, "max_spread_bps": 18.0, "max_stop_distance_pct": 0.015, "min_flush_atr": 1.5, "min_flush_pct": 0.75, "min_liq_percentile": 0.9, "min_oi_drop_pct": 0.25, "min_rvol": 1.05, "min_stop_distance_pct": 0.01, "sessions": ["europe", "us"]}`
- train: n=10, net=$45.46 (+4.55R), PF=5.053, win=90.0%, DD=$11.22, cost=$15.19
- holdout: n=0, net=$0.00 (+0.00R), PF=None, win=0.0%, DD=$0.00, cost=$0.00
- all cascade-adjusted: n=10, net=$45.46 (+4.55R), PF=5.053, win=90.0%, DD=$11.22, cost=$15.19
- all raw trades (diagnostic): n=14, net=$23.89 (+2.39R), PF=1.582, win=71.4%, DD=$34.12, cost=$20.89

## FAST_1M_ATR_TARGETS

- selected on train only: `{"max_flush_atr": 3.25, "max_flush_pct": 2.25, "max_oi_drop_pct": 3.0, "max_spread_bps": 18.0, "max_stop_distance_pct": 0.015, "min_flush_atr": 1.25, "min_flush_pct": 1.5, "min_liq_percentile": 0.9, "min_oi_drop_pct": 0.25, "min_rvol": 1.05, "min_stop_distance_pct": 0.005, "sessions": ["europe", "us"]}`
- train: n=9, net=$20.77 (+2.08R), PF=1.813, win=77.8%, DD=$13.02, cost=$19.20
- holdout: n=1, net=$9.40 (+0.94R), PF=None, win=100.0%, DD=$0.00, cost=$1.93
- all cascade-adjusted: n=10, net=$30.17 (+3.02R), PF=2.181, win=80.0%, DD=$13.02, cost=$21.13
- all raw trades (diagnostic): n=11, net=$33.98 (+3.40R), PF=2.331, win=81.8%, DD=$13.02, cost=$23.06

## FAST_1M_BALANCED

- selected on train only: `{"max_flush_atr": 3.25, "max_flush_pct": 2.5, "max_oi_drop_pct": 3.0, "max_spread_bps": 18.0, "max_stop_distance_pct": 0.015, "min_flush_atr": 1.5, "min_flush_pct": 0.75, "min_liq_percentile": 0.9, "min_oi_drop_pct": 0.5, "min_rvol": 1.05, "min_stop_distance_pct": 0.005, "sessions": ["europe", "us"]}`
- train: n=15, net=$52.76 (+5.28R), PF=3.008, win=86.7%, DD=$13.26, cost=$31.61
- holdout: n=5, net=$-37.65 (-3.77R), PF=0.17, win=20.0%, DD=$39.06, cost=$12.50
- all cascade-adjusted: n=20, net=$15.11 (+1.51R), PF=1.211, win=70.0%, DD=$46.63, cost=$44.12
- all raw trades (diagnostic): n=39, net=$-50.92 (-5.09R), PF=0.728, win=61.5%, DD=$112.13, cost=$90.98

## FAST_1M_EUROPE_MODERATE

- selected on train only: `{"max_flush_atr": 3.25, "max_flush_pct": 2.5, "max_oi_drop_pct": 3.0, "max_spread_bps": 18.0, "max_stop_distance_pct": 0.015, "min_flush_atr": 1.5, "min_flush_pct": 0.75, "min_liq_percentile": 0.9, "min_oi_drop_pct": 0.5, "min_rvol": 1.05, "min_stop_distance_pct": 0.005, "sessions": ["europe", "us"]}`
- train: n=15, net=$52.76 (+5.28R), PF=3.008, win=86.7%, DD=$13.26, cost=$31.61
- holdout: n=5, net=$-37.65 (-3.77R), PF=0.17, win=20.0%, DD=$39.06, cost=$12.50
- all cascade-adjusted: n=20, net=$15.11 (+1.51R), PF=1.211, win=70.0%, DD=$46.63, cost=$44.12
- all raw trades (diagnostic): n=39, net=$-50.92 (-5.09R), PF=0.728, win=61.5%, DD=$112.13, cost=$90.98

## FAST_1M_RECLAIM

- selected on train only: `{"max_flush_atr": 3.25, "max_flush_pct": 2.5, "max_oi_drop_pct": 3.0, "max_spread_bps": 18.0, "max_stop_distance_pct": 0.015, "min_flush_atr": 1.5, "min_flush_pct": 0.75, "min_liq_percentile": 0.9, "min_oi_drop_pct": 0.5, "min_rvol": 1.05, "min_stop_distance_pct": 0.005, "sessions": ["europe", "us"]}`
- train: n=15, net=$52.76 (+5.28R), PF=3.008, win=86.7%, DD=$13.26, cost=$31.61
- holdout: n=5, net=$-37.65 (-3.77R), PF=0.17, win=20.0%, DD=$39.06, cost=$12.50
- all cascade-adjusted: n=20, net=$15.11 (+1.51R), PF=1.211, win=70.0%, DD=$46.63, cost=$44.12
- all raw trades (diagnostic): n=39, net=$-50.92 (-5.09R), PF=0.728, win=61.5%, DD=$112.13, cost=$90.98

## HELD_1M_RECLAIM

- selected on train only: `{"max_flush_atr": 3.25, "max_flush_pct": 2.5, "max_oi_drop_pct": 3.0, "max_spread_bps": 18.0, "max_stop_distance_pct": 0.015, "min_flush_atr": 1.5, "min_flush_pct": 0.75, "min_liq_percentile": 0.9, "min_oi_drop_pct": 0.5, "min_rvol": 1.05, "min_stop_distance_pct": 0.005, "sessions": ["europe", "us"]}`
- train: n=12, net=$-11.37 (-1.14R), PF=0.811, win=58.3%, DD=$40.32, cost=$24.87
- holdout: n=2, net=$9.64 (+0.96R), PF=None, win=100.0%, DD=$0.00, cost=$3.61
- all cascade-adjusted: n=14, net=$-1.73 (-0.17R), PF=0.971, win=64.3%, DD=$40.32, cost=$28.47
- all raw trades (diagnostic): n=22, net=$-24.52 (-2.45R), PF=0.764, win=54.5%, DD=$58.43, cost=$42.65

## MEDIUM_DEEP_R_CONTROL

- selected on train only: `{"max_flush_atr": 3.25, "max_flush_pct": 2.5, "max_oi_drop_pct": 3.0, "max_spread_bps": 18.0, "max_stop_distance_pct": 0.015, "min_flush_atr": 1.5, "min_flush_pct": 0.75, "min_liq_percentile": 0.9, "min_oi_drop_pct": 0.5, "min_rvol": 1.05, "min_stop_distance_pct": 0.005, "sessions": ["europe", "us"]}`
- train: n=15, net=$52.76 (+5.28R), PF=3.008, win=86.7%, DD=$13.26, cost=$31.61
- holdout: n=5, net=$-37.65 (-3.77R), PF=0.17, win=20.0%, DD=$39.06, cost=$12.50
- all cascade-adjusted: n=20, net=$15.11 (+1.51R), PF=1.211, win=70.0%, DD=$46.63, cost=$44.12
- all raw trades (diagnostic): n=39, net=$-50.92 (-5.09R), PF=0.728, win=61.5%, DD=$112.13, cost=$90.98

## MEDIUM_DEEP_R_EXTENDED

- selected on train only: `{"max_flush_atr": 3.25, "max_flush_pct": 2.25, "max_oi_drop_pct": 3.0, "max_spread_bps": 18.0, "max_stop_distance_pct": 0.015, "min_flush_atr": 1.25, "min_flush_pct": 1.5, "min_liq_percentile": 0.9, "min_oi_drop_pct": 0.25, "min_rvol": 1.05, "min_stop_distance_pct": 0.005, "sessions": ["europe", "us"]}`
- train: n=9, net=$43.39 (+4.34R), PF=4.334, win=88.9%, DD=$13.02, cost=$19.16
- holdout: n=1, net=$10.32 (+1.03R), PF=None, win=100.0%, DD=$0.00, cost=$1.93
- all cascade-adjusted: n=10, net=$53.71 (+5.37R), PF=5.126, win=90.0%, DD=$13.02, cost=$21.09
- all raw trades (diagnostic): n=11, net=$58.78 (+5.88R), PF=5.516, win=90.9%, DD=$13.02, cost=$23.03

## MEDIUM_DEEP_STRUCTURE_HYBRID

- selected on train only: `{"max_flush_atr": 3.25, "max_flush_pct": 2.25, "max_oi_drop_pct": 3.0, "max_spread_bps": 18.0, "max_stop_distance_pct": 0.015, "min_flush_atr": 1.25, "min_flush_pct": 1.5, "min_liq_percentile": 0.9, "min_oi_drop_pct": 0.25, "min_rvol": 1.05, "min_stop_distance_pct": 0.005, "sessions": ["europe", "us"]}`
- train: n=9, net=$44.53 (+4.45R), PF=4.421, win=88.9%, DD=$13.02, cost=$18.79
- holdout: n=1, net=$8.37 (+0.84R), PF=None, win=100.0%, DD=$0.00, cost=$1.93
- all cascade-adjusted: n=10, net=$52.89 (+5.29R), PF=5.064, win=90.0%, DD=$13.02, cost=$20.73
- all raw trades (diagnostic): n=11, net=$56.56 (+5.66R), PF=5.346, win=90.9%, DD=$13.02, cost=$22.66

## Verdict

No profile demonstrated a positive holdout edge. Keep all profiles in Paper and collect more evidence.

This is Router-style evidence, not a promotion decision: 35 days is short and the candidate archive is event-selected.
