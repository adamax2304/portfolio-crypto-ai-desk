# Signal Tracking & Performance Audit — 2026-05-25

Are A/B tier proposed ideas registered, tracked, scored, and surfaced correctly? **Focus is on proposed signals, not user-executed trades.**

---

## 1. Are A-tier and B-tier ideas automatically saved?

### Crypto scalp (today)
- A-tier: **0** — nothing to register.
- B-tier: **0** — nothing to register.
- Expected DB inserts: 0. Observed: 0. **OK.**

### Crypto intraday (today)
- A-tier: 0. B-tier: 0. Same outcome.

### Stocks intraday (today)
The report finished with: `Regime=bullish | A/B ideas=8 | C watchlist=6 | rejected=14 | signals registered=14`.

| Symbol | Mode | Tier | Score | Dir | Registered? |
|--------|------|------|-------|-----|-------------|
| AAPL | intraday | A | 88.64 | long | YES (visible in active-signals) |
| LLY | intraday | A | 80.33 | long | YES |
| AMD | intraday | B | 78.77 | long | YES |
| XLK | intraday | B | 74.91 | long | YES |
| SMCI | intraday | B | 74.26 | long | YES |
| SMH | intraday | B | 73.93 | long | YES |
| UNH | intraday | B | 68.59 | long | YES |
| TSLA | intraday | B | 67.30 | long | YES |
| QQQ | intraday | C | 64.77 | long | YES |
| IWM | intraday | C | 56.47 | long | YES |
| SPY | intraday | C | 54.12 | long | YES |
| XLV | intraday | C | 52.46 | long | YES |
| MSTR | intraday | C | 51.54 | short | YES |
| DIA | intraday | C | 50.27 | long | YES |

So `signals registered=14` = 2 A + 6 B + 6 C. **All A/B were registered.** ✅

**Concern**: the registration is **inclusive of C-tier**. Per spec, "C-tier/watchlist ideas are only saved when they have a clear actionable trigger." Today's 6 C-tier names all have explicit entry zones — so the wiring is consistent — but the SPY/IWM/DIA/QQQ ETF C-tiers are essentially **regime confirmation noise**, not actionable trades. Tracking them is harmless but adds clutter.

**Flag**: stocks pipeline auto-registers all ranked ideas above the "no_trade" cutoff. **No A/B-only filter at registration**. Verify against requirements.

### Crypto signal registry today
- 0 new A/B → 0 new inserts. Verified by `signal-stats --asset-class crypto`: sample=1 (the single EDEN signal from 2026-05-22).

---

## 2. C-tier / Watchlist handling

- **Stocks**: C-tier ideas **are** being registered with full entry/invalidation/TP. This is liberal — a strict reading of the spec ("only when they have a clear actionable trigger") could argue these qualify because they have triggers. But the count (6 today on stocks alone) creates registry noise.
- **Crypto**: today's 5 watchlist ideas (NIL, SAHARA, BSB, TAO, LTC) — **uncertain** whether they were registered (they have entries but are explicitly labeled "WATCHLIST ONLY"). The active-signals output shows 0 crypto items in the active list, so either they were not registered, or they were registered but the active-signals filter only shows tier ≤ B.
- **Action item**: confirm via SQLite that crypto C-tier watchlist ideas are NOT being silently inserted as active signals.

---

## 3. Does tracking work after registration?

`track-signals --all` output:
```
checked = 19
updated = 0
tp_hits = 0
stopped = 0
expired = 0
not_triggered = 0
ambiguous = 0
no_ohlcv = 0
```

- ✅ **`no_ohlcv = 0`** — confirms Fix #1 worked: the tracker can locate stock OHLCV at `data/raw/stocks/{tf}/{SYMBOL}.csv`. (Crypto path remains `data/raw/ohlcv/{exchange}/{tf}/{SYMBOL}.csv`.)
- ✅ **Crypto + stocks both tracked**. Mixed asset classes processed in a single pass with no errors.
- ⚠️ **All 19 stayed `waiting`**. None transitioned to triggered, stopped, or expired. Given the US session has only been open ~80 min by the tracker's data, this is plausible — entries may be slightly above current price. But after a full day with `updated = 0`, the entry-trigger or expiry logic deserves scrutiny.

---

## 4. Are outcomes calculated?

The tracker supports these states (per spec): `waiting_for_entry`, `triggered`, `tp1/tp2/tp3_hit`, `stopped`, `expired`, `missed_no_entry`, `ambiguous`.

**Today's distribution**:
- waiting_for_entry: 19/19
- All other states: 0

