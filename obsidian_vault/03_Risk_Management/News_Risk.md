# News Risk

## How news lifts/lowers risk in code

- **`CatalystAgent.risk_events`** populated when a manual event has type `unlock / delisting / migration`. Adds the event to risk warnings and pushes `catalyst_quality` down by 0.25.
- **`RiskAgent`** adds +15 risk_score when `catalyst.risk_events` is non-empty plus an "avoid" line "Catalyst risk event is near the trading window."
- **`ScoringAgent`** indirectly: warnings add to `risk_penalty`; if total warnings ≥ 3, +5.
- **Verification cap**: if `catalyst.verification_status in {none, rumor, single_source}` and any catalyst is `rumor`, cap at 55.

## What counts as "news risk"

1. **Unverified rumor against direction**: caps your idea, but the bigger threat is acting on it.
2. **Verified bearish event during a long thesis** (or vice versa): close or skip.
3. **Pending unlock within 7 days** for the symbol: skip; the desk auto-tags.
4. **Pending listing on a different exchange** (often runs price then dumps after listing): treat with skepticism.
5. **Macro event window** (CPI, FOMC, jobs): the desk picks up macro keywords, but you must still respect the calendar manually.

## How to read news in the report

- `Top news` block — the top 15 by importance.
- `By symbol` block — per-ticker news.
- `By narrative` block — per-sector news.
- `Coverage audit` block — names which sources are missing or failing.
- `Macro pulse` (from `news_trader_bridge.macro_pulse`) — count of recent strong signals + top categories + top sources, last 240 min.

## News that should change your behavior immediately

- Listing on Binance / Coinbase (anchor venue) — sometimes already priced in via leak; check whether news_trader had it as `tier=strong` earlier.
- Major exchange hack / withdrawal pause — `risk_off` for the whole desk.
- Sanctions / lawsuit / SEC action against an asset you hold — close.
- War / attack / strike keywords in `macro_keywords.risk_off` — universally risk-off.

## Related

- [[News_System_Overview]]
- [[Catalyst_Agent]]
- [[Telegram_News_Evaluation]]
- [[News_Verification]]

## Implemented status

- **Implemented** for risk-event tagging on manual events + bridge macro pulse. Calendar-aware blocking **Recommended**.
