# Weekend Mode Checklist

For an LLM session running on Saturday or Sunday. Run this **before** producing any trade ideas, on top of [[Pre_Analysis_Checklist]].

---

## A — Confirm Weekend Mode status

- [ ] Run `python -m src.cli weekend-status` (or read the Weekend Mode section in `data/processed/llm_analysis_packet.md`).
- [ ] `active: true`? Then continue with this checklist.
- [ ] Note the day, current project time, and timezone.
- [ ] Note the mode-specific overrides for the requested mode.

If `active: false`, this checklist is skipped — proceed with [[Pre_Analysis_Checklist]] only.

## B — Calibrate expectations

- [ ] A-tier requires score ≥ 80 + zero caps **AND** a margin above 80 because `a_tier_score_penalty` (typ. 5, up to 7 for scalp) is subtracted.
- [ ] Confidence labels are stepped down one band — "high" today means "medium-high" pre-weekend.
- [ ] Weak signals are capped at B; weak MEXC-only at C.
- [ ] Chasing entries (extension > 2 ATR) are demoted to C even if score is high.
- [ ] Tight stops (< 0.8 ATR from price) trigger an explicit warning.

## C — Per-mode posture

### Scalp (strictest)

- [ ] Demand immediate trigger + confirmation.
- [ ] Refuse entries directly after a vertical 1m/5m candle.
- [ ] Max holding time should be explicit (≤ 2h).
- [ ] Stop must be outside the most recent wick zone.

### Intraday (default)

- [ ] Prefer pullback / retest entries over chasing breakouts.
- [ ] Demand 15m/1h acceptance before entering on a breakout.
- [ ] R/R to TP1 ≥ 1.2 (not the weekday ≥ 1.0).
- [ ] Use structural invalidation over fixed ATR.

### Swing (light)

- [ ] Higher-timeframe structure still rules.
- [ ] Add the weekend liquidity warning, but don't over-penalize.
- [ ] Avoid swing entries in the 24h before Monday open.

### Invest / long-term (informational)

- [ ] No score change.
- [ ] Warn the user that execution is worse and weekend wicks are noisy.
- [ ] Consider waiting for Monday open to enter.

## D — Per-symbol checks

For every candidate that survives [[Pre_Analysis_Checklist]] gates:

- [ ] Look at `weekend_mode_latest.json` — did this symbol get downgraded? Why?
- [ ] Cap reasons containing "weekend: ..." — surface them in the trade idea card.
- [ ] If the symbol is MEXC-only, the cap is already at most C — skip unless exceptional.
- [ ] If `notes` includes "tight stop warning" — explicitly tell the user.
- [ ] If `notes` includes "retest after impulse required" — make that the entry condition.

## E — Output adjustments

Every trade idea card on a weekend must include:

- `weekend_mode_active: true`
- `weekend_adjustment_summary` (one line summarizing the notes)
- Whether retest/confirmation is required
- Whether the stop is too tight for weekend conditions
- Whether the idea was downgraded
- Final tier after the overlay

Example block to add to the trade idea card:

```
Weekend Mode: ACTIVE (Saturday, Asia/Nicosia)
  Original tier/score: A / 82.0
  Adjusted tier/score: B / 77.0
  Notes: weekend: -5 a-tier margin penalty; weekend: prefer structural invalidation
  Tight stop warning: no
  Retest required: yes (24h move +7%)
```

## F — Closing summary additions

When closing the analysis ([[Post_Analysis_Checklist]]):

- [ ] State explicitly that Weekend Mode was active.
- [ ] List symbols downgraded by the overlay.
- [ ] Include the standard weekend reminders: thinner liquidity, demand retests, avoid scalp in dead hours.
- [ ] Update [[Current_Context_For_LLM]] to include the Weekend Mode banner.

## G — When to deviate from Weekend Mode

You can argue for treating a setup more aggressively than the overlay suggests **only** when:

- Score survived the overlay AND no caps fired.
- Cross-exchange confirmation is unusually clean.
- Catalyst is verified primary source.
- Operator explicitly requests scalp/intraday execution and accepts the elevated risk.

Even then: do not override caps. The cap is the cap.

## Related

- [[Weekend_Mode]]
- [[Weekend_Liquidity_Risk]]
- [[Pre_Analysis_Checklist]]
- [[Post_Analysis_Checklist]]
- [[Pre_Trade_Checklist_For_LLM]]
- [[Score_Caps]]

## Implemented status

- **Operator framework / checklist**.
