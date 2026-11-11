# Catalyst / Stocks Symbol Mapping — Fix Report (PART 19)

**Date:** 2026-06-03
**Severity:** MEDIUM (catalyst coverage)
**Scope:** Catalyst layer + RSS news collector + stocks aliases.

## Problem

The system audit reported that **~80 % of stocks-side catalysts came
out symbol-less** — the catalyst classifier was firing on event
keywords but the upstream news collector wasn't mapping company /
product names to tickers. The crypto path already had a curated
`config/crypto_entity_aliases.yaml` + `EntityAliasMatcher`; stocks had
no counterpart, so headlines like "Super Micro indicted", "Apple
unveils AI features", "Broadcom hits AI revenue record" were ingested
with `detected_symbols=[]`.

## Fix

### 1. Generalise `EntityAliasMatcher` (`src/catalysts/entity_aliases.py`)

Added a `suffix: str = "/USDT"` field. Crypto path keeps `suffix="/USDT"`
(legacy contract — callers compare against `BTC/USDT` storage form);
stocks path uses `suffix=""` (bare tickers — `SMCI`, `AAPL`).

Refactored `load()` into a private `_load_yaml(path, *, suffix)` helper.
Added `load_stocks(project_root)` classmethod + cached
`get_stocks_matcher(project_root)` factory mirroring `get_matcher()`.

### 2. New file: `config/stocks_entity_aliases.yaml`

28 tickers covering the universe:

| Bucket | Tickers |
|---|---|
| Mega caps | AAPL, MSFT, GOOGL, AMZN, META, NFLX, TSLA |
| AI / semis | NVDA, AMD, AVGO, SMCI, PLTR |
| Crypto-equity | COIN, MSTR |
| Defensives | JPM, XOM, UNH, LLY |
| Index ETFs | SPY, QQQ, IWM, DIA |
| Sector ETFs | SMH, XLK, XLF, XLE, XLV, XLY |

Each entry has `canonical_name`, `aliases:` (the long-form names PLUS
key person where canonical — "Jensen Huang"→NVDA, "Saylor"→MSTR,
"Lisa Su"→AMD, "Hock Tan"→AVGO), and `tags:`.

Specifically required by the audit:

- "Super Micro" / "Supermicro" / "Super Micro Computer" → SMCI
- "Apple Inc" / "Apple Computer" / "Cupertino" → AAPL
- "Advanced Micro Devices" → AMD
- "Broadcom" / "Broadcom Inc" → AVGO
- "Nvidia" / "NVIDIA" → NVDA
- "SPDR S&P 500 ETF" / "S&P 500 ETF" → SPY
- "Invesco QQQ" / "Nasdaq-100 ETF" → QQQ

### 3. False-positive safety

The matcher's case-sensitivity rules (PART per `_is_strict_ticker`)
already protect short tickers — "AMD" hits "AMD", not "amdahl"; "META"
hits "META", not "meta-analysis"; "DIA" hits "DIA", not "Buenos dia".
Long-form aliases ("Apple Inc", not bare "apple") prevent generic-noun
false positives.

### 4. Wire-up in `rss_news_collector.py`

For sources tagged `asset_class: stocks` the collector now calls
`get_stocks_matcher(...)` instead of the crypto matcher. Crypto
sources keep the existing path. Failure is read-only and tolerated:
matcher exceptions are swallowed so news ingest never breaks.

## Verification

14 pin tests in `tests/test_stocks_entity_aliases.py`:

- ✅ Super Micro / Supermicro / Super Micro Computer → SMCI
- ✅ Apple Inc → AAPL; "apple harvest" prose does NOT → AAPL
- ✅ Advanced Micro Devices → AMD; "amdahl model" does NOT → AMD
- ✅ Broadcom Inc → AVGO
- ✅ Nvidia + Jensen Huang → NVDA
- ✅ SPDR S&P 500 ETF Trust → SPY
- ✅ Invesco QQQ Trust → QQQ
- ✅ "meta-analysis" does NOT → META
- ✅ "Buenos dia" does NOT → DIA
- ✅ Returned tickers are BARE (no `/USDT` suffix)
- ✅ Cached factory `get_stocks_matcher()` loads SMCI
- ✅ Multi-symbol headline ("Nvidia and Broadcom … Super Micro racks")
  → {NVDA, AVGO, SMCI}
- ✅ **Crypto matcher unchanged** — `get_matcher(...)` still appends
  `/USDT` (regression safety pin)

## Safety contract — preserved

- ✅ No auto-trade.
- ✅ No global threshold change.
- ✅ No crypto-side change. (Crypto matcher behaviour pinned by
  regression test; suffix still `/USDT`.)
- ✅ No filter weakening — this is a coverage IMPROVEMENT
  (more headlines now correctly carry detected_symbols).
- ✅ No historical data deleted.
- ✅ No new dependencies, no paid APIs (YAML + regex only).

## Files touched

- `src/catalysts/entity_aliases.py` — `suffix` field, `load_stocks()`,
  `get_stocks_matcher()`, refactored `_load_yaml()`
- `src/data_collectors/rss_news_collector.py` — stocks-source path uses
  `get_stocks_matcher()`
- `config/stocks_entity_aliases.yaml` — NEW (28 tickers)
- `tests/test_stocks_entity_aliases.py` — NEW (14 tests)
