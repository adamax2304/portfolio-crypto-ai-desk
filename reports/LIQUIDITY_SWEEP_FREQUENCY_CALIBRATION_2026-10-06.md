# Liquidity Sweep Frequency Calibration — 2026-10-06

## Scope and safety

Read-only review of current Paper outcomes and historical replays for the six enabled crypto Fast Flush/Reclaim profiles and three enabled stock Liquidity Shock/Reclaim profiles. The stock FAST 1m profile is archived/disabled. No production strategy or Paper settings were changed, and no Live route was enabled.

The research replay now applies each profile's own stop/target geometry. Targeted regression tests: `25 passed` for the crypto and stock Paper strategy suites.

## Recent activity

The current local date is 2026-10-06, early morning before US regular trading hours. The latest stock outcomes cover 2026-10-05. No stock signal is expected before today's RTH session.

From Oct 2 through Oct 5:

- Stocks: Oct 2 had 2 distinct eligible events; Oct 3–4 were weekend; Oct 5 had 7 distinct eligible events, of which 2 were already closed when queried. These are event counts, not the sum of profile rows.
- Crypto: the six profile variants evaluated many of the same underlying events. Only 1 distinct event qualified on Oct 5; Oct 2–4 had none. The scanner was still writing observations at 2026-10-06 00:19 UTC, most recently rejected as `SESSION_NOT_ALLOWED`; this is evidence of an active scanner, not evidence of a valid entry being missed.

Across the complete forward period since Sep 29, deduplicated by underlying event ID, crypto produced 5 eligible/clean-closed events and stocks 18 eligible events, 9 of which had clean closes at query time. These totals are across profiles, not sums of their duplicated rows. The combined forward rate is already several distinct setups per week; daily frequency is naturally uneven.

## Per-profile results

Historical crypto numbers below use the exact current entry/exit profile on the available replay and are in R, net of modeled costs. These are tiny samples and not promotion evidence.

| Paper profile | Historical replay | Recent forward Paper snapshot | Decision |
|---|---:|---:|---|
| Crypto FAST 1m reclaim | 7 trades, +3.215R; all in train, no holdout | 4 clean closes, +1.038R, PF 7.22 | Keep current strict baseline; sample too small to loosen or promote |
| Crypto Europe moderate | 6 trades, +1.903R; train +2.533R, one holdout trade -0.630R | 0 closes; most recent candidates failed session/flush/confirmation/OI gates | Keep isolated Paper ID; do not lower liquidation or structure thresholds on this evidence |
| Crypto FAST ATR targets | 7 trades, +4.407R; no holdout | 2 closes, +0.153R, PF 1.915 | Keep as an exit-policy comparison, not an independent extra source of entries |
| Crypto medium-deep R control | 12 trades, +3.984R; only 2 holdout trades | One common entry cohort; forward result -1.232R | Continue Paper; evidence is insufficient |
| Crypto medium-deep R extended | 12 trades, +5.192R; only 2 holdout trades | Same entry cohort as control; forward result -1.232R | Continue Paper; do not infer edge from two holdout wins |
| Crypto medium-deep structural hybrid | 12 trades, +4.915R; only 2 holdout trades | Same entry cohort; one forward result +0.214R | Continue Paper; target-policy comparison only |
| Stocks HELD reclaim | 49 trades, +6.325R, PF 1.546; holdout 22 trades, -0.849R, PF 0.876 | 8 clean closes, +0.662R, PF 1.489 in the prior forward snapshot | Keep Paper; historical holdout is weak |
| Stocks HELD structural targets | 46 trades, +9.335R, PF 1.933; holdout 22 trades, +0.955R, PF 1.15 | 7 clean closes, +0.870R, PF 1.643 in the prior snapshot | Best stock variant so far, but still Paper; holdout margin is small |
| Stocks HELD wider stop 0.15 ATR | 49 trades, +6.165R, PF 1.538; holdout 22 trades, -1.035R, PF 0.847 | 1 clean close, +0.489R; remaining eligible cohort still maturing | Do not widen further; forward sample is immature |

Exit variants within the same entry cohort are paired experiments. They must not be added together when estimating the system's trade frequency.

## Frequency experiments

### Stock confirmation window

Replayed the same 91-symbol historical set from July 24 to October 5 with profile windows of 12, 18, and 24 minutes. Confirmation still required two green/progress bars; all market, news, liquidity, and risk filters were unchanged.