**Concern**: no signal has transitioned in 36+ hours. Three possible causes:
1. Prices genuinely have not touched any entry zone yet (plausible for stocks where entries are slightly above current price).
2. The tracker only advances on completed candles and the 15m data has not refreshed since the report.
3. There is a logic gap in trigger detection (less likely — Fix #1 covered this).

**Action**: re-run `track-signals --all` after the US close today and confirm at least some intraday signals transition to either `triggered` or `not_triggered` / `expired`.

---

## 5. Winrate / profit factor

| Metric | Crypto | Stocks |
|--------|--------|--------|
| total_signals | 1 | 19 |
| triggered | 0 | 0 |
| wins | 0 | 0 |
| losses | 0 | 0 |
| TP1 hit rate | N/A | N/A |
| stop hit rate | N/A | N/A |
| triggered_winrate | N/A | N/A |
| avgR | None | None |
| totalR | 0.0 | 0.0 |
| profit_factor | None | None |
| capture rate | N/A | N/A |
| not-triggered rate | N/A | N/A |

**All metrics correctly None** — no triggered outcomes to compute against. **The system honestly returns None rather than fabricating 0% or 100%**. ✅

---

## 6. Stat breakdowns by category

`signal-stats --asset-class stocks` produced break-downs by:
- ✅ tier (3 rows: A, B, C)
- ✅ mode (intraday + swing)
- ✅ direction (long + short)
- ✅ exchange_confirmation (1 row, all stocks)
- ✅ weekend_mode (1 row, all Monday)
- ✅ sector (1 row only — sector tagging not granular yet)
- ✅ narrative (1 row only)
- ✅ setup (1 row only)

**Missing / weak**:
- `sector` and `narrative` collapse to 1 row each → the per-signal sector tagging on stocks is not propagating to the stats engine.
- No per-symbol breakdown.

**Crypto stats** have only 1 sample, so all breakdowns are degenerate.

---

## 7. Does signal performance appear in LLM packets?

- **`llm_analysis_packet.md` (crypto, stale)**: I did not see a dedicated "recent signal performance" section in the read window. It might exist deeper in the file but was not visible in inspected portions.
- **`llm_stocks_packet.md` (stocks, stale)**: same — not seen in the read window.
- **Today's reports themselves**: **no signal performance section**. The user reads the report without knowing what worked yesterday.

**Flag**: signal stats are **queryable** via CLI but **not embedded** in the live reports or the LLM packets that the LLM is supposed to read first. The protocol's promise that "the LLM should know recent signal performance" is **not delivered today**.

---

## 8. Obsidian performance logs

Files found:
- `obsidian_vault/11_Trade_Journal/Signal_Performance/Weekly_Reviews/2026-05-24_16-53_week_review.md` — yesterday's weekly review exists.
- `obsidian_vault/11_Trade_Journal/Signal_Performance/Signal_Logs/2026-05-22_EDEN_USDT_sig_c4442a063769e04f.md` — one historical crypto signal log.
- Templates exist: Daily_Signal_Review_Template, Signal_Log_Template, Weekly_Signal_Review_Template.

**Status**:
- ✅ The structure exists and at least one weekly review was generated.
- ❌ **No new signal logs today** for the 14 stocks signals just registered. Either auto-export is not wired for stocks, or it runs on a schedule not yet invoked.
- ⚠️ The stocks Obsidian folder (`obsidian_vault/16_Stocks/`) has rule/template pages but **no signal performance subfolder**.

**Action**: investigate whether `review-signals` or `track-signals` auto-exports per-signal logs to Obsidian for stocks. If not, this is a wiring gap.

---

## 9. Does the system auto-modify strategy?

**No automatic rule changes observed.**
- `signal-stats` is a passive query.
- `track-signals` only writes outcomes; does not touch scoring weights, position sizing, or risk rules.
- No file under `config/` was modified by today's runs (verified by `last modified` timestamps remaining yesterday).
- The system **correctly stays passive**. ✅

---

## 10. Sample-size warnings

- ✅ `signal-stats` returns "confidence=anecdotal" for n=1 and "confidence=weak" for n=19.
- ✅ The footer message "no observations produced — sample sizes are still small." appears when no triggered outcomes exist.
- ✅ The principle in the spec (anecdotal <10, weak 10–29, moderate 30–49, strong 50+, reliable 100+) is **embedded in the confidence labels**.

The system **does not** show winrate/PF tables on small samples — it returns `None`. Good discipline.

---

## 11. Final verdict on signal tracking

**Working correctly**, with the following caveats:

| Component | State |
|-----------|-------|
| Auto-registration of A/B ideas | ✅ Working (stocks confirmed; crypto starved today) |
| Auto-registration of C-tier | ⚠️ Working but **liberal** — registers all C with entries |
| Cross-asset-class tracking | ✅ Working (no_ohlcv=0) |
| Outcome state machine | ⚠️ All signals stuck in `waiting_for_entry` after 36h — needs verification under a trigger event |
| Per-asset-class stats | ✅ Working (separate crypto vs stocks) |
| Per-tier / mode / dir breakdown | ✅ Working |
| Per-sector / narrative breakdown | ⚠️ Collapses to single bucket — granularity missing |
| Winrate / PF / avgR | ✅ Correctly None (insufficient data) |
| Sample-size warnings | ✅ Present |
| Performance in LLM packet | ❌ Not visible in inspected sections |
| Performance in today's reports | ❌ Not included |
| Auto Obsidian logging today | ❌ No new signal logs for today's 14 registered ideas |
| Strategy auto-modification | ✅ None — passive only (good) |

**What can be trusted now**:
- The fact that 19 signals are tracked.
- The "none/anecdotal/weak" labels.
- The cross-asset path resolution.

**What needs manual verification before trusting**:
- Whether `active-signals` includes stale entries from days ago that should be marked expired.
- Whether the entry-trigger logic actually fires on real candle moves (run again after the US close).
- Whether C-tier ETF ideas should be excluded from registration.
- Whether crypto C-tier watchlist ideas are also being silently registered.

**What must be fixed before relying on winrate/PF**:
- Real triggered outcomes must accumulate (probably 30+ for "moderate" confidence).
- The expiry / not-triggered states must actually fire so winrate is computable.
- Signal performance must be **embedded in LLM packets** so the LLM uses recent outcomes when scoring fresh ideas.
