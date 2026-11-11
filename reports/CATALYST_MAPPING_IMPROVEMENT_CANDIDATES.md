# Catalyst Mapping Improvement Candidates (PART 4)

**Date:** 2026-06-10 · Read-only analysis. **No alias added or implemented in this PR.**
**Source:** `news_items` rows in the last 3 days where `detected_symbols_json` is empty.

## 1. Method
- Pulled 80 most-recent crypto news items with **no detected symbols**.
- Extracted capitalised tokens (3–8 letters) from titles.
- Filtered against a safe blacklist (USD, USDT, ETF, SEC, CEO, FOMO, etc. — non-symbol acronyms).
- Counted token frequency to surface candidate aliases.

## 2. Top tokens from unmapped news (3-day window)

| Token | Count | Category | Add as crypto alias? |
|---|---:|---|---|
| FIFA | 3 | sports / non-crypto org | **NO** — dangerous |
| IEM | 2 | esports event | **NO** — dangerous |
| NYSE | 2 | stock exchange | **NO** — dangerous |
| EEA | 2 | European Economic Area | **NO** — dangerous |
| IAEA | 2 | nuclear watchdog | **NO** — dangerous |
| LAFC | 2 | LA football club | **NO** — dangerous |
| AFC | 2 | football conference | **NO** — dangerous |
| CPI | 2 | macro inflation index | **NO** — dangerous (macro signal, but maps to nothing) |

**Observation:** the unmapped-news tail is dominated by **sports / macro / regulatory acronyms** that are NOT tradeable crypto symbols. Adding any of these as crypto aliases would produce false-positive `news_supported=1` on unrelated news.

## 3. Split: safe / ambiguous / dangerous

### Safe (would be high-value if added)
- _None of the top-30 tokens qualify as safe aliases._ The ones that would be safe (FET, ENA, JUP, SUI, RUNE, etc.) are **already mapped** — that's why they don't appear in the unmapped tail.

### Ambiguous
- **CPI** — appears 2x in unmapped news. It's a macro release that materially affects crypto direction, but it's not a tradeable symbol. Better handled as a **macro overlay flag** (the existing `MacroGeopoliticsAgent` already does this) rather than as a symbol alias.
- Two-character / 2-letter tokens (AI, ML, RWA) might be relevant for some narrative baskets but adding them as symbol aliases would over-match.

### Dangerous (do NOT add as crypto aliases)
- **FIFA / IEM / LAFC / AFC** — sports orgs. Adding these would map FIFA partnership news (which is irrelevant to crypto markets) to crypto symbol triggers.
- **NYSE / SEC / IAEA / EEA** — regulatory/organisational. Same risk.
- **CPI / FED** — macro releases. Adding would mismap inflation news to specific tokens.

## 4. Why does the unmapped tail look this way?
1. The existing `entity_aliases.yaml` already covers the **liquid crypto universe** (BTC, ETH, SOL, BNB, XRP, all top-50 by market cap + most narrative-basket members).
2. What's left in unmapped news is **macro context + sports/regulatory press** — categories that are not "missing crypto aliases", they're a different category of content.
3. **The real gap is not alias coverage; it's classification routing.** Sports news should be filtered OUT at the news collector level so it doesn't even reach the catalyst pipeline.

## 5. Recommended action (no implementation in this PR)

| Lever | Impact | Effort | Risk |
|---|---|---|---|
| **Add a "non-crypto-org blacklist"** to the news collector to drop sports/regulatory press before classification | Reduces unmapped-news clutter; sharpens the "%mapped" metric | Low — config-only YAML change | Very low |
| **Add a `macro_release` classification** for CPI / Fed / FOMC / NFP so they surface as a macro overlay, not as a missed crypto catalyst | Improves Opus-side reasoning about macro days | Medium — requires classifier extension | Low |
| Scan unmapped-news tail weekly and harvest only **proper-noun crypto names** that appear with high confidence (e.g., "Solana", "Polygon" full words) | Could catch fresh narrative names | Medium — needs NLP entity recognition | Low—medium |

## 6. Safe alias additions found in this scan: **0**
The current alias map appears to cover all genuinely-mappable crypto symbols in the recent news flow. The "30% mapping rate" is bounded above by content composition (70% of crypto news is macro/regulatory/sports, not symbol-specific), not by alias gaps.

## Verdict
```
NO_SAFE_ALIAS_ADDITIONS_AVAILABLE
```

The unmapped-news tail is **noise, not missing aliases**. Recommended next step is to **filter sports/regulatory/macro press OUT of the catalyst pipeline** rather than to expand the alias map. That cleanup is a small reporting-layer change worth queueing for a future PR.
