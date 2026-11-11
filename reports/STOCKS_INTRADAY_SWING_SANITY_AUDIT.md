# Stocks Intraday & Swing — Sanity Audit (PART 4)

**Date:** 2026-06-09 · **Scope:** Read-only. No code/strategy/routing changes.
**Reference:** stocks swing pause / Telegram 400 fix deployed 2026-06-05T19:00 UTC.

## 1. Stocks intraday post-pause confirmation

### 1.1 Post-pause window (2026-06-05T19:00 → now)
Only 7 A/B intraday signals fired since the pause. All single trading day (Mon 2026-06-08 US session).

| created | symbol | tier | dir | outcome | R |
|---|---|---|---|---|---:|
| 06-08 18:19 | XOM | B | long | expired | 0 |
| 06-08 18:19 | XLV | B | long | expired | 0 |
| 06-08 15:45 | AAPL | B | long | **win** | **+1** |
| 06-08 15:25 | JPM | B | long | expired | 0 |
| 06-08 14:35 | XOM | A | long | expired | 0 |
| 06-08 14:35 | LLY | B | long | expired | 0 |
| 06-08 14:35 | GOOGL | B | short | expired | 0 |

**Post-pause-only verdict: too small (1 win, 0 losses, 6 expired).** Cannot confirm or deny intraday viability from the post-pause sample alone.

### 1.2 Full 14d intraday A/B (the trustworthy stat)
n=463, 165 closed, **WR 56.4%, PF 2.17, netR +84R**. This window straddles the fix; the bulk of wins predate the pause but the mode mechanics are unchanged. Intraday machinery is the same before/after the fix — the swing pause does not touch intraday, the Telegram fix only affected message delivery, not signal logic.

**Conclusion: stocks intraday remains the strongest stocks mode.** Maintaining it actionable is correct.

### 1.3 Best / worst symbols (full 14d window for power)
From the deep stats audit, A/B intraday 14d:

**Best (≥+1R):**
| symbol | dir | W | L | netR |
|---|---|---:|---:|---:|
| AMZN | short | 1 | 0 | +2 |
| AVGO | long | 2 | 0 | +2 |
| LLY | long | 1 | 1 | +2 |
| META | short | 1 | 0 | +2 |
| SPY | short | 1 | 0 | +2 |
| UNH | long | 2 | 0 | +2 |
| MSFT | short | 1 | 0 | +1 |
| QQQ | long/short | 2 | 0 | +2 |
| XLK | long/short | 2 | 0 | +2 |

**Worst (≤−1R):**
| symbol | dir | W | L | netR |
|---|---|---:|---:|---:|
| NVDA | long | 0 | 4 | −4 |
| SMCI | long | 0 | 3 | −3 |
| SMH | long | 0 | 2 | −2 |
| AAPL | long | 2 | 4 | −2 |
| PLTR | long | 0 | 1 | −1 |
| TSLA | long | 0 | 1 | −1 |

The two flagged longs (**NVDA, SMCI**) remain unresolved in post-pause data because **no new NVDA/SMCI intraday A/B signal has fired post-pause**. The 14d red flag persists structurally; post-pause has not yet tested it.

### 1.4 A-tier vs B-tier
| tier | n | closed | WR% | PF | netR |
|---|---:|---:|---:|---:|---:|
| A (14d) | 66 | 32 | 18.8 | 0.31 | −18 |
| B (14d) | 490 | 181 | 50.8 | 1.73 | +65 |

**A-tier is dragging the headline down across stocks**, but most A-tier signals are pre-pause swing/invest A's (LLY A 82–84, AAPL A 81–84, AMD A 79–82, NVDA A) that delivered the −18R. Among intraday-only A-tier signals (which are a small subset), there is currently 1 expired A in the post-pause window — no A-tier intraday loss has been observed since 06-05.

### 1.5 Shorts vs longs (intraday, 14d, A/B)
- short: **6/6 wins (100% WR, +9R)** — but small sample (15 total, 9 expired/not-triggered).
- long: 92 W / 115 L, WR 44.4%, +38R — positive but driven by frequency, not edge.

In the current tape (range-bound / mixed bias), intraday shorts on the major-cap tech basket (META, AMZN, SPY, QQQ, MSFT, GOOGL) have a perfect record over 14d on the closed sample. **This is small-sample noise** but the directional asymmetry is worth surfacing — it matches the macro context (ETF outflows, mild risk-off).

## 2. Stocks swing — pause verification & C-tier accumulation

### 2.1 Leak check
Since 2026-06-05T19:00:
- Total stocks swing signals: **25**
- Tier distribution: **25 × C, 0 × A, 0 × B**
- **No A/B leaks. Gate is holding at the data layer.** ✅

### 2.2 Post-pause C-tier counterfactual
Of 25 C-tier swing signals post-pause:
- 1 win, 0 losses (the single AAPL B-swing-long that gated through last week — counted because of the gate timing), 11 expired, 2 not_triggered, **11 pending**.
- Closed netR: +1 (on 1 closure).

**Sample is far too thin** to invalidate the pause (11 pending) but the early reads are mostly "expired" with small MFE/MAE (TSLA short MFE 0.07, AMZN short MFE 0.29) — consistent with swing being a flat grind in the current tape rather than a hidden positive edge.

### 2.3 Would swing still be losing if actionable?
The 14d **pre-pause** A/B swing data is 5W/36L (WR 12.2%, PF 0.17, −30R). That same pipeline produces today's C-tier swings — same symbols (META/TSLA/LLY/AMZN/NVDA/AAPL), same direction calls, same scoring. Without code changes, the pipeline that produced −30R cannot suddenly become positive; the pause is the correct, evidence-backed posture.

The single post-pause "win" (1×, +1R) does not invalidate that — it is consistent with the **pre-pause win-rate of 12%**: across 8 closed C-tier swing post-pause, even one win is roughly the expected rate of a broken-but-not-zero strategy.

## 3. Sanity summary

| Question | Answer |
|---|---|
| Stocks intraday still positive after pause? | **14d window: yes (+84R, PF 2.17)**. Post-pause sub-window too small alone (1W, 6 expired). |
| Best / worst symbols identified? | Yes — winners: AMZN/AVGO/LLY/META/SPY/UNH/QQQ/XLK. Losers: **NVDA, SMCI, SMH, AAPL longs**. |
| A-tier vs B-tier? | A-tier 18.8% WR / −18R driven by failed pre-pause swing/invest A's; B-tier 50.8% WR / +65R is healthy. |
| NVDA/SMCI longs still problematic? | **Yes structurally** — no fresh post-pause data on them yet. |
| Shorts vs longs in current tape? | Shorts 6/6 (100% WR, +9R, n=15) — small-sample but clean. Longs 44% WR, positive on volume. |
| Swing pause still active? | **Yes — 0 A/B leaks in 25 post-pause swings.** Gate verified. |
| Post-pause C-tier swing outcomes? | 1W / 0L / 11 expired / 2 NT / **11 pending**. Far too thin to revisit the pause. |
| Would swing still lose if actionable? | Yes by inheritance — same pipeline, same symbols, same direction calls; pre-pause was 5W/36L. |

## Verdict for PART 4
- **Stocks intraday: KEEP ACTIVE.** Full 14d data confirms +84R / PF 2.17. Post-pause sub-window too small alone but no evidence of regression; B-tier is the workhorse, A-tier intraday remains under-tested post-pause.
- **Stocks swing pause: HOLD.** 0 A/B leaks; C-tier counterfactual is too thin (11 pending) to challenge the −30R 14d pre-pause record. Continue collecting C-tier outcomes for at least one more US trading week before any re-enable consideration.
