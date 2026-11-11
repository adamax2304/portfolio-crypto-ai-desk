# Signal Performance Checklist (for the LLM)

Use this whenever the operator asks about how the desk's signals have been performing, or before promoting an existing C-tier into something more aggressive.

## A — Inputs to read

- [ ] `data/processed/llm_analysis_packet.md` → section **Recent Signal Performance** (sample sizes, last 24h / 7d, breakdowns, observations).
- [ ] `db/crypto_ai_desk.sqlite` tables `proposed_signals`, `signal_outcomes` if the user wants raw data — they're the source of truth.
- [ ] Latest review under `obsidian_vault/11_Trade_Journal/Signal_Performance/Daily_Reviews/` or `Weekly_Reviews/`.

## B — Always state explicitly

- [ ] **Proposed signal ≠ executed trade.** Performance numbers describe what the *system* suggested, not what the operator actually traded.
- [ ] **Sample size first.** Always quote `n` and `confidence_level` before any winrate / profit factor.
- [ ] **No auto-changes.** The tracker is passive. Any rule/scoring suggestion you make must end with "requires manual approval".

## C — Sample size buckets

| n | label | what to do |
|---|---|---|
| < 10 | anecdotal | mention only, no conclusions |
| 10–29 | weak | weak observation; never recommend rule changes |
| 30–49 | moderate | observation possible; suggest only, ask for approval |
| 50–99 | stronger | observation; rule-change suggestions allowed (manual approval) |
| 100+ | reliable | strong observation; manual approval still required |

## D — Metric definitions (R-based)

- `winrate_triggered` = wins / triggered. **Excludes** not-triggered signals.
- `capture_rate` = triggered / total. Measures whether entries are realistic.
- `profit_factor` = Σ(positive_R) / |Σ(negative_R)|. Default R: stop=-1, tp1=+1, tp2=+2, tp3=+3.
- `MFE_R / MAE_R` = max favorable / adverse excursion expressed in R.
- `not_triggered` is its own bucket — never roll it into losses.
- `ambiguous` = stop and TP touched in the same candle. Reported separately; conservative R is -1 but flagged.

## E — Mandatory caveats when answering

- "These rates are based on a small sample (n=…)."
- "Proposed signals; real PnL depends on execution + fees + slippage."
- "Tracker is passive — any rule change needs manual approval."
- If the user asks for an automatic strategy change: refuse. Surface the observation and stop.

## F — Suggested commands to mention

```
python -m src.cli signal-stats --period today
python -m src.cli signal-stats --period week --mode intraday
python -m src.cli active-signals
python -m src.cli signal-detail sig_<hash>
python -m src.cli review-signals --period today --write-obsidian
python -m src.cli track-signals --all
```

## Related
- [[Signal_Tracking_and_Performance]]
- `prompts/system/AI_TRADING_DESK_SYSTEM_PROMPT.md`
- `config/signal_tracking.yaml`
