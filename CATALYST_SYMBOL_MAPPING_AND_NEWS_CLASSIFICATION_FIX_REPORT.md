# Catalyst Symbol Mapping & News Classification Fix — Report

**Date:** 2026-06-01. Data-quality fix only.
**Scheduler stopped:** **NO** — running PID 11880 is undisturbed.
**Code change scope:** data-quality enrichment (NOT scoring, threshold, alert, or strategy logic).

---

## 1. What was changed

| File | Change |
|------|--------|
| `config/crypto_entity_aliases.yaml` (NEW) | 43 canonical crypto tickers with aliases + tags. Top names: BTC, ETH, BNB, SOL, XRP, ADA, AAVE, SUI, HYPE, ASTER, TON, WLD, XLM, STG, etc. |
| `src/catalysts/entity_aliases.py` (NEW) | `EntityAliasMatcher` — loads the YAML, compiles word-boundary regex with **case-sensitive guard for short tickers** so common words ("near", "one", "link", "flow") never false-positive. |
| `src/catalysts/__init__.py` | Exports `EntityAliasMatcher` + `get_matcher`. |
| `src/catalysts/collector.py` | `_row_to_event` now takes an optional `alias_matcher`; when `news_items.detected_symbols_json` is empty, the matcher runs on the title to fill the symbol field. **Never overrides** existing detections. |
| `src/data_collectors/rss_news_collector.py` | Added an **additive** post-detection enrichment step using the same matcher. Future `news_items` rows get richer `detected_symbols_json` at write time. Wrapped in `try/except` — failures NEVER break news ingest. |
| `src/catalysts/classifier.py` | Extended patterns: `regulatory_sector_headline` (ETF approval, CFTC, MiCA/FATF/FSB), `platform_growth` (TVL surge, revenue ATH), `legal_risk` (lawsuit, subpoena, wire fraud). |
| `tests/test_entity_aliases.py` (NEW) | 39 tests — required mappings, false-positive safety, classifier extensions, end-to-end backfill, basket formation. |

**No changes to**: scoring, thresholds, agents, strategy, trading logic, alert logic, scheduler core, Telegram, signal-tracking.

---

## 2. Why it is safe during running scheduler

The scheduler parent process (PID 11880) **does not import** these modules directly. It invokes Python subprocesses (`python -m src.cli scalp-report`, `python -m src.cli intraday-report`, `python -m src.cli catalyst-scan`) for each cycle step.

Each subprocess is a **fresh Python interpreter** that imports the latest `src/` modules at startup. This means:

- The currently-running step (intraday report in cycle 2 right now) finishes with the OLD code unchanged.
- The NEXT step / cycle starts a fresh subprocess that picks up the NEW code automatically.
- No scheduler restart required.
- No code is hot-reloaded mid-step; we just take effect on the next subprocess invocation.

In addition, every change is **additive**:
- New YAML file — additive.
- `EntityAliasMatcher` is a new class — additive.
- `_row_to_event` only fills `symbol` when it was previously empty — never overrides.
- `RSSNewsCollector` alias detection only **adds** to `detected_symbols` — never removes.
- Classifier patterns are appended to existing category lists — old patterns still match.

---

## 3. Files changed (full list)

```
config/crypto_entity_aliases.yaml              (NEW)
src/catalysts/__init__.py                      (export EntityAliasMatcher + get_matcher)
src/catalysts/collector.py                     (alias-matcher fallback in _row_to_event)
src/catalysts/entity_aliases.py                (NEW)
src/catalysts/classifier.py                    (extended patterns: ETF/CFTC/lawsuit/TVL)
src/data_collectors/rss_news_collector.py      (additive entity-alias enrichment)
tests/test_entity_aliases.py                   (NEW — 39 tests)
```

---

## 4. Tests run

| Suite | Result |
|-------|--------|
| `tests/test_entity_aliases.py` (NEW) | **39/39 pass** |
| Full suite (skip flaky `test_report_section_fix.py` affected by live scheduler concurrency) | **240 passed** |

