# Current Context For LLM

**Purpose**: a compact, paste-ready snapshot to drop into a fresh LLM session.

**How to refresh**:

- Recommended (when implemented): `python -m src.cli update-obsidian-context`.
- Today, also usable: run `python -m src.cli prepare-analysis --mode <mode>` to generate `data/processed/llm_analysis_packet.md`, then paste that content into the "Live snapshot" section below.
- Manual: copy from `data/processed/context_for_llm.md` and from the latest report under `data/reports/`.

---

## Static framing (do not delete)

You are working with `crypto-ai-desk`. Before using anything below:

1. Read `prompts/system/AI_TRADING_DESK_SYSTEM_PROMPT.md` — canonical operating contract.
2. Read [[System_Prompt_For_Analysis]] — vault-side mirror.
3. Read [[Pre_Analysis_Checklist]] before producing output.
4. Read [[Post_Analysis_Checklist]] before closing.

Key invariants:

- **Weekend Mode** activates automatically on Saturdays and Sundays in `Asia/Nicosia`. A-tier gets a margin penalty, weak signals cap at B, weak MEXC-only cap at C, chasing entries demote to C. See [[Weekend_Mode]] + [[Weekend_Mode_Checklist]]. Run `python -m src.cli weekend-status` to check.
- **Three modes only in code**: scalp / intraday / swing. `invest` falls back to `swing` with an announcement.
- A-tier requires score ≥ 80 AND no active caps.
- No invalidation → cap 50 → rejected.
- Stale data > 3h → cap 50 → rejected.
- MEXC-only → cap 70 (65 weak).
- Not on anchor → cap 75.
- Rumor-only catalyst → cap 55.
- Extreme adverse funding → cap 78.
- Telegram never raises score directly — only attention.
- `news_trader_bridge` is strictly read-only.

---

## Live snapshot (fill in or paste from `data/processed/context_for_llm.md` / `llm_analysis_packet.md`)

> Replace this block when refreshing.

### Mode run last

- Mode:
- Timestamp:
- Source report path:

### Regime

- Label:
- Risk mode:
- Recommended style:
- BTC trend / ETH trend:
- Breadth above EMA20:
- BTC ATR percentile:
- Confidence:

### Top candidates (mode-ranked)

- ...

### Active A/B-tier ideas

| Symbol | Tier | Score | Direction | Entry | SL | TP1 | TP2 | Caps |
|---|---|---|---|---|---|---|---|---|
| ... | ... | ... | ... | ... | ... | ... | ... | ... |

### Watchlist (C-tier with trigger)

- ...

### Rejected (top reasons in this run)

- `no clean invalidation`: ...
- `MEXC-only listing`: ...
- `extreme funding against ...`: ...

### Watchlist monitor — latest upgrades

- Symbol, tier change, score, direction, timestamp, alert sent yes/no.

### Latest Telegram alerts (bot outbound)

- ...

### News pulse (news_trader_bridge, 240 min lookback)

- signal_count:
- strong_count:
- Top categories:
- Top sources:

### Top useful news

- ...

### Top fake / unverified news

- ...

### Top narratives (NarrativeAgent)

- ... (status, heat_score)

### Risk warnings + coverage gaps

- ... (from `CoverageAuditAgent`)

### Focus for next session

- Mode:
- Sectors:
- Symbols on watch:
- Events to respect (CPI / FOMC / unlock / mainnet):
- One specific behavior change committed for next session:

---

## Related

- [[System_Prompt_For_Analysis]]
- [[Pre_Analysis_Checklist]]
- [[Post_Analysis_Checklist]]
- [[Pre_Trade_Checklist_For_LLM]]
- [[Post_Trade_Review_Checklist_For_LLM]]
- [[News_Evaluation_Checklist_For_LLM]]
- [[System_Modification_Checklist_For_LLM]]
- [[How_LLM_Should_Read_This_Vault]]

## Implemented status

- **Manual refresh today**. Automated refresh via `update-obsidian-context` and `prepare-analysis` is partially implemented (see `prompts/system/ANALYSIS_WORKFLOW_PROTOCOL.md` step 1).
