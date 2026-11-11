# Final Daily Default-Schedule Review — 2026-11-09

_Session: 2026-11-09T14:47:35.285942+02:00 → 2026-11-10T14:47:39.545704+02:00_

## 1. Cycles completed

| # | Mode | Long-horizon | Started | Finished | ok | failed | TG |
|---|------|--------------|---------|----------|----|--------|----|
| 1 | weekday | yes | 14:47 | 16:03 | 96 | 1 | sent |
| 2 | weekday | yes | 18:03 | 19:32 | 96 | 1 | sent |
| 3 | weekday | yes | 21:32 | 22:57 | 97 | 0 | sent |
| 4 | weekday | no | 00:57 | 01:34 | 79 | 0 | sent |
| 5 | weekday | yes | 03:34 | 04:46 | 97 | 0 | sent |
| 6 | weekday | yes | 06:46 | 07:53 | 97 | 0 | sent |
| 7 | weekday | yes | 09:53 | 10:59 | 97 | 0 | sent |
| 8 | weekday | yes | 12:59 | 14:17 | 96 | 1 | sent |

## 2. Final track-signals snapshot

```text
Tracking pass complete: checked=579 updated=0 tp_hits=336 stopped=0 expired=0 
not_triggered=226 ambiguous=0 no_ohlcv=0 lock_skips=0

```

## 3. Final signal-stats (crypto)

```text
┌─────────────── HEADLINE — Actionable Performance (A/B only) ────────────────┐
│ sample=21 (confidence=weak) | triggered=21 | wins=3 losses=13 |             │
│ winrate=0.142900 PF=0.125 avgR=-0.6562 totalR=-10.5                         │
└─────────────────────────────────────────────────────────────────────────────┘
┌──────────────────────── C-tier Watchlist / Research ────────────────────────┐
│ sample=0 | triggered=0 | wins=0 losses=0 | PF=None avgR=None totalR=0.0     │
│ (watchlist/research — not Telegram-actionable)                              │
└─────────────────────────────────────────────────────────────────────────────┘
┌─────────── all-tier diagnostic (A/B/C — NOT the headline) — week ───────────┐
│ sample=21 (confidence=weak) | triggered=21 / not_triggered=0 | wins=3       │
│ losses=13 amb=0 | PF=0.125 avgR=-0.6562 totalR=-10.5                        │
└─────────────────────────────────────────────────────────────────────────────┘
                                    By tier                                    
┌──────┬────┬──────┬──────┬──────┬──────┬───────┬──────┬───────┬──────┬───────┐
│ lab… │ n  │ conf │ trig │ wins │ los… │ PF    │ avgR │ tota… │ cap… │ stopR │
├──────┼────┼──────┼──────┼──────┼──────┼───────┼──────┼───────┼──────┼───────┤
│ tie… │ 21 │ weak │ 21   │ 3    │ 13   │ 0.12… │ -0.… │ -10.… │ 1.0… │ 0.71… │
└──────┴────┴──────┴──────┴──────┴──────┴───────┴──────┴───────┴──────┴───────┘
                                    By mode                                    
┌──────┬────┬──────┬──────┬──────┬──────┬───────┬──────┬───────┬──────┬───────┐
│ lab… │ n  │ conf │ trig │ wins │ los… │ PF    │ avgR │ tota… │ cap… │ stopR │
├──────┼────┼──────┼──────┼──────┼──────┼───────┼──────┼───────┼──────┼───────┤
│ mod… │ 21 │ weak │ 21   │ 3    │ 13   │ 0.12… │ -0.… │ -10.… │ 1.0… │ 0.71… │
└──────┴────┴──────┴──────┴──────┴──────┴───────┴──────┴───────┴──────┴───────┘
                                 By direction                                  
┌──────┬────┬──────┬──────┬──────┬──────┬───────┬──────┬───────┬──────┬───────┐
│ lab… │ n  │ conf │ trig │ wins │ los… │ PF    │ avgR │ tota… │ cap… │ stopR │
├──────┼────┼──────┼──────┼──────┼──────┼───────┼──────┼───────┼──────┼───────┤
│ dir… │ 4  │ ane… │ 4    │ 1    │ 1    │ 0.50… │ -0.… │ -0.5… │ 1.0… │ 0.25… │
│ dir… │ 17 │ weak │ 17   │ 2    │ 12   │ 0.09… │ -0.… │ -10.… │ 1.0… │ 0.82… │
└──────┴────┴──────┴──────┴──────┴──────┴───────┴──────┴───────┴──────┴───────┘
                    
```

## 4. Final signal-stats (stocks)

