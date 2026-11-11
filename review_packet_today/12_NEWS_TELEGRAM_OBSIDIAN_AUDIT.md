# News / Telegram / Obsidian Audit — 2026-05-25

How external context was actually used (or not) in today's analyses.

---

## 1. News (RSS)

### Crypto

**Sources fetched (today):**
- Cointelegraph: 25 items
- CoinDesk: 25 items
- Decrypt: 25 items
- Binance Announcements: 20 items
- Coinbase Blog: disabled

**Items surfaced in reports:**
- "Price predictions 5/22: BTC, ETH, BNB, XRP, SOL, DOGE, HYPE, ADA, ZEC, BCH" (Cointelegraph) — tagged to BTC, ETH, BNB, XRP, SOL, DOGE
- "MicroStrategy buys more (MSTR)" — **test_source** (not real)
- "Coinbase reports record revenue (COIN)" — **test_source**
- "AAPL announces share buyback" — **test_source**, leaked into crypto report
- "NVDA beats earnings" — **test_source**, leaked into crypto report
- "Bitcoin risks drop to $72K as demand metric hits 2026 lows" (Cointelegraph)
- "Buterin fires back at Ethereum Foundation critics" (Cointelegraph)
- "Strategy Now Holds $65 Billion in Bitcoin" (Decrypt)

**Findings:**
- ✅ Real RSS feeds are fresh and being consumed.
- ⚠️ **Stocks `test_source` items are appearing in CRYPTO reports** (AAPL/NVDA/COIN/MSTR). The news pipeline does not strictly partition by asset_class — the test items were ingested once and surface across both pipelines. This is **cross-pollution at the news layer**.
- ⚠️ **News-symbol mapping is biased toward big-caps**. Today's top crypto movers (SAGA +37%, RENDER +9%, NEAR +9%, INJ +10%) have **NO fresh catalyst tagged**. The news pipeline only matches symbols listed in canonical RSS articles. Small-cap moves are essentially newsless to the system.
- ✅ Verification labels are present (`verification single_source`) — system is honest about thin sourcing.
- ⚠️ Single-source-rumor cap (55) was **not visibly triggered** today. All "fresh attention" callouts come from `single_source` items, yet scores like AAPL 88.64 stand. For stocks the cap may not be wired; for crypto it didn't apply because crypto produced no A/B.

### Stocks

**Sources fetched:**
- "Skipping disabled RSS source MarketWatch Top Stories"
- "Skipping disabled RSS source Yahoo Finance Top Stories"
- "Skipping disabled RSS source Seeking Alpha Market Currents"

**Items surfaced:**
- AAPL announces share buyback — **test_source**
- NVDA beats earnings — **test_source**
- COIN reports record revenue — **test_source**
- MSTR buys more — **test_source**

**Findings:**
- ❌ **No real stocks RSS source is enabled.** All four stocks news items come from `test_source` test fixtures.
- ⚠️ AAPL's idea explicitly uses "1 news catalyst(s) in lookback window" as evidence — that catalyst is a **test fixture**. AAPL's A-tier score (88.64) is partly justified by fake news.
- ✅ Per-symbol tagging works (CompanyNewsAgent did connect AAPL news to AAPL idea evidence).

**Verdict**: stocks news layer is **wired but starved**. Real stocks RSS is sitting disabled.

---

## 2. Telegram / news_trader bridge

