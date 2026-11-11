# Final 12H Monitor Review — 2026-05-29

_Session: 2026-05-29T03:54:04.071151+03:00 → 2026-05-29T04:04:25.354111+03:00_

## 1. Cycles completed

| Cycle | Priority | US window | Started | Finished | ok | failed | TG |
|-------|----------|-----------|---------|----------|----|--------|----|
| 1 | regular | - | 03:54 | 03:54 | 6 | 0 | skipped |
| 2 | regular | - | 03:59 | 04:00 | 6 | 0 | skipped |

## 2-8. Final snapshots

### track-signals --all
```text
Tracking pass complete: checked=142 updated=6 tp_hits=88 stopped=0 expired=5 
not_triggered=1 ambiguous=0 no_ohlcv=0

```

### signal-stats crypto
```text
┌──────────────────────── signal-stats overall — week ────────────────────────┐
│ sample=13 (confidence=weak) | triggered=11 / not_triggered=2 | wins=1       │
│ losses=5 amb=0 | PF=0.2 avgR=-0.3636 totalR=-4.0                            │
└─────────────────────────────────────────────────────────────────────────────┘
                                    By tier                                    
┌──────┬────┬──────┬──────┬──────┬──────┬───────┬──────┬───────┬──────┬───────┐
│ lab… │ n  │ conf │ trig │ wins │ los… │ PF    │ avgR │ tota… │ cap… │ stopR │
├──────┼────┼──────┼──────┼──────┼──────┼───────┼──────┼───────┼──────┼───────┤
│ tie… │ 13 │ weak │ 11   │ 1    │ 5    │ 0.20… │ -0.… │ -4.0… │ 0.8… │ 0.54… │
└──────┴────┴──────┴──────┴──────┴──────┴───────┴──────┴───────┴──────┴───────┘
                                    By mode                                    
┌──────┬───┬───────┬──────┬──────┬──────┬───────┬──────┬───────┬──────┬───────┐
│ lab… │ n │ conf  │ trig │ wins │ los… │ PF    │ avgR │ tota… │ cap… │ stopR │
├──────┼───┼───────┼──────┼──────┼──────┼───────┼──────┼───────┼──────┼───────┤
│ mod… │ 8 │ anec… │ 7    │ 1    │ 1    │ 1.00… │ 0.0… │ 0.00… │ 0.8… │ 0.14… │
│ mod… │ 5 │ anec… │ 4    │ 0    │ 4    │ 0.00… │ -1.… │ -4.0… │ 0.8… │ 1.25… │
└──────┴───┴───────┴──────┴──────┴──────┴───────┴──────┴───────┴──────┴───────┘
                                 By direction                                  
┌──────┬───┬───────┬──────┬──────┬──────┬───────┬──────┬───────┬──────┬───────┐
│ lab… │ n │ conf  │ trig │ wins │ los… │ PF    │ avgR │ tota… │ cap… │ stopR │
├──────┼───┼───────┼──────┼──────┼──────┼───────┼──────┼───────┼──────┼───────┤
│ dir… │ 5 │ anec… │ 3    │ 1    │ 0    │ inf   │ 0.3… │ 1.00… │ 0.6… │ 0.33… │
│ dir… │ 8 │ anec… │ 8    │ 0    │ 5    │ 0.00… │ -0.… │ -5.0… │ 1.0… │ 0.62… │
└──────┴───┴───────┴──────┴──────┴──────┴───────┴──────┴───────┴──────┴───────┘
                           By exchange_confirmation                            

```

### signal-stats stocks
```text
┌──────────────────────── signal-stats overall — week ────────────────────────┐
│ sample=582 (confidence=reliable) | triggered=376 / not_triggered=184 |      │
│ wins=97 losses=62 amb=1 | PF=2.3651 avgR=0.2287 totalR=86.0                 │
└─────────────────────────────────────────────────────────────────────────────┘
                                    By tier                                    
┌──────┬─────┬──────┬──────┬──────┬──────┬──────┬──────┬───────┬──────┬───────┐
│ lab… │ n   │ conf │ trig │ wins │ los… │ PF   │ avgR │ tota… │ cap… │ stopR │
├──────┼─────┼──────┼──────┼──────┼──────┼──────┼──────┼───────┼──────┼───────┤
│ tie… │ 211 │ rel… │ 143  │ 17   │ 42   │ 0.4… │ -0.… │ -25.… │ 0.6… │ 0.30… │
│ tie… │ 303 │ rel… │ 184  │ 58   │ 10   │ 9.9… │ 0.5… │ 98.0… │ 0.6… │ 0.19… │
│ tie… │ 68  │ str… │ 49   │ 22   │ 10   │ 2.3… │ 0.2… │ 13.0… │ 0.7… │ 0.20… │
└──────┴─────┴──────┴──────┴──────┴──────┴──────┴──────┴───────┴──────┴───────┘
                                    By mode                                    
┌──────┬─────┬──────┬──────┬──────┬──────┬──────┬──────┬───────┬──────┬───────┐
│ lab… │ n   │ conf │ trig │ wins │ los… │ PF   │ avgR │ tota… │ cap… │ stopR │
├──────┼─────┼──────┼──────┼──────┼──────┼──────┼──────┼───────┼──────┼───────┤
│ mod… │ 581 │ rel… │ 375  │ 97   │ 62   │ 2.3… │ 0.2… │ 86.0… │ 0.6… │ 0.23… │
│ mod… │ 1   │ ane… │ 1    │ 0    │ 0    │      │ 0.0… │ 0.00… │ 1.0… │ 0.00… │
└──────┴─────┴──────┴──────┴──────┴──────┴──────┴──────┴───────┴──────┴───────┘
                                 By direction                                  
┌──────┬─────┬──────┬──────┬──────┬──────┬──────┬──────┬───────┬──────┬───────┐
│ lab… │ n   │ conf │ trig │ wins │ los… │ PF   │ avgR │ tota… │ cap… │ stopR │
├──────┼─────┼──────┼──────┼──────┼──────┼──────┼──────┼───────┼──────┼───────┤
│ dir… │ 581 │ rel… │ 375  │ 97   │ 61   │ 2.4… │ 0.2… │ 87.0… │ 0.6… │ 0.23… │
│ dir… │ 1   │ ane… │ 1    │ 0    │ 1    │ 0.0… │ -1.… │ -1.0… │ 1.0… │ 1.00… │

```