```text
┌─────────────── HEADLINE — Actionable Performance (A/B only) ────────────────┐
│ sample=69 (confidence=stronger) | triggered=43 | wins=7 losses=5 |          │
│ winrate=0.162800 PF=4.2323 avgR=0.4618 totalR=9.6969                        │
└─────────────────────────────────────────────────────────────────────────────┘
┌──────────────────────── C-tier Watchlist / Research ────────────────────────┐
│ sample=634 | triggered=140 | wins=27 losses=14 | PF=2.8333 avgR=0.1264      │
│ totalR=11.0  (watchlist/research — not Telegram-actionable)                 │
└─────────────────────────────────────────────────────────────────────────────┘
┌─────────── all-tier diagnostic (A/B/C — NOT the headline) — week ───────────┐
│ sample=703 (confidence=reliable) | triggered=183 / not_triggered=504 |      │
│ wins=34 losses=19 amb=2 | PF=3.2997 avgR=0.1916 totalR=20.6969              │
└─────────────────────────────────────────────────────────────────────────────┘
                                    By tier                                    
┌──────┬─────┬──────┬──────┬──────┬──────┬──────┬──────┬───────┬──────┬───────┐
│ lab… │ n   │ conf │ trig │ wins │ los… │ PF   │ avgR │ tota… │ cap… │ stopR │
├──────┼─────┼──────┼──────┼──────┼──────┼──────┼──────┼───────┼──────┼───────┤
│ tie… │ 634 │ rel… │ 140  │ 27   │ 14   │ 2.8… │ 0.1… │ 11.0… │ 0.2… │ 0.14… │
│ tie… │ 60  │ str… │ 40   │ 7    │ 5    │ 4.2… │ 0.5… │ 9.69… │ 0.6… │ 0.12… │
│ tie… │ 9   │ ane… │ 3    │ 0    │ 0    │      │ 0.0… │ 0.00… │ 0.3… │ 0.00… │
└──────┴─────┴──────┴──────┴──────┴──────┴──────┴──────┴───────┴──────┴───────┘
                                    By mode                                    
┌──────┬─────┬──────┬──────┬──────┬──────┬──────┬──────┬───────┬──────┬───────┐
│ lab… │ n   │ conf │ trig │ wins │ los… │ PF   │ avgR │ tota… │ cap… │ stopR │
├──────┼─────┼──────┼──────┼──────┼──────┼──────┼──────┼───────┼──────┼───────┤
│ mod… │ 703 │ rel… │ 183  │ 34   │ 19   │ 3.2… │ 0.1… │ 20.6… │ 0.2… │ 0.13… │
└──────┴─────┴──────┴──────┴──────┴──────┴──────┴──────┴───────┴──────┴───────┘
                                 By direction                                  
┌──────┬─────┬──────┬──────┬──────┬──────┬──────┬──────┬───────┬──────┬───────┐
│ lab… │ n   │ conf │ trig │ wins │ los… │ PF   │ avgR │ tota… │ cap… │ stopR │
├──────┼─────┼──────┼──────┼──────┼──────┼──────┼──────┼───────┼──────┼───────┤
│ dir… │ 246 │ rel… │ 56   │ 14   │ 4    │ 5.5… │ 0.3… │ 13.6… │ 0.2… │ 0.12… │
│ dir… │ 457 │ rel… 
```

## 5. Active signals — crypto

