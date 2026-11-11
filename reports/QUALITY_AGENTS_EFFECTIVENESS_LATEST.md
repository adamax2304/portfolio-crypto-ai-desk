# Quality Agents Effectiveness

Generated: `2026-11-11T21:11:36.196776+00:00` | lookback: `30d`

All agents are measured point-in-time. `recommended_action` is counterfactual; `applied_action` remains `ALLOW` while the system is in shadow mode.

## Runtime

- `event_risk`: n=765, errors=0 (0.0%), avg=0.526ms, max=30.05ms
- `execution_sanity`: n=64, errors=0 (0.0%), avg=0.425ms, max=16.076ms
- `market_regime`: n=765, errors=0 (0.0%), avg=4.19ms, max=280.033ms
- `news_entity`: n=765, errors=0 (0.0%), avg=175.862ms, max=12698.724ms

## Matched Outcomes

- `event_risk` / `PASS`: n=43, W/L=12/8, sum=+4.37R, PF=1.5463
- `execution_sanity` / `PASS`: n=43, W/L=12/8, sum=+4.37R, PF=1.5463
- `market_regime` / `INSUFFICIENT_DATA`: n=13, W/L=5/3, sum=+2.51R, PF=1.8365
- `market_regime` / `CAUTION`: n=9, W/L=2/0, sum=+2.03R, PF=inf
- `market_regime` / `SUPPORT`: n=21, W/L=5/5, sum=-0.17R, PF=0.9658
- `news_entity` / `INSUFFICIENT_DATA`: n=37, W/L=10/7, sum=+4.13R, PF=1.5894
- `news_entity` / `CAUTION`: n=6, W/L=2/1, sum=+0.24R, PF=1.2449

## Counterfactual

- Hard-block recommendations: n=0, saved losers=0, missed winners=0, net delta=+0.00R.
- Half-size recommendations: n=9, full-size sum=+2.03R, delta versus full size=-1.02R.

## Active Incidents

- None.

## OpenRouter Advisory Cache

- No cached LLM assessments yet.

## LLM Paper Experiments

- No experiment assignments yet.

## Post-Trade Diagnostics

- `paper` / `normal_loss`: n=29, sum=-29.00R, $-351.10
- `paper` / `late_entry`: n=24, sum=-8.02R, $-305.48
- `paper` / `normal_scratch`: n=187, sum=+0.00R, $-339.50
- `paper` / `normal_win`: n=52, sum=+31.23R, $+349.16

## Promotion Rule

No news, event, or regime agent may become an enforced live gate until matched closed outcomes show positive net delta after missed winners, acceptable false-block rate, and stable error/latency metrics. Execution sanity may only enforce objective invariants.