### dedup (raw vs deduped)
```text
{
  "totals": {
    "all_signals": 595,
    "outcome_rows": 9328,
    "unique_signals_with_outcomes": 595
  },
  "stocks_all": {
    "raw_count": 582,
    "dedup_count": 80,
    "raw_stats": {
      "sample": 582,
      "triggered": 376,
      "not_triggered": 184,
      "wins": 97,
      "losses": 62,
      "tp1_hits": 98,
      "tp2_hits": 42,
      "tp3_hits": 10,
      "stopped": 88,
      "winrate": 0.610062893081761,
      "tp1_hit_rate": 0.26063829787234044,
      "stop_rate": 0.23404255319148937,
      "avg_r": 0.5408805031446541,
      "total_r": 86.0,
      "profit_factor": 2.365079365079365
    },
    "dedup_stats": {
      "sample": 80,
      "triggered": 47,
      "not_triggered": 16,
      "wins": 11,
      "losses": 5,
      "tp1_hits": 11,
      "tp2_hits": 2,
      "tp3_hits": 1,
      "stopped": 8,
      "winrate": 0.6875,
      "tp1_hit_rate": 0.23404255319148937,
      "stop_rate": 0.1702127659574468,
      "avg_r": 0.5625,
      "total_r": 9.0,
      "profit_factor": 2.8
    }
  },
  "stocks_AB": {
    "raw_count": 371,
    "dedup_count": 47,
    "raw_stats": {
      "sample": 371,
      "triggered": 233,
      "not_triggered": 124,
      "wins": 80,
      "losses": 20,
      "tp1_hits": 81,
      "tp2_hits": 42,
      "tp3_hits": 10,
      "stopped": 45,
      "winrate": 0.8,
      "tp1_hit_rate": 0.34763948497854075,
      "stop_rate": 0.19313304721030042,
      "avg_r": 1.11,
      "total_r": 111.0,
      "profit_factor": 6.285714285714286
    },
    "
```

### alert-status
```text
                       Alert status — asset_class=stocks                       
┌───────────────┬───────────────┬────────────┬────────────────┬───────────────┐
│ ab_signals_t… │ alerts_sent_… │ ab_alerted │ ab_not_alerte… │ duplicate_al… │
├───────────────┼───────────────┼────────────┼────────────────┼───────────────┤
│ 371           │ 178           │ 178        │ 193            │ 0             │
└───────────────┴───────────────┴────────────┴────────────────┴───────────────┘

                       Alert status — asset_class=crypto                       
┌───────────────┬───────────────┬────────────┬────────────────┬───────────────┐
│ ab_signals_t… │ alerts_sent_… │ ab_alerted │ ab_not_alerte… │ duplicate_al… │
├───────────────┼───────────────┼────────────┼────────────────┼───────────────┤
│ 13            │ 0             │ 0          │ 13             │ 0             │
└───────────────┴───────────────┴────────────┴────────────────┴───────────────┘

```

## 9-13. Interpretation (manual)
- Best/worst setups, filter strictness, A/B meaningfulness: review the per-cycle summaries + signal-stats above. The scheduler does NOT auto-judge tradeability — that is a human read.
- Crypto filters: if crypto produced 0 A/B during a CLEAN uptrend for the whole session, investigate. During downtrend, 0 A/B is correct.
- Stocks raw stats are inflated by repeat registrations; trust the deduped view above.

## 14. Safety confirmation
- No auto-trades. No scoring/threshold/agent/architecture changes. Only existing CLI commands invoked. Telegram A/B-only via CLI gates.
