# How to Adjust Scoring

Same surface as [[How_to_Adjust_Filters]] but focused on the scoring math.

## Principles

- **Calibrate against backtests, not vibes.** Use `ReviewAgent` outputs.
- **Adjust one knob at a time.** Otherwise you can't tell which change moved the needle.
- **Keep base weights summing to ~100.**
- **Multipliers between 0.7 and 1.3 are gentle.** Values outside that change desk character.
- **Caps are global rules**, not symbol-specific. Treat them as constitutional.

## Common adjustments

### "I want more shorts in bearish trend"

- Increase `momentum` multiplier under `bearish trend` (e.g. 1.15 → 1.25).
- Or reduce the alignment penalty for shorts in bearish (`_market_alignment` returns 0.88; increasing wouldn't help — it's already high).
- Or lower `b_tier` threshold (risky; affects all modes).

### "I want fewer MEXC-only ideas"

- Increase `min_24h_quote_volume_per_exchange.mexc` to 5M+.
- Or set `mexc.enabled = false` in `config/exchanges.yaml` temporarily.
- Or change the MEXC-only cap from 70 → 60 in `scoring_agent.py` (more aggressive).

### "I want stricter A-tier"

- Increase `a_tier` threshold to 82 or 85.
- Already A-tier requires `not caps` — that gate is hard.

### "I want more swing ideas in `bullish trend`"

- Increase `swing.narrative` multiplier or `swing.catalyst_news`.
- Add more configured narratives (see [[Sector_Overview]]).

### "Telegram is creating false confidence"

- Telegram does not directly feed score — the lever is `CrowdAttentionAgent._attention_score` (line ~85). Lower the per-note weights to mute Telegram-derived attention.

## Validation

- After any change, run `python -m src.cli daily-report --auto-universe` and compare top 5 ideas.
- Use `ReviewAgent` (`python -m src.cli review`) on a backtesting window if available.

## Hard-don'ts

- Don't lower `no_clear_invalidation` penalty.
- Don't remove score caps.
- Don't push A-tier threshold below 78.

## Related

- [[How_to_Adjust_Filters]]
- [[Scoring_Overview]]
- [[Score_Caps]]

## Implemented status

- **Operator guide**.