```text
            Armed Watch / active signals (40) — asset_class=crypto             
┌─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┐
│ si… │ sy… │ as… │ ti… │ mo… │ di… │ sc… │ st… │ en… │ en… │ in… │ ex… │ we… │
├─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┤
│ si… │ ZE… │ cr… │ B   │ in… │ sh… │ 68… │ tr… │ 1,… │ 1,… │ 1,… │ 20… │     │
│ si… │ ZE… │ cr… │ B   │ in… │ sh… │ 66… │ tp… │ 1,… │ 1,… │ 1,… │ 20… │     │
│ si… │ PU… │ cr… │ B   │ in… │ lo… │ 68… │ tp… │ 0.… │ 0.… │ 0.… │ 20… │     │
│ si… │ AD… │ cr… │ B   │ in… │ lo… │ 65… │ tp… │ 0.… │ 0.… │ 0.… │ 20… │     │
│ si… │ PU… │ cr… │ B   │ in… │ lo… │ 68… │ tp… │ 0.… │ 0.… │ 0.… │ 20… │     │
│ si… │ BR… │ cr… │ B   │ in… │ lo… │ 69… │ tp… │ 0.… │ 0.… │ 0.… │ 20… │     │
│ si… │ ST… │ cr… │ B   │ in… │ lo… │ 66… │ tp… │ 0.… │ 0.… │ 0.… │ 20… │ Y   │
│ si… │ LT… │ cr… │ B   │ in… │ lo… │ 68… │ tp… │ 53… │ 53… │ 52… │ 20… │ Y   │
│ si… │ UN… │ cr… │ B   │ in… │ lo… │ 65… │ tp… │ 6.… │ 6.… │ 6.… │ 20… │     │
│ si… │ ZK… │ cr… │ B   │ sc… │ lo… │ 69… │ tp… │ 0.… │ 0.… │ 0.… │ 20… │ Y   │
│ si… │ ON… │ cr… │ B   │ sc… │ lo… │ 67… │ tp… │ 0.… │ 0.… │ 0.… │ 20… │     │
│ si… │ VI… │ cr… │ B   │ sc… │ lo… │ 71… │ tp… │ 0.… │ 0.… │ 0.… │ 20… │     │
│ si… │ IN… │ cr… │ B   │ sc… │ lo… │ 68… │ tp… │ 5.… │ 5.… │ 5.… │ 20… │     │
│ si… │ VI… │ cr… │ B   │ sc… │ lo… │ 71… │ tp… │ 0.… │ 0.… │ 0.… │ 20… │     │
│ si… │ PE… │ cr… │ B   │ in… │ lo… │ 70… │ tp… │ 0.… │ 0.… │ 0.… │ 20… │     │
│ si… │ TA… │ cr… │ B   │ in… │ lo… │ 67… │ tp… │ 23… │ 23… │ 22… │ 20… │     │
│ si… │ IN… │ cr… │ B   │ sc… │ lo… │ 73… │ tp… │ 4.… │ 5.… │ 4.… │ 20… │     │
│ si… │ TU… │ cr… │ B   │ sc… │ lo… │ 68… │ tp… │ 0.… │ 0.… │ 0.… │ 20… │ Y   │
│ si… │ CO… │ cr… │ B   │ in… │ lo… │ 66… │ tp… │ 0.… │ 0.… │ 0.… │ 20… │ Y   │
│ si… │ XP… │ cr… │ B   │ sc… │ lo… │ 66… │ tp… │ 0.… │ 0.… │ 0.… │ 20… │     │
│ si… │ BI… │ cr… │ B   │ in… │ sh… │ 65… │ tp… │ 0.… │ 0.… │ 0.… │ 20… │     │
│ si… │ TS… │ cr… │ B   │ sc… │ lo… │ 68… │ tp… │ 0.… │ 0.… │ 0.… │ 20… │ Y   │
│ si… │ BI… │ cr… │ B   │ sc… │ lo… │ 68… │ tp… │ 0.… │ 0.… │ 0.… │ 20… │ Y   │
│ si… │ ZB… │ cr… │ B   │ sc… │ lo… │ 66… │ tp… │ 0.… │ 0.… │ 0.… │ 20… │     │
│ si… │ TU… │ cr… │ B   │ sc… │ lo… │ 74… │ tp… │ 0.… │ 0.… │ 0.… │ 20… │     │
│ si… │ KI… │ cr… │ B   │ in… │ lo… │ 65… │ tp… │ 0.… │ 0.… │ 0.… │ 20… │     │
│ si… │ HF… │ cr… │ B   │ sc… │ lo… │ 69… │ tp… │ 0.… │ 0.… │ 0.… │ 20… │     │
│ si… │ SY… │ cr… │ 
```

## 6. Active signals — stocks

