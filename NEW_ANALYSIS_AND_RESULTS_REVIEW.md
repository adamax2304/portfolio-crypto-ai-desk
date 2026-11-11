# New Analysis and Results Review

**Cycle window:** 2026-05-26 ~12:36 → 2026-05-27 ~early UTC
**Latest reports:** US session covered + ~60 minutes of post-session monitoring.

---

## 1. Monitor completion status

| Monitor | Task ID | Status | Ticks | Errors | Telegram |
|---------|---------|--------|-------|--------|----------|
| Crypto watchlist | `buqz5nkmv` | ✅ completed (`iterations limit reached; exiting`) | 6/6 | 0 | 0 promotions to A/B → 0 alerts |
| Stocks monitor session | `bg4ohjm2m` | ✅ completed (`finished after 4 tick(s)`) | 4 ticks | 0 | **57 alerts sent** (new=1, upgrades=56), 0 failed |

Crypto monitor produced no tier promotions (every symbol stayed C or dropped to rejected). Stocks monitor fired **57 Telegram alerts** during the US session because scores and entry zones moved enough to trip the material-improvement gates (Δscore ≥ 5 or entry/invalidation Δ ≥ 0.5 %).

---

## 2. Reports generated this cycle

| Mode | Path | Saved at (UTC) |
|------|------|----------------|
| Crypto scalp | `data/reports/scalp/2026-05-26_15-58_scalp_report.md` | 15:58 |
| Crypto intraday | `data/reports/intraday/2026-05-26_15-56_intraday_report.md` | 15:56 |
| Stocks intraday (initial) | `data/reports/stocks/intraday/2026-05-26_15-53_stocks_intraday_report.md` | 15:53 |
| Stocks intraday (latest mid-session refresh by monitor) | `data/reports/stocks/intraday/2026-05-26_17-05_stocks_intraday_report.md` | 17:05 |

