# Stock Swing Mode

Horizon: several days to a few weeks.
Run: `python -m src.cli stocks-swing-report`

## Timeframes

- Execution: 1h
- Context: 1d

## Priorities (scoring multipliers)

- `sector_confirmation` ×1.10 — sector alignment matters most over multi-day holds
- `index_confirmation` ×1.05
- `relative_strength` ×1.10
- `earnings_risk_adjustment` ×1.30 — much stronger penalty than intraday
- `technical_setup` ×0.95 — slightly de-emphasized (regime + sector dominate over days)

## Hard rules

- **Block** any new swing entry if `days_ahead ≤ 2` to next earnings (unless the user explicitly invokes earnings-strategy mode).
- Downgrade if `days_ahead ≤ 5` (`earnings_within_3_days_for_swing` penalty applies for ≤3 days).
- Require a clean invalidation that respects daily structure (not just intraday wicks).

## Required confirmations for A-tier

1. Daily trend is directional.
2. Sector status agrees with direction (strong for longs, weak for shorts).
3. Index direction agrees.
4. RR to TP1 ≥ 1.5.
5. No earnings within the blocking window.
6. RS classification ≥ follower (longs) or laggard (shorts).

## Common rejects

- Earnings within 2 days (`earnings_blocks_swing_entry` block).
- Sector contradicts direction (-6 penalty).
- Range trend (no directional setup).
- No invalidation.

## Position management note

Swing trades that fire on Friday close should be sized smaller — weekend gap risk is real. Stage 7 will add a `friday_close_size_haircut` config knob; for now, manually halve size on Friday entries.