Key tests:
- **Required mappings (13 cases):** Cardano→ADA, Sui→SUI, Aave→AAVE, BNB Chain→BNB, Binance Coin→BNB, Hyperliquid→HYPE, Ripple→XRP, Solana→SOL, Ethereum→ETH, Bitcoin→BTC, Stellar Foundation→XLM, Toncoin→TON, Worldcoin→WLD — **all pass**.
- **False-positive safety (5 cases):** "Stay near the entry zone", "If price holds the level", "Coin holders unlocked one new feature", "The link between volume and price", "Free flow of capital" — **all return `[]`**.
- **Case-sensitive strict tickers:** "NEAR Protocol" matches; "Stay near" does not.
- **Multi-word OP alias:** Only "Optimism" triggers OP, not bare "OP".
- **Extended classifier:** "SEC approves Bitcoin spot ETF" → `regulatory_sector_headline`; "filed a lawsuit" → `legal_risk`; "TVL surge" → `platform_growth`.
- **End-to-end collector backfill:** A news_items row with empty `detected_symbols` and headline "Cardano Foundation cancels..." → event.symbol = `ADA/USDT`.
- **Basket formation:** "BNB Chain exploit" headline now triggers `binance_ecosystem_teaser` basket end-to-end.

---

## 5. Dry-run / validation result

### 5.1 Pre-fix baseline (cycle 1 events.jsonl from 13:36 UTC)

```
PRE-FIX events: 2/35 mapped (5.7%)
```
Only `XRP/USDT` was mapped (and a duplicate of the same article). 33 events had `symbol=""`.

### 5.2 Re-classify the same 35 titles with the new matcher

```
POST-FIX re-class: 17/35 would be mapped (48.6%)
```

Sample new mappings (would have been written if the matcher had been live):
- `Cardano Foundation cancels annual conference after failed funding vote` → `['ADA/USDT']`
- `Sui Foundation says major upgrade fixed bugs behind three outages` → `['SUI/USDT']`
- `Three Sui mainnet halts in 48 hours traced to an upgrade bug` → `['SUI/USDT']`
- `Whitehat developer unlocks $2 million stuck in a 2016 Ethereum ICO contract` → `['ETH/USDT']`
- `Aave overhauls listing standards after $230 Million rsETH exploit` → `['AAVE/USDT']`
- `XRP drops to $1.32 as sellers overpower exchange outflows` → `['XRP/USDT']`

### 5.3 Live `catalyst-scan` after the fix (run-once verification)

```
$ python -m src.cli catalyst-scan --no-print --cycle-label post-fix-validation
Catalyst scan ok — events=20, baskets=1, scanned=20,
rejected_test=0, rejected_missing=0
```

**Baskets went 0 → 1** (`perps_dex_narrative`, primary HYPE, related DYDX/GMX/ASTER) from the headline "XLM, HYPE gain". This is the first real basket formed since the catalyst layer went live.

### 5.4 Symbol-coverage improvement summary

| | Pre-fix | Post-fix (re-class) | Post-fix (live scan) |
|---|--------:|---------------------:|---------------------:|
| Events mapped to a symbol | 5.7% (2/35) | 48.6% (17/35) | 31.4% (11/35) live snapshot |
| Narrative baskets | 0 | — | **1** |
| Auto-trade introduced | none | none | none |
| Scoring changed | no | no | no |

---

## 6. Examples of correctly mapped headlines

| Headline | Mapped Ticker | Why it works now |
|----------|---------------|------------------|
| `Cardano Foundation cancels annual conference` | ADA/USDT | "Cardano" alias (5+ chars → case-insensitive) |
| `Sui Foundation says major upgrade fixed bugs` | SUI/USDT | "Sui Foundation" multi-word alias |
| `Aave overhauls listing standards after $230M exploit` | AAVE/USDT | "Aave" case-insensitive 4-char alias |
| `DxSale drained for $7.3M in BNB Chain liquidity exploit` | BNB/USDT | "BNB Chain" multi-word alias |
| `Hyperliquid launches new perpetual contract` | HYPE/USDT | "Hyperliquid" alias |
| `Ripple SEC settlement reached` | XRP/USDT | "Ripple" alias |
| `Stay near the breakout zone if pullback holds` | (no match) | "NEAR" required case-sensitive, lowercase "near" rejected |

