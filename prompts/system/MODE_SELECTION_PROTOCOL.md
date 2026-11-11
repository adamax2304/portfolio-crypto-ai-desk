# Mode Selection Protocol

How to identify the requested mode and apply the right rules. Do not mix mode logic.

---

## Modes the desk supports

| Mode | Status | Horizon | Timeframes | Primary TF | CLI |
|---|---|---|---|---|---|
| scalp | **Implemented** | 30m–2h | 1m / 5m / 15m | 5m | `scalp-report --auto-universe` |
| intraday | **Implemented** (default) | 4–24h | 15m / 1h / 4h | 1h | `intraday-report` |
| swing | **Implemented** | several days | 1h / 4h / 1d | 4h | `swing-report --auto-universe` |
| invest / long-term | **Recommended / not implemented** | weeks–months | 1d / 1w | 1d | (fallback to `swing-report` + manual thesis overlay) |
| review | meta-mode | any | n/a | n/a | `review` |
| news-only | meta-mode | any | n/a | n/a | (no report; consume `context_for_llm.md` + bridge) |
| candidate-debug | meta-mode | any | n/a | n/a | `candidate-debug --symbol X --mode <mode>` |

## How to detect the requested mode

| User phrasing | Detected mode |
|---|---|
| "scalp", "next hour", "5m chart", "сейчас" | scalp |
| "intraday", "today", "morning", "сегодня", "интрадей" | intraday (default) |
| "swing", "few days", "multi-day", "свинг" | swing |
| "invest", "hold long", "weeks", "months", "инвест", "долгосрок" | invest → fallback to swing |
| "review", "what worked", "обзор", "ревью" | review |
| "news", "telegram", "channel said" | news-only |
| "why X is rejected" / "debug X" | candidate-debug |
| nothing specific | intraday |

State the mode in your first sentence. If `invest` was requested, **announce the fallback explicitly**:

> "Invest mode is not implemented in code. Running `swing` analysis as the closest proxy. Long-term thesis overlay should be added manually using `obsidian_vault/10_Trade_Idea_Format/Long_Term_Trade_Template.md`."

## Per-mode rules (do not mix)

### Scalp

- Tight invalidation (1.2 ATR or recent local S/R).
- Time stop: exit if no progress in 30 min.
- Only trade in active session (US / EU / Asia open).
- No scalp in `high-volatility danger` regime unless size reduced.
- Funding > +0.001 or < -0.001 against direction → cap 78.
- Don't trade Telegram catalysts on 5m charts; they're too slow.

### Intraday

- Default mode. Calibration baseline.
- 1h close past invalidation = stop hit.
- Demand R/R to TP1 ≥ 1; ideal R/R to TP2 ≥ 2.
- Skip if data freshness > 60 min for the relevant timeframes.

### Swing

- Wider invalidation (built off 1h but mentally treat 4h).
- Re-evaluate at every 4h close.
- Skip if known token unlock within 7 days for the symbol.
- Narrative + catalyst weighting active (×1.30 / ×1.20).
- Don't take swing in `high-volatility danger`.

### Invest / long-term (fallback)

Since the desk has no implemented invest mode:

1. Run `python -m src.cli swing-report --auto-universe` to get the structural read.
2. Apply additional manual checks:
   - Anchor exchange only.
   - 1d / 1w trend up or accumulating.
   - Macro context (rates / dollar / ETF flows) — external sources.
   - Sector narrative durability (`hot` for ≥ 2 weeks).
   - Tokenomics + unlock pipeline (≥ 30 days from next major unlock).
3. Use `Long_Term_Trade_Template` from the vault.
4. Position sizing manual — the desk does not produce long-term sizes.

### Review

- Run `python -m src.cli review`.
- Read `data/reports/reviews/<latest>.md`.
- Follow [[REVIEW_AND_LEARNING_PROTOCOL]].
- Do not generate new trade ideas during review.

### News-only

- Read `data/processed/news_trader_bridge_latest.json`.
- Read `data/processed/context_for_llm.md` (news + macro sections).
- Apply [[NEWS_INTELLIGENCE_PROTOCOL]].
- Do not synthesize trades from news alone — output attention + classification only.

### Candidate-debug

- Run `python -m src.cli candidate-debug --symbol <SYMBOL> --mode <mode>`.
- Read `obsidian_vault/13_Debugging_and_Improvement/Candidate_Debug_Guide.md`.
- Explain why the symbol passed / failed / was capped. No trade output.

## Mode mismatch detection

If the user asks "should I take this swing trade?" but the symbol's idea was generated under `scalp`:

1. State the mismatch explicitly.
2. Recommend re-running in the requested mode before answering.
3. Do **not** mentally re-score a scalp idea as swing — the multipliers are wrong.

## Edge cases

- "Trade now" without mode → default to `scalp` if session is active, else `intraday`.
- "Best opportunities right now" → `intraday` unless data is clearly scalp-tuned.
- "Position for the next month" → `invest` fallback with manual overlay.
- Mixed: scalp this name and swing that one → **two separate analyses**, each in its own mode.

## Related

- [[AI_TRADING_DESK_SYSTEM_PROMPT]]
- [[ANALYSIS_WORKFLOW_PROTOCOL]]
- [[RISK_AND_SCORING_PROTOCOL]]
