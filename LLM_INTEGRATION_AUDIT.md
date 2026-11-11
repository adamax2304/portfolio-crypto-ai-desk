# LLM Integration Audit

**Date:** 2026-05-29. Read-only audit. No code changed.

---

## Headline answer

**The project does NOT call any LLM automatically. It is "manual-only / LLM-ready".**

Reports, monitoring, scoring, tiering, and Telegram alerts are produced **100% by deterministic rule-based agents + Markdown templates**. The "LLM packets" are **files saved to disk for a human (or an external Claude/GPT session) to read manually** — they are never sent to any API by the project.

The LLM in the loop is **you/me, in this chat**, when the user pastes a packet or asks for analysis. The desk itself never makes an API call.

---

## Evidence

### 1. Is there an Anthropic/Claude/OpenRouter/OpenAI API integration?
**No.**
- No LLM SDK in dependencies (`requirements*.txt` / `pyproject.toml` → no `anthropic`, `openai`, `openrouter`, `litellm`, `langchain`).
- No HTTP calls to `api.anthropic.com`, `api.openai.com`, `openrouter.ai`, `messages.create`, or `chat.completions` anywhere in the `.py` source.
- No API keys in `config/`.
- `.env.example` contains only:
  ```
  # Optional future LLM summaries. The deterministic report builder works without this.
  OPENAI_API_KEY=
  ```
  → an empty placeholder, explicitly marked "optional future", and unused by any code path.

### 2. Which model is configured?
**None.** No model name (`opus`, `sonnet`, `gpt-*`) is referenced in source. There is no model selection because there is no API client.

### 3. Which commands call the LLM?
**None call an LLM.** All are rule-based:
| Command | LLM call? | What it actually does |
|---------|-----------|------------------------|
| `scalp-report` | ❌ | Supervisor runs agents → `ReportBuilder` renders Markdown from templates |
| `intraday-report` | ❌ | same |
| `stocks-intraday-report` | ❌ | `StocksPipeline` agents → `stocks_report_builder` templates |
| `monitor-watchlist` | ❌ | re-scores watchlist via agents; rule-based tier flip → Telegram |
| `stocks-monitor-session` | ❌ | re-runs stocks report + `MaterialImprovementChecker` (pure logic) |
| final daily review (schedulers) | ❌ | concatenates CLI outputs into Markdown |

`src/reports/report_builder.py` has a method named `build_context_for_llm` — but that only **writes** `context_for_llm.md` to disk. It does not contact an LLM.

### 4. If no LLM is called automatically — stated clearly:
✅ **Confirmed: no automatic LLM call exists. The pipeline is fully deterministic.**

### 5. Files created for LLM context
All three exist and are real, freshly-generated files:
- `data/processed/context_for_llm.md` — live desk snapshot (regime, movers, derivatives, news).
- `data/processed/llm_analysis_packet.md` — crypto packet (system prompt + context + latest report + signal stats + checklist).
- `data/processed/llm_stocks_packet.md` — stocks packet (stocks regime, sectors, latest stocks report, signal stats, earnings).

### 6. Are these packets sent to the LLM, or saved for manual use?
**Saved for manual use only.** They are written to `data/processed/` by `write_packet` / `write_stocks_packet` / `build_context_for_llm`. Nothing reads them back and POSTs them to an API. The intended workflow: the user opens the packet (or this chat reads it) and reasons over it manually.

### 7-8. Is there a system prompt? Where?
**Yes** — `prompts/system/AI_TRADING_DESK_SYSTEM_PROMPT.md` (8.2 KB). It is **inlined into `llm_analysis_packet.md`** at generation time, so a human/LLM reading the packet sees it. It is a *document*, not a programmatic `system=` parameter (there is no API call to attach it to).

