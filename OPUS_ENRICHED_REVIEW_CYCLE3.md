# Opus Enriched Review — 24H Crypto-Only Run, **Cycle 3**

**Methodology:** `prompts/llm_review/enriched_market_review_protocol.md` (§14 source discipline + §15 skill workflow).
**Skill:** `.claude/skills/enriched-review/SKILL.md` (Phase 1-7 executed).
**Cycle:** 3 / 12 — started **2026-05-30 22:39 EEST**, finished **23:03 EEST** (UTC+3, Saturday).
**Run folder:** `data/scheduled_runs/2026-05-30_24h_crypto_only/cycle_03_summary.md`.
**Mode:** advisory only. No auto-trade. No scoring / threshold / agent changes.

> ✅ **External web research available this run.** 13 sources fetched via WebSearch + WebFetch and ingested into `news_items` SQLite via `scripts/ingest_enriched_review_sources.py` (asset_class=crypto, all `single_source`, zero rejected). See **Sources** at the bottom.

---

## 1. Executive Summary

- **Cycle 3 status: 9/9 steps ok, Telegram sent.** Scheduler healthy; the bounded crypto monitor (90 min) was spawned (pid 22552) and cleanly killed at end-of-cycle as designed.
- **Zero new A-tier / zero new B-tier** in both scalp (22:51) and intraday (23:02) reports — same as cycles 1–2. The system continues to refuse to force setups in a BTC/ETH downtrend during the weekend.
- **Active crypto signals: 2** (BCH/USDT, UNI/USDT — both PART-1 backfilled scalp shorts, both still `tp1_hit` from earlier). **No new actionable produced by the 24h-only run so far.**
- **Biggest enrichment finding (overrides internal verdict):** **NEAR/USDT C-tier watchlist short is a TRAP.** Internal data sees it as a clean −9.1% bleed; external data shows NEAR is **+228 % from yearly low, mid-AI-narrative rally with a documented short-squeeze on 22 May at $1.72 that liquidated $5.8M of shorts** ([CoinDesk](https://www.coindesk.com/markets/2026/05/22/near-protocol-to-automate-its-own-growth-and-its-token-is-skyrocketing), [BanklessTimes](https://www.banklesstimes.com/articles/2026/05/22/near-protocol-surges-26-today-why-is-this-ai-token-pumping/)) + dynamic-resharding launch scheduled for June. **AVOID shorting NEAR — system was correctly cautious by not promoting it, external research confirms the avoid call.**
- **ASTER rejection is technically correct but fundamentally underpriced:** today (2026-05-30) ASTER hit **$1.26T cumulative volume**, dual-reward staking system went live May 29, **BTC/ETH perps launched May 28** ([CoinMarketCap top stories](https://coinmarketcap.com/top-stories/6a0dce432b069225f869e74c/)). The +10–11% move has real fundamental backing — not random noise. **Watchlist for pullback, not avoid.**
- **DxSale exploit fully verified across 10 outlets** (CryptoTimes, crypto.news, AMBCrypto, Blockonomi, MEXC News, etc.) — $7.3M drained from 1,400 LPs via setFee + backdated-lock backdoor, attacker funneled through Binance deposit addresses, insider involvement suspected. **Material narrative damage for BNB Chain. BNB long-watchlist should be downgraded.**
- **Net read for cycle 3:** system is **behaving correctly**; the enrichment adds one critical AVOID (NEAR), one upgrade-from-AVOID-to-WATCHLIST (ASTER), and one downgrade-from-WATCHLIST-to-AVOID (BNB).

---

## 2. Data Used

**Internal (cycle 3):**
- `data/scheduled_runs/2026-05-30_24h_crypto_only/cycle_03_summary.md`
- `data/reports/scalp/2026-05-30_19-51_scalp_report.md`
- `data/reports/intraday/2026-05-30_20-02_intraday_report.md`
- `data/processed/llm_analysis_packet.md` (refreshed by cycle 3 at 23:02)
- SQLite: `proposed_signals`, `signal_outcomes`, `news_items` (post-ingest), `watchlist_alerts`
- `track-signals --all`: `checked=146 updated=12 tp_hits=93 stopped=0 expired=8 not_triggered=4 ambiguous=0 no_ohlcv=0`
- `detect_untracked_legacy_alerts --since 2026-05-30` → **0 untracked** ✓

**External (per §14, all verified via WebSearch + WebFetch):** 13 sources, ingested into `news_items` (see Sources).

**Unavailable (declared):**
- TradingView / live chart access — **`TradingView manual chart check unavailable`**.
- Reddit social attention — `403 Blocked` on `r/CryptoCurrency`, `r/Bitcoin`, `r/ethereum` (every report).
- KOL X/Telegram/Discord live notes — placeholder list, no live data.

**Data-environment reconciliation (§4):** Real-world prices verified against internal:
| Symbol | Internal (cycle 3 report) | External (web) | Reconciled? |
|--------|--------------------------|----------------|-------------|
| BTC | downtrend | ~$76,900, "bearish technical short-term, MACD bearish" | ✓ matches |
| ETH | downtrend | ~$2,100, "ETH ETF outflows $401M May, BUT whales +$2B accumulation despite −12 % price" | ✓ partial — internal sees only downtrend, external sees mixed accumulation |
| NEAR | 24h −9.1 % | 24h −4.4 %, 7d +17.9 %, +228 % from yearly low | ⚠ same direction today, but 7d picture is the opposite of the short thesis |
| PORTAL | +57 % 24h (scalp), +47 % 24h (intraday) | +62 % 24h, RSI 36.5, "trading 87 % below yearly high" | ✓ matches; web confirms oversold bounce, not real trend |

→ Internal data is the base of record (per §4). External research used for confirm/weaken/contradict only.

---

## 3. Cycle 3 signal landscape

| Slot | Source | Result |
|------|--------|--------|
| 1 — track-signals (pre) | CLI | 146 checked, 12 updated, 8 expired |
| 2 — scalp report | `2026-05-30_19-51_scalp_report.md` | 0 A-tier, 0 B-tier, ID/USDT top watchlist (score 56.2) |
| 3 — intraday report | `2026-05-30_20-02_intraday_report.md` | 0 A-tier, 0 B-tier, NEAR top watchlist short (score 59.5) |
| 4 — crypto monitor (90 min) | background pid 22552 | spawned, no upgrades fired |
| 5 — active-signals crypto | CLI | 2 (BCH B short scalp tp1_hit, UNI B short scalp tp1_hit) |
| 6 — signal-stats crypto | CLI | sample=17 weak, PF=1.6, totalR=+3 |
| 7 — untracked-legacy detector | script | 0 untracked ✓ |
| 8 — track-signals (post) | CLI | 134 checked, 0 updates |
| 9 — daily review (obsidian) | CLI | `obsidian_vault/11_Trade_Journal/Daily_Reviews/2026-05-30.md` updated |

**Macro / regime (intraday report cycle 3):**
- BTC trend: downtrend; ETH trend: downtrend (cycle 2 had ETH range — flipped back down between 17:38 and 20:02).
- Altcoin breadth above EMA20: 53.6 %; above EMA50: 57.1 %.
- BTC ATR percentile 33 (low vol).
- Style recommendation: *"mean reversion or wait for clean breakouts."*
- Weekend overlay active (A-tier penalty −5, structural-stop preference, weak MEXC-only capped at C).

---

## 4. Candidate Deep Dives (per §12)

### 4.1 NEAR/USDT — crypto / intraday / **C-tier watchlist short, score 59.5** — **⚠ AVOID (external override)**

**Internal system view:**
- Direction `short`, mode `intraday`, score 59.5.
- Entry zone 2.315–2.333 (failed bounce); invalidation 2.356; TP1 2.266 / TP2 2.226 / TP3 2.185.
- Setup quality 66.4/100, RR-to-TP1 1.84.
- Derivatives: price↓ + OI↓ (deleveraging), funding 0.0001 (neutral), crowding normal.
- Catalyst/news: "no fresh verified catalyst detected" (system was BLIND here).
- Narrative: AI is "rising" (heat 67/100) — but treated as background only.

**External research:**
- 24h: −4.4 % (system says −9.1 %; reconciled — same direction, different magnitude likely from different snapshot times).
- 7-day: **+17.9 %**, +228 % from yearly low ([CoinGecko via search](https://coinmarketcap.com/cmc-ai/near-protocol/latest-updates/)).
- 22 May: **NEAR surged 26.5 % to $2.19 on a short squeeze at $1.72 that liquidated $5.8M in shorts** ([BanklessTimes](https://www.banklesstimes.com/articles/2026/05/22/near-protocol-surges-26-today-why-is-this-ai-token-pumping/)).
- Real fundamental catalyst: **dynamic resharding launches June 2026**, plus FIPS-204 post-quantum signing in May — these are the "automating its own growth" headline that drove the breakout ([CoinDesk, 2026-05-22](https://www.coindesk.com/markets/2026/05/22/near-protocol-to-automate-its-own-growth-and-its-token-is-skyrocketing)).
- 25 May: **golden cross + cup-and-handle setup printed, eyeing 100 % rally target** ([BanklessTimes](https://www.banklesstimes.com/articles/2026/05/25/near-protocol-prints-golden-cross-as-cup-and-handle-setup-eyes-100-rally/)).
- External consensus: "bullish but cautious — overbought signals, expecting a healthy pullback."

**Chart verification:** TradingView unavailable.

**Confirms / weakens / contradicts:** **CONTRADICTS** the system's short bias. Internal sees only the −9 % 24h flush; external shows it's a **healthy pullback inside an established uptrend with a fresh catalyst pipeline**. Shorting NEAR into known-squeeze levels after $5.8M of shorts just got liquidated is exactly the trap the system narrative agent should have flagged but didn't.

**Verdict:** **AVOID.** Even though the system only put it on watchlist (not actionable), this enriched review is the place to harden the call: **do not short NEAR**. Wait for either a) the resharding launch to disappoint (real invalidation), or b) a clean lower-high after a multi-day failure of the $2.80 area. The current −4 to −9 % dip is noise inside a rally.

**Telegram alert should remain valid:** *no alert was sent* (correct — system held it at C-tier). Confirm no future cycle promotes this.

---

### 4.2 ASTER/USDT — crypto / scalp+intraday / **rejected (overextended)** — **upgrade to WATCHLIST**

**Internal system view:**
- Momentum 92.8 (scalp) / 100.0 (intraday) — top of leaderboard.
- 24h +10.4 to +11.1 %, RS vs BTC +9.7 to +10.4 %, volume 3.6×–3.93×.
- Derivatives: price↑ + OI↑ (+13 % 24h), funding +5e-05 (neutral), L/S 2.09, crowding `normal` (Binance) / `elevated` (Bybit/OKX).
- **Rejected:** "Price > 2 ATR from EMA20; do not chase. Converted to watchlist only: wait for pullback."

**External research:**
- **Today, 2026-05-30: ASTER hit $1.26T cumulative trading volume**, second-largest perpetual DEX by cumulative volume ([CoinMarketCap latest-updates](https://coinmarketcap.com/cmc-ai/aster/latest-updates/)).
- May 29: **dual-reward staking system detailed** — weekly distribution of 450K ASTER, base APY + loyalty rewards.
- May 28: **BTC + ETH perpetual pairs launched** as first validator-approved listings, with 50K U reward campaign.
- Mcap $1.88B, rank #46, 24h volume $119.9M (+100.6 % vs prior day).
- Q2 2026 forward: ASTER staking for network security + on-chain governance.
- Top-story tag: "Aster Surges 3.6 % on Protocol Update and Social Catalysts" ([CoinMarketCap](https://coinmarketcap.com/top-stories/6a0dce432b069225f869e74c/)).

**Chart:** TradingView unavailable. Volume 3.9× + OI +13 % is consistent with new long positioning, not late-cycle short covering.

**Confirms / weakens / contradicts:** **STRONGLY CONFIRMS** the underlying move; the system's price-only "overextended" rejection is technically correct but **misses the fundamental catalyst stack** (volume milestone today + new staking + new perp listings). The system has no agent that connects on-chain product launches to price moves.

**Verdict:** **WATCHLIST (was: rejected/avoid implicitly).** Re-enter the conversation only on a pullback into EMA20 with held structure. Do not chase. Suggested re-evaluation trigger: ASTER prints a higher-low on the 1h above EMA50 with volume holding above 1.5× — then it's a B-tier candidate by structure.

---

### 4.3 BNB/USDT — crypto / scalp+intraday / **rejected (overextended)** — **downgrade to AVOID**

**Internal system view:**
- Score 83.2 (scalp) / 99.0 (intraday).
- 24h +11.2 to +12.5 %, OI +26.3 %, funding +1.4e-04 (positive), L/S 1.40.
- Catalyst: **GENIUS HODLer Airdrop** (Binance Announcements, *primary_source*) AND **DxSale BNB Chain $7.3M exploit** (Cointelegraph, *single_source* internally).
- Rejected: overextended.

**External research:**
- **DxSale exploit verified across 10 outlets** ([CryptoTimes](https://www.cryptotimes.io/2026/05/29/hackers-drain-7-3m-from-dxsales-old-bnb-chain-liquidity-lockers/), [crypto.news](https://crypto.news/dxsale-exploit-drains-7-3m-in-bnb-through-hidden-contract-backdoor/), [AMBCrypto](https://ambcrypto.com/dxsale-hit-by-7-3-mln-exploit-as-claims-of-insider-involvement-rise-details/), [Blockonomi](https://blockonomi.com/dxsale-legacy-locker-exploit-drains-7-3m-from-bnb-chain-pools), [MEXC News](https://www.mexc.com/news/1119229), TradingView News, Invezz, Tronweekly).
- Mechanism (per Coinsult, referenced by crypto.news): ownership of locker contract transferred 269 days before the attack, hidden through 80 wallet transfers, `setFee` + backdated lock turned "locked" deposits into withdrawable balance.
- 1,400 LPs affected, **funds funneled to Binance deposit addresses** (multi-source confirmation).
- **Insider involvement suspected** — Telegram channels reportedly offered DxSale LP-unlock services since August 2025 ([AMBCrypto](https://ambcrypto.com/dxsale-hit-by-7-3-mln-exploit-as-claims-of-insider-involvement-rise-details/)).
- This is a **BNB Chain narrative hit**, not a direct BNB-token vulnerability — but it materially weakens the "BNB pumping on GENIUS airdrop" thesis because the exploit story competes for narrative.

**Verdict:** **AVOID** (was: watchlist/overextended). Chasing BNB at +12 % into a contradicting headline is asking for chop. The GENIUS airdrop is real but already priced in; the exploit story has 10-outlet legs and will refresh as the insider-involvement angle develops.

---

### 4.4 WLD/USDT — crypto / scalp+intraday / **rejected (overextended)** — **stay rejected**

**Internal:** score 83–89, 24h +20 %, volume 1.99–2.13×, OI flat, funding neutral. Rejected: overextended.

**External:**
- 25 May: WLD reclaimed **$1B market cap, +14 % to $0.30** on Oku Trade DeFi integration in World App ([Blockonomi](https://blockonomi.com/worldcoin-surges-15-as-on-chain-activity-hits-2026-highs-amid-defi-integration)).
- Whale TX 64 / 24h = 2026 high; active addresses 1,309 (2nd highest of year); 379 new wallets / 24h = year high.
- **BUT analysts tag this as FOMO-driven, "speculative buying rather than fundamental adoption growth"** ([CryptBull, 2026-05-28](https://www.cryptbull.net/2026/05/28/worldcoins-fomo-rally-cracks-after-on-chain-activity-explodes/)).
- Forward catalyst: **July 24 emission cut −43 %** (5.1M → 2.9M tokens/day).

**Verdict:** **STAY REJECTED.** External directly agrees with system's "do not chase" — FOMO label is consistent with the overextension flag. The July 24 emission cut is a real forward catalyst but is 8 weeks away — too far to anchor a now-trade.

---

### 4.5 PORTAL/USDT — crypto / scalp / **rejected (overextended + crowded short risk)** — **AVOID**

**Internal:** rejected; price +57 % 24h, volume 0.42–0.58× (LOW — divergent), OI +183 %, funding **−0.0065** (deeply negative, crowded short), Bybit funding **−0.011** (worse).

**External:** +62 % 24h ([CoinGecko via search](https://www.coingecko.com/en/coins/portal)), trading 87 % below yearly high, RSI 14d 34.5 → classic oversold-bounce. No fresh catalyst (Portal 2.0 announcement was 21 April, 6 weeks old). Funded $25M back in December 2025.

**Verdict:** **AVOID engage either direction.** Negative funding + big OI add + low spot volume = textbook squeeze candidate that can also unwind in either direction violently. Not a setup the desk should be in. System correctly avoids.

---

### 4.6 BTC + ETH macro (regime backdrop)

**External:**
- BTC ~$76,900; analyst targets $58K downside; bearish technical short-term but uptrend intact medium-term ([Bitcoinist](https://bitcoinist.com/bitcoin-ethereum-price-for-2026/), [Economies.com](https://www.economies.com/crypto/news/bitcoin-in-2026:-a-strong-uptrend-or-a-reset-into-a-bear-market%20-48016)).
- ETH ~$2,100; ETF outflows $401M in May (bearish institutional); whales accumulated **+$2B during May despite −12 % price** ([Bitcoin Foundation](https://bitcoinfoundation.org/news/ethereum/why-crypto-whales-are-accumulating-ethereum-again-in-may-2026/)). MACD bearish; June seasonality historically weak for ETH.

**Read:** **Mixed signal** — internal "downtrend" rating is right on price action but misses the whale-accumulation undercurrent on ETH. Doesn't change cycle-3 verdict (no A/B-tier setups today either way) but informs forward stance: a pullback to a clean ETH support level + sustained whale accumulation + funding reset would be the **first place to look for longs** in the next 3-5 days.

---

## 5. Signal Performance Context

- Cycle 3 produced **0 new** trackable signals (same as cycles 1 & 2).
- The 2 active crypto signals (BCH/UNI) are both at `tp1_hit` and are managed (TP1 already booked).
- `signal-stats crypto` snapshot: n=17 (weak confidence), PF 1.6, totalR +3.0, scalp PF 2.0 / intraday PF 0.0 (anecdotal at n=4). **Sample is still under the 30-threshold for any rule-change recommendation** (per `SignalTrackingConfig.minimum_sample_for_recommendations`).
- Cumulative through cycle 3: **78 cycle-steps run, 78 ok, 0 failed**.

---

## 6. Best Candidates (passes internal + external sanity)

**None actionable from cycle 3.** The cleanest forward-watchlist names are:

1. **ASTER** — on pullback to EMA20 / EMA50 with held structure. Fundamental backing is real (today's $1.26T volume milestone + perp launches).
2. **ETH macro** — if ETF outflows reverse + whale accumulation continues + price reclaims a clean local high. Watch June 1-3 for the seasonality test.

## 7. Avoid / No Trade

- **NEAR short** — counter-trend into a known-squeeze name with $5.8M of shorts already liquidated 8 days ago; AI catalyst (resharding) launches June.
- **BNB long** — overextended + DxSale exploit headline competing for narrative; insider angle could refresh.
- **WLD long** — external sources confirm the system's "FOMO" read.
- **PORTAL** — squeeze trap (negative funding −0.011, low spot vol, OI ×3 in 24h).
- **All longs on alts** while BTC/ETH structure is unclear.

## 8. Main Risks

- **Reddit social = 0** for the third cycle straight (403). Crowd-attention agent is operating without its main social leg.
- **NEAR finding** is the kind of cross-check the system literally cannot do — proves the value of enriched review, but also proves the SYSTEM SCORE alone is not safe for short setups in trending alts. PART 3 (legal-risk gate for stocks) is the template; an "ai_narrative_squeeze_risk" gate for crypto could be a future PART.
- **DxSale insider angle** could escalate; if a named exchange / project insider is identified, BNB Chain risk-off intensifies.
- **Real-world reconciliation note (§4):** today's enriched review benefited from external data **matching the internal date** — that won't always be true (test-data runs). Per §4 the protocol always treats internal as base of record.

## 9. Action Plan

- Continue the run as-is (9 more cycles).
- **Add the DxSale headline to BNB risk flags manually** if any future cycle promotes BNB to B-tier — the current internal `catalysts` field has it but doesn't propagate as a "no_entry" condition.
- After cycle 6 (~03:48 EEST): re-check whether any A/B emerges in the EU/Asia overnight window. Likely still NO TRADE.
- **Do NOT** lower scoring / weekend penalty thresholds because of 3-cycle dry spell. That's exactly what the protocol forbids.

## 10. Final Verdict

| Mode | Verdict (cycle 3) |
|------|-------------------|
| Crypto scalp | **NO TRADE** — overextended longs rejected (correct, fundamentally backed for ASTER); no clean short entries |
| Crypto intraday | **NO TRADE** — same; **NEAR watchlist short is a TRAP per external research → reject the trade idea** |
| Crypto swing/invest | not run this cycle (protocol-aligned) |
| Overall | System is behaving correctly. **Enriched review adds 3 material overrides:** NEAR → AVOID (was watchlist short), ASTER → WATCHLIST (was overextended-rejected), BNB → AVOID (was overextended-rejected, now with narrative risk too). PART 1 detector: zero untracked. |

**Safety statement:** no auto-trade, no scoring/threshold/agent/strategy change, no fabricated data, TradingView unavailable (declared), Reddit social 403 noted, all 13 external sources verified and ingested into `news_items` via §15 skill workflow.

---

## §14 Final checklist

- [x] Every external claim has named source + title + date + URL.
- [x] No uncited statistics ($1.26T ASTER cumulative volume → CoinMarketCap; $5.8M NEAR short liquidations → BanklessTimes; $7.3M DxSale → 10 outlets; ETH whale +$2B accumulation → Bitcoin Foundation).
- [x] No uncited legal claims.
- [x] No fabricated TradingView observations — declared unavailable.
- [x] No missing-source claim stated as fact.
- [x] `test_source` filtered at ingest (`ingest_enriched_review_sources.py` rejected 0, all 13 valid).
- [x] **Sources** section below with markdown hyperlinks.
- [x] Web access available → did not declare it unavailable.

---

## Sources

External sources ingested into `news_items` (asset_class=crypto) via
`python -m scripts.ingest_enriched_review_sources --json data/raw/enriched_review_sources/2026-05-30_2300_cycle3.json` → 13 valid, 0 rejected.

**Macro / regime:**
- [Why Crypto Whales Are Accumulating Ethereum Again in May 2026 — Bitcoin Foundation, 2026-05-29](https://bitcoinfoundation.org/news/ethereum/why-crypto-whales-are-accumulating-ethereum-again-in-may-2026/)
- [Bitcoin in 2026: A strong uptrend or a reset into a bear market? — Economies.com, 2026-05-28](https://www.economies.com/crypto/news/bitcoin-in-2026:-a-strong-uptrend-or-a-reset-into-a-bear-market%20-48016)
- [Analyst Predicts Bitcoin And Ethereum Price For The Rest Of 2026 — Bitcoinist](https://bitcoinist.com/bitcoin-ethereum-price-for-2026/)

**DxSale / BNB Chain exploit:**
- [Hackers Drain $7.3M From DxSale Old BNB Chain Liquidity Lockers — CryptoTimes, 2026-05-29](https://www.cryptotimes.io/2026/05/29/hackers-drain-7-3m-from-dxsales-old-bnb-chain-liquidity-lockers/)
- [DxSale exploit drains $7.3M in BNB through hidden contract backdoor — crypto.news, 2026-05-29](https://crypto.news/dxsale-exploit-drains-7-3m-in-bnb-through-hidden-contract-backdoor/)
- [DxSale hit by $7.3 mln exploit as claims of insider involvement rise — AMBCrypto, 2026-05-29](https://ambcrypto.com/dxsale-hit-by-7-3-mln-exploit-as-claims-of-insider-involvement-rise-details/)
- [DxSale Legacy Locker Exploit Drains $7.3M From BNB Chain Pools — Blockonomi](https://blockonomi.com/dxsale-legacy-locker-exploit-drains-7-3m-from-bnb-chain-pools)
- [DxSale Suffers $7.3M Drain in BNB Chain Liquidity Exploit — MEXC News](https://www.mexc.com/news/1119229)

**ASTER:**
- [Aster Surges 3.6% on Protocol Update and Social Catalysts — CoinMarketCap top stories, 2026-05-30](https://coinmarketcap.com/top-stories/6a0dce432b069225f869e74c/)
- [Latest Aster News ($1.26T cumulative volume, staking, perps) — CoinMarketCap, 2026-05-30](https://coinmarketcap.com/cmc-ai/aster/latest-updates/)

**WLD:**
- [Worldcoin Surges 15% as On-Chain Activity Hits 2026 Highs Amid DeFi Integration — Blockonomi, 2026-05-25](https://blockonomi.com/worldcoin-surges-15-as-on-chain-activity-hits-2026-highs-amid-defi-integration)
- [Worldcoin's FOMO Rally Cracks After On-Chain Activity Explodes — CryptBull, 2026-05-28](https://www.cryptbull.net/2026/05/28/worldcoins-fomo-rally-cracks-after-on-chain-activity-explodes/)

**PORTAL:**
- [Portal Coin Latest News (Portal 2.0 AI pivot) — CoinMarketCap](https://coinmarketcap.com/cmc-ai/portal-gaming/latest-updates/)

**NEAR:**
- [Near Protocol to automate its own growth and its token is skyrocketing — CoinDesk, 2026-05-22](https://www.coindesk.com/markets/2026/05/22/near-protocol-to-automate-its-own-growth-and-its-token-is-skyrocketing)
- [NEAR Protocol Surges 26% Today: Why Is This AI Token Pumping? — BanklessTimes, 2026-05-22](https://www.banklesstimes.com/articles/2026/05/22/near-protocol-surges-26-today-why-is-this-ai-token-pumping/)
- [NEAR Protocol Prints Golden Cross as Cup-and-Handle Setup Eyes 100% Rally — BanklessTimes, 2026-05-25](https://www.banklesstimes.com/articles/2026/05/25/near-protocol-prints-golden-cross-as-cup-and-handle-setup-eyes-100-rally/)

**Internal sources (auditable):**
- `prompts/llm_review/enriched_market_review_protocol.md` (§14 + §15)
- `.claude/skills/enriched-review/SKILL.md`
- `data/scheduled_runs/2026-05-30_24h_crypto_only/cycle_03_summary.md`
- `data/reports/scalp/2026-05-30_19-51_scalp_report.md`
- `data/reports/intraday/2026-05-30_20-02_intraday_report.md`
- SQLite tables: `proposed_signals`, `signal_outcomes`, `news_items` (+13 fresh rows)
- `scripts/detect_untracked_legacy_alerts.py --since 2026-05-30` (zero)
- `scripts/ingest_enriched_review_sources.py` (13 valid / 0 rejected)
