# Analyst Action Visibility (PART 5)

**Date:** 2026-06-15 · Display-only. No scoring boost, no tier change.

## Problem

Analyst actions (upgrade/downgrade/initiate/price-target) were classified by the
RSS classifier but never surfaced to Opus, the packet, or the dashboard.

## What changed

- `src/stocks/llm_packet.py` — new `_company_news_analyst_section`, wired into
  `build_stocks_packet`. Reads the latest company-news agent output, lists
  symbols with ticker-specific news, and **explicitly flags analyst actions**
  (`catalyst_type` contains "analyst") as an informational block. Also states
  honestly: *"Options / open-interest data: not available for stocks (earnings + news only)."*
- `src/stocks/agents/trade_idea_agent.py::_catalyst_meta_from_news` sets
  `is_analyst_action` and surfaces the analyst headline in catalyst_meta, so the
  Telegram catalyst line can read e.g. `Catalyst: analyst upgrade`.

## Rules honoured

- No scoring boost — analyst action is informational only (the stocks scorer's
  news_catalyst component is unchanged binary).
- Not mandatory — absence is fine.
- No tier promotion.

## Tests

The packet section + meta extraction are exercised by the stocks packet build;
`test_1`/`test_2` confirm the news flag path is unaffected for scoring.