| Profile / window | Trades | Net R | PF | Holdout trades | Holdout net R / PF |
|---|---:|---:|---:|---:|---:|
| HELD baseline, 12m | 49 | +6.325 | 1.546 | 22 | -0.849 / 0.876 |
| HELD baseline, 18m | 65 | +2.957 | 1.157 | 27 | -0.837 / 0.898 |
| HELD baseline, 24m | 77 | +1.747 | 1.078 | 31 | -2.690 / 0.733 |
| Structural targets, 12m | 46 | +9.335 | 1.933 | 22 | +0.955 / 1.150 |
| Structural targets, 18m | 61 | +5.409 | 1.317 | 27 | +0.249 / 1.031 |
| Structural targets, 24m | 73 | +4.349 | 1.212 | 31 | -1.603 / 0.839 |
| Wider stop, 12m | 49 | +6.165 | 1.538 | 22 | -1.035 / 0.847 |
| Wider stop, 18m | 65 | +2.874 | 1.154 | 27 | -1.020 / 0.874 |
| Wider stop, 24m | 77 | +1.716 | 1.078 | 31 | -2.830 / 0.715 |

Longer windows reduce expiry rejections, but the added trades dilute total PF and do not improve holdout. **Keep the current 12-minute window.**

### Stock lunch session

Added 11:30–13:30 ET to the existing windows and replayed the two active entry cohorts over the same 91 symbols. The independent eligible counts and P&L were unchanged: HELD remained 49 events and structural targets 46. The raw `RTH_WINDOW_NOT_ALLOWED` rejection count fell from 17,329 to 5,159, but `FLUSH_TOO_SMALL` rose from 21,418 to 33,019. The added lunch candidates did not become valid entries. **Do not add the lunch window.**

### Crypto confirmation window

Cloned all six active profile policies with 12- and 16-bar confirmation windows. FAST strict, Europe, and ATR-target variants each gained at most one training-period trade and no additional holdout entry. Medium-deep entry cohorts were unchanged. **Keep current 8-bar windows.**

## Why frequency is uneven

- Stocks were not supposed to trade on Oct 3–4 (weekend), and Oct 6 RTH had not started at the time checked. Oct 5 did produce seven distinct eligible stock setups.
- Stock historical failures concentrate in the shock-size and session envelope, then confirmation expiry. Broadening time or waiting longer did not create a better holdout cohort.
- Crypto FAST is constrained by profile flush size, flush ATR, session, liquidation/OI quality, and closed-candle reclaim. The last recorded observation was a session rejection; this is not a dead scanner.
- Historical crypto event coverage is stale/incomplete: the liquidation candidate archive ends Sep 28, while 2,254 of 2,680 events lack required context. The replay is therefore not adequate to optimize current crypto entry filters. This is a data-coverage limitation, not a reason to loosen risk gates.
- Several Paper IDs intentionally share the same setup but use different targets/stops. Counting each profile as a separate signal exaggerates frequency.

## Latency check

The stored `latency_seconds` measures when the Paper strategy processed a confirmed candle relative to that candle's timestamp. It is **not** exchange order round-trip latency.

- Crypto FAST confirmations on Oct 5 were processed in about 1.5 seconds. The only stale FAST reclaim in this forward sample was TAO on Sep 29 and was rejected as `STALE_RECLAIM_ENTRY`; no stale rejection was found on Oct 2–5.
- Stock Paper rows on Oct 5: 21 profile rows, all marked clean, with median processing delay 5 seconds, p90 10.6 seconds, maximum 10.6 seconds. Oct 2's maximum was 20 seconds.
- There was a historical stock delay burst on Oct 1: 10 profile rows had median 290 seconds, p90 621 seconds, and only 4 were marked clean. Delayed rows clustered around Sep 29–Oct 1; this did not recur in the Oct 2 or Oct 5 samples.
- The latest stock Paper heartbeat, at Oct 5 19:59:55 UTC, was `OK` with a 5.36-second tick. It is expected not to advance outside US RTH.

The Paper sweep does 15-second checks during US market hours, but refreshes at most 12 candidate 1m symbols per pass. Selection is currently alphabetical. This is a potential fairness risk under a burst of more than 12 simultaneous candidates, but the recent delay data does not show it recurring. Do not raise the cap blindly: larger batch fetches could make the tick exceed its 15-second budget. Record refresh backlog/age and rotate or prioritize the stalest candidates if the issue reappears. Paper timing does not establish actual MEXC/Bybit order latency.

## Action

No setting change passed the frequency-and-quality check, so current Paper settings remain unchanged. Keep all current candidates isolated in Paper and compare only distinct entry events. The next useful improvement is complete, append-only historical capture of crypto liquidation/context data; after enough clean forward observations, retest one threshold at a time against an untouched time split. Preserve the existing governance gates (`min_clean_closed: 30`, `min_forward_days: 28/30`, and PF `>= 1.20`) before considering any promotion.