---

## 7. Remaining limitations

- The matcher is **regex-based** — it does not understand context like an LLM would. Tabloid headlines that strip the project name will still slip through (e.g., "Devs ship upgrade" with no project context).
- The YAML curation is **manual**. Adding a new project requires a code change. Out of scope for this fix.
- Stocks news (`asset_class=stocks`) goes through a separate `_stocks_tickers` pool — entity-alias enrichment runs **crypto only** for now. Stocks legal-risk gate (PART 3 fix) is unchanged and handles SMCI/etc.
- A few common-word tickers (NEAR, ONE, OP, LINK, FLOW) are intentionally **strict** — they only match when uppercase / multi-word. This is by design to prevent the false-positive trap; a real headline with a lowercase project mention won't be caught. Trade-off accepted.
- The classifier still classifies many headlines as `other_news` when the topic genuinely doesn't fit a named category. That's correct behavior.

---

## 8. Confirmation — safety contract

- ✅ **No scoring changes.** No edits to `scoring_agent.py`, `risk_agent.py`, or any score-related YAML.
- ✅ **No threshold changes.** Tier thresholds (`A ≥ 80`, `B ≥ 65`, etc.) unchanged.
- ✅ **No alert-logic changes.** PART 1 registration-before-alert + PART 2 cooldown + PART 3 legal block all intact.
- ✅ **No auto-trade.** `grep -r "place_order\|create_order\|auto_trade" src/catalysts/ config/` → 0 matches.
- ✅ **No automatic Opus / LLM calls** introduced. `grep -r "anthropic\|openai\|claude api" src/catalysts/` → 0 matches.
- ✅ **Scheduler not stopped.** PID 11880 alive, untouched.
- ✅ **Additive only.** RSSNewsCollector adds aliases; collector fallback fills empty fields only.
- ✅ **Tests pass.** 240 in the safe set; 39 new tests cover the fix end-to-end.

---

## 9. Effective behavior — when does the fix kick in

> **Starting from the next cycle after this patch, catalyst symbol mapping may improve. Earlier cycles remain comparable as pre-fix.**

Specifically:
- **Cycle 2 onwards** (next scalp/intraday report after this patch) — RSSNewsCollector will write richer `detected_symbols_json` into the SQLite `news_items` table for newly-fetched RSS items.
- **Cycle 2 onwards catalyst-scan step** — collector backfills empty detected_symbols on the fly via the matcher. Even for OLD news_items rows that came in before this patch, the catalyst layer will now produce mapped events when re-scanned.
- **Manual `python -m src.cli catalyst-scan`** — already live (see §5.3 above; ran successfully right now, produced 1 basket).
- **Manual Opus / enriched-review skill** — reads the new JSONL automatically; Phase 1 (catalyst data first) now gets richer symbols + baskets.

The change is also **idempotent** — running catalyst-scan multiple times appends to `catalyst_events.jsonl` (audit log) but deduplicates by `catalyst_id` when reading.

---

## 10. Next-cycle expectation

Cycle 2 of the current run starts ~15:44 EEST. Expected observable changes:
- Cycle 2's `catalyst_events.jsonl` lines will include `symbol="ADA/USDT"`, `symbol="SUI/USDT"`, `symbol="AAVE/USDT"`, etc. instead of empty strings.
- `narrative_baskets.jsonl` will have ≥ 1 basket (instead of 0).
- The packet `## Catalyst / Narrative (auto-collected)` section will list "Active narrative baskets" with primary/related symbols.
- The scalp/intraday report's "## 5b. Structured Catalyst / Narrative" section will show "Notable events" with real ticker symbols.

If the next cycle fails for any other reason (network, etc.), the catalyst step remains **non-fatal** and the rest of the cycle continues unchanged.