### 9. Does the system prompt include…?
| Item | Present? |
|------|----------|
| asset_class separation | ✅ (crypto vs stocks; packets are asset-isolated) |
| crypto rules | ✅ (MEXC caps, OI/funding, BTC/ETH regime) |
| stocks rules | ✅ (index/sector confirmation, earnings overrides — in stocks packet) |
| no auto-trade rule | ✅ (implicit + "NO TRADE is a valid, preferred answer"; the project has no order-placement code at all) |
| signal performance | ✅ (Recent Signal Performance embedded in packets + reports) |
| missing data handling | ✅ ("Never invent missing data. If a field is empty, say so and downgrade confidence.") |
| risk/reward protocol | ✅ ("≥1R to TP1, ideally ≥2R to TP2; invalidation mandatory") |
| stale data | ✅ ("OHLCV > 3h → cap 50 → rejected") |
| invalidation mandatory | ✅ ("No idea without a clean invalidation → cap 50 → rejected") |
| Weekend Mode | ✅ |

So the *guidance* is comprehensive — but it only takes effect when a human/LLM actually reads the packet. The deterministic agents enforce a subset of these (caps, tiers, invalidation gating) in code; the rest are advisory text for the reader.

### 10-11. Does the LLM have direct internet/news access?
**N/A — there is no automatic LLM.** News is **collected by the project** via RSS collectors (`src/data_collectors/rss_news_collector.py`: Cointelegraph, CoinDesk, Decrypt, Binance Announcements) + Reddit social + the read-only `news_trader` bridge. That collected news is summarized into the packets. An external LLM reading the packet sees only the **collected** news — it has no live internet unless the human's chat tool provides it.

### 12. Does every scheduled cycle use LLM reasoning?
**No cycle uses LLM reasoning.** Every cycle is deterministic agents + templates. The only "LLM reasoning" that ever happens is when the user brings a packet into a chat like this one.

### 13. If not, which cycles SHOULD use it?
Highest-value insertion points (recommendation, not implemented):
- **Final daily / 12h review** — an LLM could synthesize the day's reports + signal stats into a narrative verdict. Best ROI, lowest risk (read-only summary).
- **A/B trade-idea narrative** — an LLM could write the counter-thesis / "why it matters" per idea (currently templated/canned). Medium value.
- **NOT** scalp/intraday every 2h — too frequent, would burn tokens for marginal gain; the deterministic scoring already handles tiering.

---

## What is working
- Deterministic agent pipeline (regime, momentum, derivatives, technical, risk, scoring, tiering) — fully functional, no LLM needed.
- LLM **context packets** are generated fresh, asset-isolated, with system prompt + signal performance embedded.
- A complete, well-written system prompt exists with all the right invariants.
- Telegram, tracking, stats — all rule-based and working.

## What is missing
- **No programmatic LLM call** — packets are never auto-sent; no API client, no model configured, no key.
- The system prompt's richer judgments (counter-thesis quality, narrative synthesis) are only realized if a human pastes the packet into an LLM.
- `OPENAI_API_KEY` placeholder is a dangling "future" hook with no consumer.

## What should be improved (if you want real LLM integration)
1. Add an optional LLM client (Anthropic SDK, model = your choice e.g. Opus/Sonnet) gated behind a config flag + key — **off by default**, so the deterministic path stays the default.
2. Use it only at the **final review** step first (lowest frequency, highest synthesis value), feeding it `llm_analysis_packet.md` + `llm_stocks_packet.md`.
3. Keep the hard rule: LLM output is **advisory only** — it must not place trades, change scores, or alter thresholds.
4. Pass collected news only (no live internet) to keep determinism + auditability.

---

## Final verdict

**LLM integration: NOT integrated (manual-only / LLM-ready).**

- The desk is a **deterministic, rule-based research engine.** It builds everything itself.
- It **prepares** excellent LLM context packets + a system prompt, but **never calls an LLM.**
- The LLM-in-the-loop is the human's external chat session (this one). To make it automatic, a gated, optional LLM client would need to be added — recommended for the final-review step only, advisory-only, off by default.