**Source:** `C:\Users\adama\Documents\zeph ai projects\news_trader\` (read-only)

**Per protocol:**
- Telegram contributes only to attention staging, never to `catalyst_news` component.
- Rumor cap = 55.
- News_trader directory is strictly read-only.

**Today's status:**
- ✅ Read-only invariant honored (no writes attempted; the constraint is preserved verbatim in CLAUDE.md and respected by the bridge).
- ❌ **No fresh Telegram/KOL items detected today**. The LLM packet's KOL section reads: *"Configured sources: Manual KOL notes, example_account. Manual signal count: 0. Symbols: none. No manual KOL/crowd notes found; X/Telegram/Discord context is not live yet."*
- ⚠️ The KOL watchlist still has `example_account` as a placeholder — explicitly flagged by the system ("KOL watchlist still contains the placeholder account; replace it with trusted sources").

**Verdict**: Telegram bridge **structurally present, runtime silent**. Today's analysis had **zero Telegram influence**. The system is honest about this.

---

## 3. Obsidian

**Files referenced in protocol:**
- `obsidian_vault/15_LLM_Context/Current_Context_For_LLM.md`
- `obsidian_vault/15_LLM_Context/Pre_Analysis_Checklist.md`
- `obsidian_vault/15_LLM_Context/Post_Analysis_Checklist.md`
- `obsidian_vault/01_Market_Regime/Weekend_Mode.md`
- `obsidian_vault/16_Stocks/*`

**Status:**
- ✅ Files exist on disk.
- ❌ **`Current_Context_For_LLM.md` is still a template** — the body says "Replace this block when refreshing" and the fields are empty. `update-obsidian-context` CLI is a TODO stub, so the dynamic context never auto-refreshes.
- ⚠️ The structured rule pages (System Prompt mirror, checklists, Weekend Mode docs) **do** exist but their use is purely manual — they are not pulled into the LLM packet automatically. The crypto LLM packet does inline the System Prompt at the top, which is good, but the checklists and Obsidian rules are not embedded.

**Verdict**: Obsidian is a **static knowledge base** today, not a live context channel. The dynamic refresh promise is unfulfilled.

---

## 4. Macro / geopolitics

**Sources:**
- MacroGeopoliticsAgent (crypto pipeline only)

**Today's output (in both crypto reports):**
- Risk score 35/100
- BTC bias: neutral / data-watch
- 1 risk-off headline: "BTC price to attack $80K shorts on Iran peace deal" (Cointelegraph)
- 0 risk-on hits, 0 calendar/watch hits

**Findings:**
- ⚠️ The macro/geopolitics surface is **one headline from a crypto news source**. There is no Fed calendar, no DXY, no yields, no actual macro feed. The CoverageAuditAgent acknowledges this explicitly.
- ✅ The system **does not** treat that single headline as a trade trigger — risk score 35 is treated as background context, not a buy/sell signal.
- ❌ **Stocks pipeline has no MacroGeopoliticsAgent at all.** US equity intraday decisions today were made without any macro overlay (no FOMC stance, no rate context, no DXY). For an intraday-stocks read this is a real gap.

---

## 5. Did the system overuse weak news?

- AAPL A-tier (88.64) has only **1 news catalyst** in its evidence — a test_source "share buyback" item. The 88.64 score is largely driven by RS + above-prev-day-high + tape, not by news. So news contributed but did not dominate.
- LLY A-tier (80.33) has **0 news catalysts** in its evidence — it stands on RS alone.
- Crypto: top movers (SAGA, RENDER, NEAR, INJ) **got no news boost**. Without news they still scored ≥95 raw but were rejected on overextension. The narrative agent's AI sector heat (48.5/100) tagged NEAR and TAO as representatives — that did flow into the narrative scoring component (e.g. TAO got narrative=2.9 of ~5 max).

**Verdict**: news was **not** overused as a score driver. The bigger issue is the opposite — news is **under-coupled** to the small-cap crypto movers that actually need a catalyst story.

---

## 6. Did the system ignore important news?

Unknown — we cannot tell what *important* news existed but was unfetched. With 4 crypto RSS sources and 0 real stocks RSS sources, **whole categories of relevant news** (Fed speakers, ETF flows, on-chain whale moves, exchange listings, hack alerts) are simply not in the feed.

---

## Summary table

| Channel | Configured? | Fresh items today? | Used in analysis? | Honest about gaps? |
|---------|-------------|--------------------|--------------------|--------------------|
| Crypto RSS | Yes | Yes (4 sources, ~95 items) | Yes (big-cap only) | Yes |
| Stocks RSS | Disabled | No real items | Only test_source items | ⚠️ The reports do not loudly say "all news is fake"; only the audit reveals it |
| Telegram / news_trader bridge | Yes (read-only) | No fresh items today | No | Yes |
| KOL watchlist | Placeholder | No items | No | Yes — system flags placeholder |
| Obsidian dynamic context | Stub | n/a (auto-refresh not implemented) | No | Implicitly — protocol claims it, code doesn't |
| Macro/geopolitics (crypto) | Yes | 1 headline | As background | Yes |
| Macro/geopolitics (stocks) | **Not wired** | n/a | No | **Not surfaced as a gap in the stocks report** |

**Net**: the news/external-context layer is **functional but uneven**. Stocks news is the weakest pillar (fake data + disabled real feeds + no macro). Crypto news is thin but real and honest about its limits.