```text
            Armed Watch / active signals (40) — asset_class=stocks             
┌─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┐
│ si… │ sy… │ as… │ ti… │ mo… │ di… │ sc… │ st… │ en… │ en… │ in… │ ex… │ we… │
├─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┤
│ si… │ CO… │ st… │ C   │ in… │ lo… │ 92… │ wa… │ 1,… │ 1,… │ 1,… │ 20… │     │
│ si… │ UB… │ st… │ C   │ in… │ lo… │ 92… │ wa… │ 70… │ 71… │ 70… │ 20… │     │
│ si… │ LLY │ st… │ C   │ in… │ lo… │ 90… │ wa… │ 1,… │ 1,… │ 1,… │ 20… │     │
│ si… │ DIS │ st… │ C   │ in… │ lo… │ 88… │ wa… │ 11… │ 11… │ 11… │ 20… │     │
│ si… │ GE  │ st… │ C   │ in… │ lo… │ 87… │ wa… │ 33… │ 33… │ 33… │ 20… │     │
│ si… │ XLI │ st… │ C   │ in… │ lo… │ 86… │ wa… │ 16… │ 16… │ 16… │ 20… │     │
│ si… │ RI… │ st… │ C   │ in… │ lo… │ 84… │ wa… │ 17… │ 17… │ 17… │ 20… │     │
│ si… │ AA… │ st… │ C   │ in… │ lo… │ 77… │ wa… │ 34… │ 35… │ 34… │ 20… │     │
│ si… │ XLC │ st… │ C   │ in… │ lo… │ 73… │ wa… │ 10… │ 10… │ 10… │ 20… │     │
│ si… │ IBM │ st… │ C   │ in… │ sh… │ 90… │ wa… │ 24… │ 24… │ 24… │ 20… │     │
│ si… │ AXP │ st… │ C   │ in… │ sh… │ 67… │ wa… │ 32… │ 32… │ 32… │ 20… │     │
│ si… │ DE… │ st… │ C   │ in… │ sh… │ 74… │ wa… │ 34… │ 35… │ 35… │ 20… │     │
│ si… │ CO… │ st… │ C   │ in… │ sh… │ 68… │ wa… │ 13… │ 13… │ 13… │ 20… │     │
│ si… │ MS… │ st… │ C   │ in… │ sh… │ 67… │ wa… │ 12… │ 12… │ 12… │ 20… │     │
│ si… │ AD… │ st… │ C   │ in… │ sh… │ 70… │ wa… │ 23… │ 23… │ 23… │ 20… │     │
│ si… │ CR… │ st… │ C   │ in… │ sh… │ 57… │ wa… │ 67… │ 68… │ 68… │ 20… │     │
│ si… │ CO… │ st… │ C   │ in… │ lo… │ 92… │ tp… │ 1,… │ 1,… │ 1,… │ 20… │     │
│ si… │ BI… │ st… │ C   │ in… │ lo… │ 95… │ tp… │ 25… │ 25… │ 25… │ 20… │     │
│ si… │ NVO │ st… │ C   │ in… │ lo… │ 91… │ tp… │ 40… │ 40… │ 40… │ 20… │     │
│ si… │ DIS │ st… │ C   │ in… │ lo… │ 88… │ tp… │ 11… │ 11… │ 11… │ 20… │     │
│ si… │ MAR │ st… │ C   │ in… │ lo… │ 86… │ tp… │ 41… │ 41… │ 41… │ 20… │     │
│ si… │ UB… │ st… │ C   │ in… │ lo… │ 92… │ tp… │ 69… │ 69… │ 68… │ 20… │     │
│ si… │ RD… │ st… │ C   │ in… │ sh… │ 83… │ tr… │ 15… │ 15… │ 15… │ 20… │     │
│ si… │ RD… │ st… │ C   │ in… │ sh… │ 91… │ tr… │ 15… │ 15… │ 15… │ 20… │     │
│ si… │ DX… │ st… │ C   │ in… │ sh… │ 78… │ tr… │ 82… │ 83… │ 84… │ 20… │     │
│ si… │ GI… │ st… │ C   │ in… │ sh… │ 77… │ tp… │ 16… │ 16… │ 17… │ 20… │     │
│ si… │ SN… │ st… │ C   │ in… │ sh… │ 68… │ tp… │ 27… │ 27… │ 28… │ 20… │     │
│ si… │ AM… │ st… │ 
```

## 7. Untracked legacy detector

```text
## Untracked Legacy Crypto Alerts

_Detector: watchlist_alerts (crypto) without a matching proposed_signal within ±6h. Read-only._

- None. Every legacy crypto alert has a backing proposed_signal (or there were no crypto alerts).

```

## 8. Daily review (obsidian refresh)

```text
wrote 
C:\Users\adama\Documents\crypto-ai-desk\obsidian_vault\11_Trade_Journal\Daily_R
eviews\2026-11-10.md

```

## 9–17. Manual interpretation

- Best / worst signals: see per-cycle summaries + signal-stats above.
- Crypto vs stocks balance: was the weekday cycle producing distinct stocks A/B?
- Long-horizon hygiene: confirm swing/invest only ran once (`daily_*.done` marker).
- Filter strictness: 0 A/B is fine in downtrend / vol-compression / weekend; investigate only if 0 A/B during a clean trend day.
- Stocks legal/headline gate: PART 3 fix surfaces blocked signals in the report; verify any blocked A/B in the day's stocks report.
- What to improve next: typically nothing — this scheduler is workflow hygiene only.
- Final verdict: human read — the scheduler does not auto-judge tradeability.

## Safety

- No auto-trade.
- No scoring / threshold / agent / strategy changes.
- No Opus / LLM calls auto-invoked.
- Telegram A/B-only gates inherited from PART 1 (registration-before-alert) + PART 2 cooldown + PART 3 legal-block.