Each `*-report` command refreshed the corresponding LLM packet automatically (QA Fix #1 verified by `LLM packet refreshed:` lines in stdout).

---

## 3. LLM packet freshness

| Packet | Latest refresh source |
|--------|------------------------|
| `data/processed/llm_analysis_packet.md` | scalp report (15:58 UTC) — last crypto run owns the file |
| `data/processed/llm_stocks_packet.md` | latest stocks-intraday refresh (17:05 UTC, by monitor) |
| `data/processed/context_for_llm.md` | latest crypto run (15:58 UTC) |

All packets fresh, all stamped with `Source report:` header. No stale packet in flight.

---

## 4. Final tracking results

```
python -m src.cli track-signals --all
Tracking pass complete: checked=238 updated=79 tp_hits=37 stopped=0
                       expired=4 not_triggered=32 ambiguous=0 no_ohlcv=0
                       errors=0
```

**Sequence across the cycle:**
| Pass | checked | updated | tp_hits | stopped | expired |
|------|---------|---------|---------|---------|---------|
| Pre-reports | 241 | 0 | 1 (carry-over) | 0 | 0 |
| Post-reports (before monitors) | 250 | **104** | **36** | 19 | 1 |
| Final (after monitors) | 238 | **79** | **37** | 0 | 4 |

Across the cycle the tracker recorded **79+ new transitions**, the bulk of which are TP1 hits on stocks longs that entered during the US session. `no_ohlcv=0` and `errors=0` throughout — the cross-asset path resolution works.

---

## 5. Active signals snapshot

### Crypto (1 active)
| Symbol | Tier | Mode | Direction | Score | Status |
|--------|------|------|-----------|-------|--------|
| TAO/USDT | B | intraday | long | 66.3 | **tp1_hit** ✅ (booked TP1, still open) |

7 of the 8 historical crypto signals have closed terminal — SAGA/NIL/EDEN got stopped or expired during the cycle. TAO is the only survivor.

### Stocks (multiple active, top of A-tier)
| Symbol | Tier | Mode | Score | Status |
|--------|------|------|-------|--------|
| AAPL | A | intraday | 84.0 | waiting/triggered (multiple rows) |
| LLY | A | intraday | ~80 | triggered |
| AMD | B | intraday | ~78 | triggered |
| XLK / SMCI / SMH / UNH / TSLA | B | intraday | 67–75 | triggered (most) |

**Note:** AAPL appears 4× in active because every report run registered a fresh row. The dedup view (Section 6) shows only **5 unique A-tier setups** in total this week.

Score on AAPL dropped from **88.64 → 84.0** between report runs — softer setup but still A-tier on the floor.

---

## 6. Signal statistics

### 6a. Raw stats (`signal-stats` output)

| Class | Sample | Confidence | Triggered | Wins | Losses | PF | avgR | totalR |
|-------|--------|-----------|-----------|------|--------|----|------|--------|
| Crypto | 8 | anecdotal | 7 | 1 | 4 | 0.5 | −0.29R | **−2.0R** |
| Stocks | 288 | "reliable" (mostly duplicates) | 99 | 36 | 19 | 2.79 | +0.34R | **+34.0R** |

The "reliable" confidence label on stocks is misleading — it is the by-product of registering the same 8 setups across 30+ report runs. See deduped view below.

### 6b. Deduped stats (one canonical signal per unique setup)

Dedup key: `(symbol, asset_class, mode, direction, tier, day-of-created_at)` + entry mid Δ < 0.5 % + invalidation Δ < 0.5 %. Canonical = earliest signal; replaced only on tier upgrade, score ≥ +5, or entry/invalidation Δ ≥ 0.5 %.

#### Stocks
| Bucket | Raw n | **Dedup n** | Triggered (dedup) | Wins | Losses | PF | avgR | totalR | TP1 hit rate | Stop rate |
|--------|------:|------------:|------------------:|-----:|-------:|---:|-----:|-------:|--------------|-----------|
| All stocks | 288 | **35** | 14 | 2 | 3 | 0.67 | −0.20R | **−1.0R** | 14.3 % | 35.7 % |
| Stocks A/B | 186 | **21** | 7 | 2 | 0 | ∞ | +1.00R | **+2.0R** | 28.6 % | 28.6 % |
| Stocks A only | 42 | **5** | 3 | 2 | 0 | ∞ | +1.00R | **+2.0R** | 66.7 % | 0 % |
| Stocks B only | 144 | **16** | 4 | 0 | 0 | n/a | n/a | 0R | 0 % | 50 % |
| Stocks C only | 102 | **14** | 7 | 0 | 3 | 0.0 | −1.00R | **−3.0R** | 0 % | 42.9 % |
| Stocks intraday A/B | 186 | **21** | 7 | 2 | 0 | ∞ | +1.00R | **+2.0R** | 28.6 % | 28.6 % |

**Dedup inflation factor:** raw 288 / dedup 35 = **8.2×**. Every "setup" was registered an average of ~8 times across report runs.

#### Crypto
| Bucket | Raw n | Dedup n | Triggered | Wins | Losses | PF | avgR | totalR | TP1 hit rate | Stop rate |
|--------|------:|--------:|----------:|-----:|-------:|---:|-----:|-------:|--------------|-----------|
| All crypto | 8 | 8 | 7 | 1 | 4 | 0.5 | −0.40R | **−2.0R** | 14.3 % | 85.7 % |
| Crypto A/B | 8 | 8 | 7 | 1 | 4 | 0.5 | −0.40R | −2.0R | 14.3 % | 85.7 % |
| Crypto A only | 0 | 0 | — | — | — | — | — | — | — | — |
| Crypto B only | 8 | 8 | 7 | 1 | 4 | 0.5 | −0.40R | −2.0R | 14.3 % | 85.7 % |
| Crypto scalp A/B | 3 | 3 | 3 | 0 | 1 | 0.0 | −1.00R | −1.0R | 0 % | 33 % |
| Crypto intraday A/B | 5 | 5 | 4 | 1 | 3 | 0.67 | −0.25R | −1.0R | 25 % | 125 %† |

†`stop_rate > 100%` in crypto intraday is an artefact: one stopped signal had `entry_triggered=0` (the tracker recorded a stop without an entry-trigger transition). Result is honest, the ratio is just badly defined for that edge case.

**Crypto did NOT inflate** — each crypto setup was unique. Dedup count = raw count.

#### Sample-size verdict
- **Stocks A-tier dedup:** 5 unique setups (1 day) → still **anecdotal** despite the impressive raw numbers.
- **Stocks B-tier dedup:** 16 unique setups → weak — still in the "wait for more samples" zone.
- **Stocks C-tier:** 14 unique setups, 0/3 wins → **C-tier ETF longs lost money** (QQQ/IWM/SPY/DIA chopped). Healthy that C-tier was kept off Telegram.
- **Crypto:** 8 anecdotal — far below moderate-confidence threshold.

---

## 7. Telegram alerts summary

| Metric | Crypto | Stocks |
|--------|--------|--------|
| Alerts sent this cycle | 0 | **57** (1 new, 56 material-improvement updates) |
| Duplicates skipped | several cooldown skips | **533** |
| Failed alerts | 0 | 0 |
| Symbols alerted | none | AAPL, LLY, AMD, XLK, SMCI, SMH, UNH, TSLA (multiple updates each as scores and entries shifted during US session) |
| C-tier alerted incorrectly | 0 | **0** (gate held) |

The `upgrades=56` count means the same setup was alerted multiple times because the score / entry / invalidation crossed the material-improvement threshold within the 4-tick window. This is **the intended behaviour** — not spam — but a small refinement could be useful: rate-limit "tier_upgrade" / "score_improvement" to once per N minutes per symbol. Logged as a Should-fix.

---

## 8. What changed since the previous run

### Crypto scalp
- Regime: **transition_up BTC / range ETH** (unchanged); breadth above EMA20 ticked **higher** (~72 % → ~similar) — wider tape participation.
- Strongest momentum: TAO/USDT (4.17x volume), WLD, ERA — but all over-extended → rejected from active.
- No new A/B; INJ/USDT, TAO/USDT, RENDER/USDT continue to dominate C-tier watchlist.

### Crypto intraday
- Same regime read. BTC stayed within transition_up.
- Previous B-tier signals (SAGA, NIL) **closed terminal** (stops/expiry). Only TAO/USDT B-tier `tp1_hit` remains active.
- 4 expirations this cycle indicate validity windows did their job.

### Stocks intraday
- Regime unchanged: **bullish**, VIX low, 100 % breadth above EMA20/EMA50.
- A-tier: AAPL **score dropped 88.64 → 84.0** during the session (still A). LLY stayed at 80.33.
- B-tier: AMD/XLK/SMCI/SMH/UNH/TSLA unchanged in tier; small score deltas triggered material-improvement alerts.
- **No new A/B name joined**; **no existing A/B was downgraded** from the A/B universe.
- C-tier got SLIMMER: previous run had 5 C-tier (QQQ/IWM/SPY/XLV/DIA), latest had 1 C-tier. Most ETFs dropped to rejected — reflecting that ETF longs are losing edge in the current tape (confirmed by C-tier dedup: 0/3 wins, totalR −3R).

---

## 9. Manual review checklist (A/B candidates worth chart-verifying now)

### AAPL A 84.0 (was 88.64)
- Entry: 308.0356 – 308.8800 (zone unchanged)
- Invalidation: 306.3468
- TP1: 311.4132 (R:R 1.0 — system flagged "below 1.5")
- RR: 1.0
- News/catalyst: 1 prior catalyst (test-source residue cleared per QA-2; the new pipeline confirms 0 fake news)
- Data confidence: high
- **Main risk:** earnings UNKNOWN (yfinance lookup pending) + score softening since open

### LLY A 80.33
- Entry: 1060.83 – 1065.65
- Invalidation: 1051.18
- TP1: 1080.12 (R:R ~1.5–1.8)
- News/catalyst: none verified
- Data confidence: high
- **Main risk:** pharma sector reversal; LLY is RS leader vs both index + sector

### AMD B 78.77
- Entry: 463.37 – 467.51
- Invalidation: 455.09
- TP1: 479.93 (R:R ~1.0)
- News/catalyst: none verified
- Data confidence: high
- **Main risk:** extended move; wait for retest into 463 zone

### Crypto TAO/USDT B (tp1_hit)
- Already booked TP1. Decide on partial or full close vs trail.
- Original invalidation 275.13; with TP1 booked, move stop to break-even or first 15m higher-low.

---

## 10. Final verdict

| Mode | Verdict | Why |
|------|---------|-----|
| Crypto scalp | **No trade / watchlist only** | Regime transition mixed, 0 A/B today, top movers all over-extended, recent 1/4 wins on B-tier |
| Crypto intraday | **Watchlist only** | TAO already in profit (manage existing); no new A/B; sample anecdotal and negative PF |
| Stocks intraday | **Tradeable — selectively** | LLY A clearest setup (RS leader vs both index + sector, clean R:R). AAPL A acceptable if entered near zone (avoid chasing after 84 score). AMD B requires retest. Skip C-tier ETFs (data confirms losses) |

---

## 11. Warnings

- **yfinance earnings calendar still UNKNOWN** for most individual stocks → every stocks A/B carries undated event risk.
- **Stocks signal registry inflation** — 8.2× dedup factor. Cosmetic (does not bias scoring) but inflates the "reliable" confidence label. Should be cleaned up.
- **Crypto Telegram cooldown** sometimes blocks legitimate re-alerts when score swings between ticks — acceptable in current design.
- **Disabled news sources** (MarketWatch, Yahoo Finance, Seeking Alpha RSS) — still off; stocks news layer remains thin.
- **`stop_rate > 100 %` artefact** in crypto_intraday_AB dedup — tracker recorded a stop on a signal without an `entry_triggered` outcome row. Cosmetic.

---

## 12. Safety confirmation

- ✅ No auto-trades
- ✅ No scoring changes
- ✅ No threshold changes
- ✅ No architecture changes
- ✅ No agent changes
- ✅ No alerts without invalidation (`no_inv_skipped=0`)
- ✅ No C-tier Telegram alerts
- ✅ Crypto/stocks isolation preserved
- ✅ No test_source news in any production report

---

## 13. Should we run another fresh analysis cycle now?

**Verdict: No — wait. Current signals are still active and need tracking.**

Reasoning:
1. **Stocks A/B universe is unchanged** (same 8 names). Scores moved within ±5 points — material-improvement alerts already fired during the just-completed session.
2. **TAO/USDT B-tier already booked TP1** — needs a *manual trade decision* (close TP2 / trail / scale out), not a new analysis.
3. **Crypto regime is still transition mixed** — selective only. Another report would not change that read.
4. **Sample-size discipline:** the deduped stats above show only **5 unique A-tier setups** and **21 A/B total**. Re-running the same report now adds more duplicates without adding decision information.
5. **US session closed** during the monitoring window — stocks data won't move until pre-market in ~10 hours. yfinance won't have new prints.

**Next useful action (when you choose):**
- A few hours from now (next US pre-market), run **stocks-intraday-report** and let the monitor pick up overnight changes.
- For crypto: run a fresh **intraday-report** at the next 4h boundary to see if the regime breaks out of "transition mixed".
- Continue running `track-signals --all` every ~30 min to keep outcome statistics live.

**Right now:** no new analysis. Watch TAO/USDT decision and the AAPL/LLY/AMD active entries. Let the data accumulate.
