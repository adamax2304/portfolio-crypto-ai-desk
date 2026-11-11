# News / Catalyst / Narrative Audit — Post-Weekend

**As of:** 2026-06-07 (Sun) · READ-ONLY.

## 1. Volume
| Window | news_items |
|---|---|
| 24h | **614** |
| 48h | **1345** |
| 72h | **2304** |
| total | 5821 |

Steady ingest through the weekend — news/collector healthy, no gaps.

## 2. Sources (48h, top)
CryptoBriefing 318 · Motley Fool 234 · Yahoo Finance 178 · **t.me/lookonchain
122** · Seeking Alpha 77 · AMBCrypto 67 · **t.me/WalterBloomberg 59** · BeInCrypto
46 · MarketWatch 45 · CNBC 42 · CoinDesk 33 · Cointelegraph 25. Healthy crypto +
stocks mix; Telegram bridge feeding (lookonchain/WalterBloomberg).

## 3. Catalyst events & narratives
- Catalysts persist to **`data/catalysts/<date>/catalyst_events.jsonl`** (NOT a
  DB table) + `narrative_baskets.jsonl`. Today (06-07): **601 catalyst events**,
  fresh 11:04; latest cycle scan 151 rows.
- Narrative tags on news (48h): **46%** tagged. Top: **AI 545**, **Memes 92**,
  macro 8, RWA 7, L2 6, exploit_hack 2, etf_flows 1, semiconductors 1.
- Narrative baskets this slot: 1 (`momentum_breakout`, primary PARTI/USDT
  +18.5%, no confirmed news → `wait_pullback`). Overnight had 4 baskets
  (AI/perps/delisting) that didn't re-trigger.

## 4. Symbol mapping (the weak spot)
- **26–27% mapped** (347/1345 in 48h; day-cumulative 162/601 = 27%). **73%
  unmapped.** Consistent with prior audits (~24%) → **not a regression**, a
  persistent limitation. Catalyst layer remains **context-only** (it informs
  Opus/reports but does not, by itself, gate signals).

## 5. Importance distribution (48h)
Long tail, top items imp 3.0–3.8 (handful), bulk low-importance. Distribution
sane; high-importance items are real (SMCI 8-K, UNH DOJ probe).

## 6. Quality / duplicates / social-only
- Duplicates de-dup'd by URL at ingest (registry). No obvious flooding.
- Social-only (Telegram) claims are tagged by source and treated as
  context/attention, not as hard catalysts — correct handling.

## 7. Did the system catch weekend crypto narratives?
Yes — bearish risk-off regime corroborated; AI dominant narrative; PARTI
momentum basket surfaced; on-chain (lookonchain) flowing. Opus used these
correctly (cited, weekend-aware, flagged unmapped weakness).

## Answers
- **News arriving?** ✅ yes, steady (614/24h).
- **Catalysts classified correctly?** ✅ mostly; narratives sensible.
- **Narratives useful?** ✅ for context/Opus; AI/Memes/momentum baskets relevant.
- **Symbol mapping still weak?** ✅ **yes — 26–27%** (unchanged; P2 TODO).
- **Caught weekend crypto narratives?** ✅ yes.
- **Opus used narratives correctly?** ✅ yes (cited, flagged 73% unmapped).

## Technical bugs found
- None in collection/ingest. (My audit query initially used wrong table/column
  names — that was an audit-script error, fixed; production schema is fine:
  catalysts live in JSONL, not a DB table.)

## TODO (no code change made — quality, needs approval to alter mapping)
- **TODO-catalyst-symbol-mapping (P2):** 73% of catalysts unmapped to symbols.
  Improving the entity/alias matcher would raise catalyst→signal usefulness.
  Evidence: 162/601 mapped today. Risk: medium (touches matching that feeds
  scoring context) → propose, do not implement without approval.
